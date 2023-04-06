import discord
import asyncio
import requests
import json
import sys
sys.path.append('..')

from config import github_user, channel_id, bot_token

# Set up the Discord client
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# Define a function to get the latest repository name for the specified GitHub user
def get_latest_repo():
    url = f"https://api.github.com/users/{github_user}/repos"
    response = requests.get(url)
    repos = json.loads(response.content)
    # latest_repo_name = repos[0]["name"]
    latest_repo_url = repos[0]["html_url"]
    return latest_repo_url

# Define a function to send a message to the specified Discord channel
async def send_message(message):
    channel = client.get_channel(channel_id)
    await channel.send(message)

# Set up the Discord bot event handler for when the bot is ready
@client.event
async def on_ready():
    print(f"{client.user.name} is ready.")

# Set up a loop to check for new repositories every 3 hours (10800 seconds)
@client.event
async def on_ready():
    current_repo = ""
    print(f"{client.user.name} is ready.")
    while True:
        latest_repo = get_latest_repo()
        if latest_repo != current_repo:
            print(f"{current_repo} is the current repo.")
            print(f"{latest_repo} is the latest repo.")
            current_repo = latest_repo
            await send_message(f"{github_user} just published a new repository: \n{latest_repo}")
            print(f"{current_repo} is now the latest repo.")
        await asyncio.sleep(10800)

# Start the Discord bot
client.run(bot_token)