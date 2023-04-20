import discord
import os
import asyncio
import datetime
import sys
from requests_html import HTMLSession
from config import announcement_channel_id, bot_token, stream_user_id
import random
import imdb
from plexlist import plexlist

# Set up the Discord client
intents = discord.Intents.default()
intents.members = True
movie = random.choice(plexlist)
movie_title = movie[0]
movie_url = movie[1]
with open('selection.txt', 'w') as f:
    f.write(movie_url)

# Create a Discord client
client = discord.Client(intents=intents)

# Get Description of Movie from IMDB
def get_movie_info(movie_title):
    ia = imdb.IMDb()
    search_results = ia.search_movie(movie_title)
    
    if not search_results:
        return "No movie found with the given title."
    
    movie_id = search_results[0].getID()
    movie = ia.get_movie(movie_id)
    
    title = movie.get('title')
    year = movie.get('year')
    plot = movie.get('plot outline')
    
    return f"**'{title}'**  ({year}) \n{plot}"

# Define a function to send a Discord message with the details of a randomly selected anime
async def announce_movie():
    channel = client.get_channel(announcement_channel_id)
    message = f"Hey @everyone! \n\nTonight's Random-Movie-Night feature will be... \n\n{get_movie_info(movie_title)}\n\nUser <@{stream_user_id}> will begin streaming the movie from within the <#1093292347640528991> channel at 7:00pm EST. To watch along, simply click on <@{stream_user_id}> at 7:00pm EST and then click on 'Watch Stream' \n\nSo grab your popcorn, get comfortable, and join us for an exciting viewing experience!"
    await channel.send(message)
    print(message)
    await client.close()

# Start the scheduled task when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await announce_movie()

# Run the bot
client.run(bot_token)
