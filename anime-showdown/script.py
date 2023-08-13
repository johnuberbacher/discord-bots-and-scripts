import discord
from discord.ext import commands
import os
import requests
import json
import random
import asyncio
from PIL import Image, ImageDraw, ImageFont
from config import anime_channel_id, bot_token
from discord.ext import commands

characters_to_fetch = 100 # fetch the top 50 characters from the api
voting_duration = 10800 # 10800s ~ 3 hours

# Set up the Discord client
intents = discord.Intents.default()
intents.members = True

# Create a Discord client
client = discord.Client(intents=intents)

def fetch_top_anime_characters(ignore_list=None):
    url = "https://api.jikan.moe/v4/top/characters"
    params = {
        "type": "anime"
    }

    characters = []
    page = 1
    while len(characters) < characters_to_fetch:
        params["page"] = page
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        for character in data["data"]:
            if ignore_list and character["name"] in ignore_list:
                continue
            characters.append(character)
            if len(characters) >= characters_to_fetch:
                break
        page += 1

    return characters
# Fetch all the anime characters
ignore_list = []
if os.path.exists("ignore.txt"):
    with open("ignore.txt", "r") as f:
        ignore_list = [line.strip() for line in f]

all_characters = fetch_top_anime_characters(ignore_list=ignore_list)

# Select 2 random characters from the fetched list
random_characters = random.sample(all_characters, 2)

# Create a blank white image with a size of 600x300
final_image = Image.new("RGB", (600, 300), "white")

# Open and resize the first character's image
character1_image = Image.open(requests.get(random_characters[0]['images']['jpg']['image_url'], stream=True).raw)
character1_image.thumbnail((300, 300))

# Calculate the position to paste the first character's image
character1_position = (
    (300 - character1_image.width) // 2,
    (300 - character1_image.height) // 2
)

# Open and resize the second character's image
character2_image = Image.open(requests.get(random_characters[1]['images']['jpg']['image_url'], stream=True).raw)
character2_image.thumbnail((300, 300))

# Calculate the position to paste the second character's image
character2_position = (
    300 + (300 - character2_image.width) // 2,
    (300 - character2_image.height) // 2
)

# Paste the first character's image on the left side of the final image
final_image.paste(character1_image, character1_position)

# Paste the second character's image on the right side of the final image
final_image.paste(character2_image, character2_position)

# Add character names at the bottom of each square
font_size = 30
font_weight = "bold"
font_color = "white"
stroke_color = "black"
character1_stroke_color = "blue"
character1_outline_color = "blue"
character2_stroke_color = "red"
character2_outline_color = "red"
text_align = "center"

draw = ImageDraw.Draw(final_image)
font = ImageFont.truetype("arial.ttf", font_size)

# Calculate the text position for the first character's name
character1_name = random_characters[0]["name"]
character1_text_width, character1_text_height = draw.textsize(character1_name, font=font)
character1_text_position = (
    character1_position[0] + (character1_image.width - character1_text_width) // 2,
    character1_position[1] + character1_image.height - character1_text_height - 30
)

# Calculate the text position for the second character's name
character2_name = random_characters[1]["name"]
character2_text_width, character2_text_height = draw.textsize(character2_name, font=font)
character2_text_position = (
    character2_position[0] + (character2_image.width - character2_text_width) // 2,
    character2_position[1] + character2_image.height - character2_text_height - 30
)

# Draw the text on the image for the first character's name
draw.text(character1_text_position, character1_name, font=font, weight=font_weight, fill=font_color, stroke_width=4, stroke_fill=character1_stroke_color, align=text_align)

# Draw the text on the image for the second character's name
draw.text(character2_text_position, character2_name, font=font, weight=font_weight, fill=font_color, stroke_width=4, stroke_fill=character2_stroke_color, align=text_align)

# Add "vs" text in the middle of the screen
vs_text = "vs"
vs_text_width, vs_text_height = draw.textsize(vs_text, font=font)
vs_text_position = (
    (600 - vs_text_width) // 2,
    (300 - vs_text_height) // 2
)

