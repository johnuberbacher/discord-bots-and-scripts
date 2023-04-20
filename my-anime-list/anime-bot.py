import discord
import os
from requests_html import HTMLSession
import random
import asyncio
import datetime
import sys
sys.path.append('..')
from config import anime_channel_id, bot_token

# Set up the Discord client
intents = discord.Intents.default()
intents.members = True

# Create a Discord client
client = discord.Client(intents=intents)

# Define a function to scrape the top 50 anime list
def scrape_top_anime():
    session = HTMLSession()
    url = 'https://myanimelist.net/topanime.php'
    response = session.get(url)
    table = response.html.find('table.top-ranking-table', first=True)
    rows = table.find('tr.ranking-list')
    anime_list = []
    for row in rows:
        title = row.find('div.di-ib.clearfix a', first=True).text.strip()
        score = row.find('span.score-label', first=True).text.strip()
        page_url = row.find('div.di-ib.clearfix a', first=True).attrs['href']
        anime_list.append({'page_url': page_url, 'title': title, 'score': score})
    return anime_list

# Define a function to send a Discord message with the details of a randomly selected anime
async def send_random_anime(anime_list):
    anime = random.choice(anime_list)
    title = anime['title']
    score = anime['score']
    page_url = anime['page_url']
    channel = client.get_channel(anime_channel_id)
    await channel.send(f"The random anime of the day is... \n\n**{title}** \n\nIt currently sits with an average score of **⭐{score}** on MAL. \n\n**What do YOU think about {title}?** \nHave you seen it? Is it on any of your lists? Why or why not? \n\n{page_url}")
    print(f"The random anime of the day is... \n\n**{title}** \n\nIt currently sits with an average score of **⭐{score}** on MAL. \n\n**What do YOU think about {title}?** \nHave you seen it? Is it on any of your lists? Why or why not? \n\n{page_url}")
    await client.close()

# Start the scheduled task when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    anime_list = scrape_top_anime()
    await send_random_anime(anime_list)

# Run the bot
client.run(bot_token)