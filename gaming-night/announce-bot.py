import discord
import os
from requests_html import HTMLSession
import random
import asyncio
import datetime
import sys
from config import gaming_channel_id, bot_token

# Set up the Discord client
intents = discord.Intents.default()
intents.members = True

# Create a Discord client
client = discord.Client(intents=intents)

# 20-top Cross Platform Games
games = [
    ["Fortnite", "Rocket League", "Call of Duty: Warzone", "Minecraft", "Destiny 2", "Apex Legends", "Genshin Impact", "PUBG", "SMITE", "Warframe", "Dead by Daylight", "Back 4 blood", "Dauntless", "Elder Scrolls Online", "Fall Guys", "Deep Rock Galactic", "Rogue Company", "Overcooked 2", "Sea of Thieves", "Wargroove"]
]
games_string = "\n".join([game for sublist in games for game in sublist])


# Define a function to send a Discord message with the details of a randomly selected anime
async def send_friday_night_gaming_message():
    channel = client.get_channel(gaming_channel_id)

    message = f"Hey @everyone! \n\nIt's Friday which means it's **Gaming Night!** \n\nWho's ready to kick off the weekend with some gaming fun? If you're planning on gaming tonight, drop a message in the server and let us know what you're playing! And if you need any help getting started or finding a group, don't hesitate to ask! \n\nFor those of you looking for some cross-platform compatible games, here are a few options that we can play whether you game on PC, Xbox, PS4 and PS5: \n\n{games_string} \n\nOf course, these are just a few suggestions - feel free to share your own favorites in the server as well. Let's get gaming and have a great time tonight!"
    await channel.send(message)
    print(message)

    await client.close()

# Start the scheduled task when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await send_friday_night_gaming_message()

# Run the bot
client.run(bot_token)