draw.text(vs_text_position, vs_text, font=font, fill=font_color, stroke_width=4, stroke_fill=stroke_color, align=text_align)

# Save the finalized image as showdown.jpg
final_image.save("showdown.jpg")

async def get_character_anime(character_id):
    # Replace the placeholder with the provided character ID
    url = "https://api.jikan.moe/v4/characters/{id}/anime".replace("{id}", str(character_id))    
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data["data"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Define a function to send a Discord message with the details of the new anime showdown
async def send_random_anime(channel, anime_list):
    character1_anime = await get_character_anime(random_characters[0]["mal_id"])
    character1_name = random_characters[0]["name"]
    character1_bio = random_characters[0]["about"][:200] if len(random_characters[0]["about"]) <= 200 or random_characters[0]["about"][200] == ' ' else random_characters[1]["about"][:random_characters[0]["about"].rfind(' ', 0, 200)]
    
    character2_anime = await get_character_anime(random_characters[1]["mal_id"])
    character2_name = random_characters[1]["name"]
    character2_bio = random_characters[1]["about"][:200] if len(random_characters[1]["about"]) <= 200 or random_characters[1]["about"][200] == ' ' else random_characters[1]["about"][:random_characters[1]["about"].rfind(' ', 0, 200)]
    
    if character1_anime:
        print("Character1 Anime Data:")
        print(character1_anime[0]["anime"]["title"])
        
    if character2_anime:
        print("Character1 Anime Data:")
        print(character2_anime[0]["anime"]["title"])
    
    # Load the image file
    with open('showdown.jpg', 'rb') as f:
        image = discord.File(f)

    # Send the image as an attachment in a message
    message = await channel.send(file=image)

    # Send the text message
    poll_message = await channel.send(f"🔥 Anime Showdown Alert! 🔥\n\n🔵 **{character1_name}** from {character1_anime[0]['anime']['title']} \n\nor \n\n🔴 **{character2_name}** from {character2_anime[0]['anime']['title']} \n\nIt's time to decide the ultimate champion, whether through their power, intellect, or maybe you just want to vote for your favorite! Who will prevail? \n\nChoose now and let your voice be heard! 💫 💪\n\nWho are you voting for?")

    # Add reactions to the poll message
    await poll_message.add_reaction("🔵")  # Blue circle emoji
    await poll_message.add_reaction("🔴")  # Red circle emoji

    # Wait for the voting duration
    await asyncio.sleep(voting_duration)

    # Fetch the updated poll message
    updated_poll_message = await channel.fetch_message(poll_message.id)
 
    # Get the vote counts for each option
    blue_count = 0
    red_count = 0

    for reaction in updated_poll_message.reactions:
        if str(reaction.emoji) == "🔵":
            blue_count = reaction.count - 1  # Subtract 1 to exclude the bot's own reaction
        elif str(reaction.emoji) == "🔴":
            red_count = reaction.count - 1  # Subtract 1 to exclude the bot's own reaction

    # Calculate the percentage of votes for each option
    total_votes = blue_count + red_count
    blue_percentage = (blue_count / total_votes) * 100 if total_votes > 0 else 0
    red_percentage = (red_count / total_votes) * 100 if total_votes > 0 else 0

  
    # async for message in channel.history(limit=1):
    #     if message.author == client.user:
    #        await message.delete()
       
    # Send the voting results         
    await channel.send(f"🔥 Voting has ended! 🔥 \n\nHere are the results:\n\n🔵 {character1_name}: {blue_count} votes ({blue_percentage:.2f}%)\n🔴 **{character2_name}: {red_count} votes ({red_percentage:.2f}%)**")
    await client.close()
    await quit()

# Run the Discord client
@client.event
async def on_ready():
    channel = client.get_channel(anime_channel_id)
    await send_random_anime(channel, random_characters)

client.run(bot_token)
