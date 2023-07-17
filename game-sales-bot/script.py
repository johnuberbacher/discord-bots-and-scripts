import discord
import requests
import random
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from tabulate import tabulate
import asyncio
import time
import sys
from config import game_sales_channel_id, bot_token

# Set up the Discord client
intents = discord.Intents.default()
intents.members = True

# Create a Discord client
client = discord.Client(intents=intents)

num_games = 10
greetings = [
    "Rise and shine, you scrumptious muffins!",
    "Good morning, you bunch of wildflowers!",
    "Wakey wakey, pancakes and bacon!",
    "Greetings, you fearless explorers!",
    "Hey there, you funky monkeys!",
    "Rise and shine, my little donut holes!",
    "Good morning, you lovely bunch of coconuts!",
    "Wakey wakey, eggs and bakey!",
    "Greetings, my fellow adventurers!",
    "Hey there, you crazy cats and kittens!"
]

# Function to scape top Steam sale games
def get_top_steam_sale_games(num_games):

    # Steam URL with search query for games on sale
    url = f"https://store.steampowered.com/search/?specials=1"

    # Send a request to the URL and get the response
    response = requests.get(url)
    
    # Parse the response with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the container for the top sale games
    top_steam_sale_games = soup.find_all("div", class_="responsive_search_name_combined")

    games_info = []
    for game in top_steam_sale_games[:num_games]:

        # Get the game name
        name = game.find("span", class_="title").text.strip()

        # Get the game sale price and original price
        price_div = game.find("div", class_="search_price_discount_combined")
        if price_div.find_all("div"):
            
            sale_price = price_div.find_all("div", class_="discount_final_price")[0].text.strip()
            sale_amount = price_div.find_all("div", class_="discount_pct")[0].text.strip()
            print(sale_price)
            # truncated_sale_price = sale_price.index("$", sale_price.index("$") + 1)
            #truncated_sale_price = sale_price
            #sale_price = sale_price[truncated_sale_price+1:]
        else:
            sale_price = "N/A"
            sale_amount = "N/A"

        # Get the game review percentage
        review_div = game.find("div", class_="col search_reviewscore responsive_secondrow")
        if review_div:
            review_pct = review_div.span["data-tooltip-html"].split("<br>")[0]
        else:
            review_pct = "N/A"

        # Append the game information to the list
        # games_info.append([name, sale_amount, sale_price, review_pct])
        games_info.append([name, sale_amount, sale_price])

    return games_info

# Function to scape top Switch sale games
def get_top_switch_sale_games(num_games):

    # DekuDeals URL with search query for games on sale
    url = f"https://www.dekudeals.com/games?sales=1"

    # Send a request to the URL and get the response
    response = requests.get(url)

    # Parse the response with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the container for the top sale games
    game_divs = soup.find_all("div", class_="cell")
    print(game_divs)

    games_info = []
    for game in game_divs[:num_games]:

        # Get the game name
        name = game.find("div", class_="h6 name").text.strip()

        # Get the game sale price and original price
        price_div = game.find("div", class_="card-badge")
        if price_div:
            sale_price = price_div.find("strong").text.strip()
            original_price = price_div.find("s", class_="text-muted").text.strip()
        else:
            sale_price = "N/A"
            original_price = "N/A"

        # Get the game discount percentage
        discount_div = game.find("span", class_="align-text-bottom badge badge-danger")
        if discount_div:
            discount_pct = discount_div.text.strip()
        else:
            discount_pct = "N/A"

        # Append the game information to the list
        games_info.append([name, discount_pct, sale_price, original_price])

    return games_info
 
@client.event
async def on_ready():
    print("Bot is ready")
    channel = client.get_channel(game_sales_channel_id)
    # Get a random greeting
    greeting = random.choice(greetings)

    # Get the top sale games
    top_steam_sale_games = get_top_steam_sale_games(num_games)
    top_switch_sale_games = get_top_switch_sale_games(num_games)

    # Convert the list of games info into an ASCII table
    steamTable = tabulate(top_steam_sale_games, headers=["Name", "Discount", "Sale Price"])
    # switchTable = tabulate(top_switch_sale_games, headers=["Name", "Discount", "Sale Price", "Review Score"])

    # Send the greeting and the table in a Discord message
    await channel.send(f"{greeting} \n\nHere are the top {num_games} Steam games on sale right now!\n```\n{steamTable}\n-------------------------------------------------\nhttps://store.steampowered.com/search/?specials=1```\n\n")
    # await channel.send(f"_ _\nAnd here's the top {num_games} Switch games on sale (sorted by Popularity):\n```\n{switchTable}\n-------------------------------------------------\nhttps://www.dekudeals.com/games?sales=1```")

    await client.close()

client.run(bot_token)