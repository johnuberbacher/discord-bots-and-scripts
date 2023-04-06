import discord
import requests
import json

# Set up the Discord client and GitHub user to monitor
client = discord.Client()
github_user = "your_github_username"

# Set up the Discord channel to send messages to
channel_id = your_discord_channel_id
bot_token = your_bot_token

# Define a function to get the latest repository name for the specified GitHub user
def get_latest_repo():
    url = f"https://api.github.com/users/{github_user}/repos"
    response = requests.get(url)
    repos = json.loads(response.content)
    latest_repo_name = repos[0]["name"]
    return latest_repo_name

# Define a function to send a message to the specified Discord channel
async def send_message(message):
    channel = client.get_channel(channel_id)
    await channel.send(message)

# Set up the Discord bot event handler for when the bot is ready
@client.event
async def on_ready():
    print(f"{client.user.name} is ready.")

# Set up a loop to check for new repositories every minute
@client.event
async def on_ready():
    print(f"{client.user.name} is ready.")
    while True:
        latest_repo = get_latest_repo()
        if latest_repo != current_repo:
            current_repo = latest_repo
            await send_message(f"{github_user} just published a new repository: {latest_repo}")
        await asyncio.sleep(60)

# Start the Discord bot
client.run(bot_token)