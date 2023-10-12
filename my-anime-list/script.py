import discord
from requests_html import HTMLSession
import random
import asyncio
import sys

sys.path.append('..')
from config import channel_id, bot_token

chosen_category = ''
categories = ["tv", "movies", "upcoming", "airing", "favorite"]

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

def get_random_category_description(title, score, rank):
    chosen_category = random.choice(categories)
    if chosen_category == "tv":
        return f"**{title}** currently sits with an average score of **⭐{score}** on MAL, holding the **#{rank}** position on the 'Top TV Series' of all time. \n\nHave you seen {title}? If so, what did you think?"
    elif chosen_category == "movies":
        return f"**{title}** is one of the top anime movies of all time with a solid score of **⭐{score}** at rank **#{rank}** on MyAnimeList. \n\nHave you seen {title}? Where would you rank this movie among your favorites?"
    elif chosen_category == "upcoming":
        return f"**{title}** is an upcoming anime that you might want to keep an eye on. Anticipated to be a great addition to the anime world, it's currently sitting at rank **#{rank}** on MyAnimeList's Top Upcoming Anime list. \n\nWhat are your expectations for this upcoming release?"
    elif chosen_category == "airing":
        return f"**{title}** is currently airing and sits at the **#{rank}** spot on MyAnimeList's Top Airing Anime with an average score of **⭐{score}**. \n\nAre you currently watching {title}? What are your thoughts on it so far?"
    elif chosen_category == "favorite":
        return f"**{title}** has earned its place as one of the most favorited anime shows and movies on MyAnimeList. With a remarkable score of **⭐{score}**, it's a fan favorite, holding the **#{rank}** position of Most Favorited Anime. \n\nHave you seen {title}? Is it one of your favorites as well?"

async def scrape_top_anime():
    session = HTMLSession()

    url = 'https://myanimelist.net/topanime.php?type=' + chosen_category
    response = session.get(url)
    table = response.html.find('table.top-ranking-table', first=True)
    rows = table.find('tr.ranking-list')
    anime_list = []

    for row in rows:
        title = row.find('div.di-ib.clearfix a', first=True).text.strip()
        score = row.find('span.score-label', first=True).text.strip()
        page_url = row.find('div.di-ib.clearfix a', first=True).attrs['href']
        rank = row.find('span.top-anime-rank-text', first=True).text.strip()

        anime_list.append({'page_url': page_url, 'title': title, 'score': score, 'rank': rank})

    return anime_list

async def send_random_anime(anime_list):
    anime = random.choice(anime_list)
    title = anime['title']
    score = anime['score']
    rank = anime['rank']
    page_url = anime['page_url']

    # Headlessly visit the new page and extract img_url
    session = HTMLSession()
    new_page_response = session.get(page_url)
    await asyncio.sleep(2)
    leftside_div = new_page_response.html.find('div.leftside', first=True)
    await asyncio.sleep(2)
    img_url = leftside_div.find('div > a > img', first=True).attrs['data-src']

    channel = client.get_channel(channel_id)
    embed = discord.Embed(
        title=title,
        url=page_url,
        colour=0x00b0f4,
        color=discord.Color.dark_theme()
    )
    embed.set_author(name="Random Anime of the Day")
    embed.add_field(name="", value=get_random_category_description(title, score, rank), inline=False)
    embed.set_image(url=img_url)

    await channel.send(embed=embed)
    print(get_random_category_description(title, score, rank) + f'\n\n{page_url}')

    await client.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    anime_list = await scrape_top_anime()
    await send_random_anime(anime_list)

# Run the bot
client.run(bot_token)