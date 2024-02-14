# main.py
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from db import create_db
from messages import on_message_received, on_reaction_received

load_dotenv()
bot_token = os.environ.get("BOT_TOKEN")
channel_id = os.environ.get("CHANNEL_ID")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    
    try:
        channel_ids = [channel.id for guild in bot.guilds for channel in guild.channels]
        await create_db(bot, channel_ids)
        print(f"{bot.user} has connected to SQLite!")
    except Exception as e:
        print(f"Something went wrong: {e}")
    finally:
        print(f"{bot.user} is running!")

@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot and reaction.message.author != user:
        await on_reaction_received(reaction, user)

@bot.event
async def on_message(message):
    if not message.author.bot:
        await on_message_received(message)
        await bot.process_commands(message)

bot.run(bot_token)
