import discord
import requests
import asyncio
from datetime import datetime, timedelta
from config import channel_id, bot_token, github_users

# Set up the Discord client
intents = discord.Intents.default()
intents.members = True

# Create a Discord client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user.name} is ready.")
    await check_github_updates()

async def check_github_updates():
    for username in github_users:
        try:
            repos_url = f'https://api.github.com/users/{username}/repos?per_page=100&sort=created'
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(repos_url, headers=headers)

            if response.status_code == 200:
                repos = response.json()
                for repo in repos:
                    repo_name = repo['name']
                    html_url = repo['html_url']
                    created_at = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                    current_time = datetime.utcnow()
                    time_diff = current_time - created_at
                    if time_diff <= timedelta(hours=24):
                        hours = time_diff.seconds // 3600
                        minutes = (time_diff.seconds // 60) % 60
                        message = f"GitHub user **{username}** recently created the new repository **{repo_name}**\n\n{html_url}"
                        channel = client.get_channel(channel_id)
                        await channel.send(message)
                    else:
                        print(f"No new repositories in {repo_name} by {username}.")
            else:
                print(f"Failed to fetch repositories for {username}. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred for {username}: {str(e)}")
    
    await client.close()

# Run the main function
asyncio.run(client.start(bot_token))
