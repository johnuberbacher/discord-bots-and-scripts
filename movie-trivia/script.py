import discord
import requests
import asyncio
import html
import random

from config import channel_id, bot_token

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user.name} is ready.")
    await asyncio.sleep(1)
    await get_trivia()

async def get_trivia():
    url = "https://opentdb.com/api.php?amount=1&category=11&type=multiple"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        question = html.unescape(data['results'][0]['question'])
        correct_answer = html.unescape(data['results'][0]['correct_answer'])
        incorrect_answers = [html.unescape(answer) for answer in data['results'][0]['incorrect_answers']]
        
        options = [correct_answer] + incorrect_answers
        random.shuffle(options)
        
        # Format the options with a newline after each option
        options_text = '\n'.join(f"{option}" for option in options)
        
        # Check if correct_answer is smaller than 10 characters
        if len(correct_answer) < 20:
            # Add spaces around correct_answer
            correct_answer = f"{' ' * 8}{correct_answer}{' ' * 8}"

            
        channel = client.get_channel(channel_id)
        embed = discord.Embed(
            colour=0x00b0f4,
            color=discord.Color.dark_theme()
        )
        embed.set_author(name="Random Movie Trivia")
        embed.add_field(name="", value=f"{question}\n\n{options_text}", inline=False)
        embed.add_field(name="", value=f"The answer is ||{correct_answer}||!", inline=False)

        await channel.send(embed=embed)
        await client.close()
    else:
        print("Request failed with status code:", response.status_code)

client.run(bot_token)
