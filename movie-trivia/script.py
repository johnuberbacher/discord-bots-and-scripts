import discord
import requests
import asyncio
import html

from config import movie_channel_id, bot_token

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
        answer = html.unescape(data['results'][0]['correct_answer'])

        message = "**Random Movie Trivia:**\n\n" + question + '\n\nThe answer is ||' + answer + '||!\nWant another? Just type `/trivia` in the movie channel.'
        print(message)

        channel = client.get_channel(movie_channel_id)
        await channel.send(message)
    else:
        print("Request failed with status code:", response.status_code)

client.run(bot_token)
