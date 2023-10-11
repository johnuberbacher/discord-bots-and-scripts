## Console Release Anniversary Bot

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)

This is a Discord bot written in Python that reminds users of upcoming console releases. The bot checks a JSON file (consoles.json) for release dates and sends a message in a specified Discord channel on the day of the release, along with a related fact about the console. The bot also looks for an associated image in the /images/ folder to include in the message.

### Prerequisites
Before running the bot, make sure you have the following prerequisites installed:
- Python 3.x
- discord.py library

You will also need to create a Discord bot and obtain its token. Follow these steps:
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on "New Application" and enter a name for your bot.
3. Go to the "Bot" tab and click on "Add Bot".
4. Copy the bot token.


### Setup
1. Clone or download the repository to your local machine.
2. Install the required libraries by running the following command in your terminal:
```
pip install discord.py requests Pillow
```
3. Replace the placeholders in the config.py file with your Discord channel ID and bot token:
```
channel_id = YOUR_CHANNEL_ID
bot_token = YOUR_BOT_TOKEN
```
4. Run the script: 
```
python script.py
```

### How it Works
1. The bot loads console data from the consoles.json file.
2. It compares the current date with the release dates of the consoles.
3. If a console is releasing on the current day, the bot prepares a message with a fact about the console.
4. The bot checks for an associated image in the /images/ folder and attaches it to the message.
5. The bot sends the message to the specified Discord channel.
6. The bot exits after processing all consoles.

### Example
![](https://i.imgur.com/IO7htC1.png)
