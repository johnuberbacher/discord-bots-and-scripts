import discord
import asyncio
import json
import os
from datetime import datetime

from config import channel_id, bot_token

# Set up the Discord client
intents = discord.Intents.default()
intents.members = True

# Create a Discord client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user.name} is ready.")
    await asyncio.sleep(1)
    await check_console_release()
    await client.close()  # Close the client when done

async def check_console_release():
    # Load console data from consoles.json
    with open('consoles.json', 'r') as file:
        data = json.load(file)

    # Get the current month and day
    current_month_day = datetime.now().strftime('%m-%d')

    for console in data["consoles"]:
        try:
            release_date = datetime.strptime(console["release_date"], '%Y-%m-%d')

            # Check if month or day is '00'
            if release_date.month == 0 or release_date.day == 0:
                print(f"Skipping invalid date for {console['name']}: {console['release_date']}")
                continue

            release_month_day = release_date.strftime('%m-%d')
        except ValueError:
            # Handle invalid date format
            print(f"Invalid release_date format for {console['name']}: {console['release_date']}")
            continue

        if release_month_day == current_month_day:
            # Assuming images are stored in the /images/ folder and named with the console's name as the filename (lowercased)
            image_filename = f"images/{console['name'].lower()}.jpg"

            # Prepare the message content
            message_content = f"{console['fact']}\n\nDo you have a favorite **{console['name']}** game?"

            # Get the channel using the defined channel_id
            channel = client.get_channel(channel_id)

            # Check if the image file exists
            if os.path.exists(image_filename):
                # Send the message with the locally saved image
                await channel.send(content=message_content, file=discord.File(image_filename))
            else:
                # Send only text if the image is not found
                await channel.send(content=message_content)

client.run(bot_token)
