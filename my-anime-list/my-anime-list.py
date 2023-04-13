import discord
import requests
from bs4 import BeautifulSoup
import random
import tabulate
import asyncio
import sys
import datetime
sys.path.append('..')
from config import anime_channel_id, bot_token

# Set up the Discord client
intents = discord.Intents.default()
intents.members = True

# Create a Discord client
client = discord.Client(intents=intents)

# Define a function to scrape the top 50 anime list
def scrape_top_anime():
    url = 'https://myanimelist.net/topanime.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='top-ranking-table')
    rows = table.find_all('tr', class_=('ranking-list'))
    anime_list = []
    for row in rows:
        title = row.find('div', class_='di-ib clearfix').a.text.strip()
        score = row.find('span', class_='score-label').text.strip()
        page_url = row.find('div', class_='di-ib clearfix').a.get('href')
      
        anime_list.append({'page_url': page_url, 'title': title, 'score': score})
      
    return anime_list

# Define a function to send a Discord message with the details of a randomly selected anime
async def send_random_anime():
    anime_list = scrape_top_anime()
    anime = random.choice(anime_list)
    title = anime['title']
    score = anime['score']
    page_url = anime['page_url']

    await client.get_channel(anime_channel_id).send(f"The random anime of the day is... \n\n**{title}** \n\nIt currently sits with an average score of **⭐{score}** on MAL. \n\n**What do YOU think about {title}?** \nHave you seen it? Is it on any of your lists? Why or why not?")
    print(f"The random anime of the day is... \n\n**{title}** \n\nIt currently sits with an average score of **⭐{score}** on MAL. \n\n**What do YOU think about {title}?** \nHave you seen it? Is it on any of your lists? Why or why not?")

    await client.get_channel(anime_channel_id).send(f"_ _\n{page_url}")
    
# Define a task to run the send_random_anime function every day at 8:00am Mountain Time
async def scheduled_task():
    while True:
        # Get the current time in Mountain Time
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-7)))
        # Calculate the time for the next run at 9:30am Mountain Time
        next_run = datetime.datetime(now.year, now.month, now.day, 9, 30, tzinfo=now.tzinfo)
        if next_run < now:
            # The next run time has already passed today, so schedule for tomorrow
            next_run += datetime.timedelta(days=1)
        # Calculate the number of seconds until the next run
        seconds_until_next_run = (next_run - now).total_seconds()
        # Sleep until the next run
        print(f'Sleeping...')
        await asyncio.sleep(seconds_until_next_run)
        # Run the task
        print(f'Looking for anime...')
        await send_random_anime()

# Start the scheduled task when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    client.loop.create_task(scheduled_task())

# Run the bot
client.run(bot_token)
