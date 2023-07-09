import discord
from discord.ext import commands
import requests
import asyncio
import html
import requests

from config import movie_channel_id, bot_token

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command(pass_context=True)
async def trivia(ctx):
    if ctx.channel.id == movie_channel_id:
        await getTrivia()
    else:
        await ctx.send('This command can only be used in the movie channel.')

async def getTrivia():
    url = "https://opentdb.com/api.php?amount=1&category=11&type=multiple"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        question = html.unescape(data['results'][0]['question'])
        answer = html.unescape(data['results'][0]['correct_answer'])

        await send_message("**Random Movie Trivia:**\n\n" + question + '\n\nThe answer is ||' + answer + '||!\nWant another? Just type `/trivia` in the movie channel.')
        print("**Random Movie Trivia:**\n\n" + question + '\n\nThe answer is ||' + answer + '||!\nWant another? Just type `/trivia` in the movie channel.')
    else:
        print("Request failed with status code:", response.status_code)

async def send_message(message):
    channel = bot.get_channel(movie_channel_id)
    await channel.send(message)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")

bot.run(bot_token)
