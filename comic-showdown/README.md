## Comic Book Showdown Bot

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)

This is a Discord bot written in Python that generates a comic book showdown between two randomly selected characters and allows users to vote for their favorite character. The bot uses the ComicVine API to fetch the top comic book characters, creates a collage image of the two characters, and posts it in a specified Discord channel. After a specified voting duration, the bot calculates the vote counts and percentages and announces the results.

### Prerequisites
Before running the bot, make sure you have the following prerequisites installed:
- Python 3.x
- discord.py library
- requests library
- Pillow library

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
comic_channel_id = YOUR_COMIC_CHANNEL_ID
bot_token = YOUR_BOT_TOKEN
```
4. Run the script: 
```
python script.py
```

### How it Works
1. The bot fetches the top comic book characters from the ComicVine API, limited to the specified number of characters (characters_to_fetch).
2. Two random characters are selected from the fetched list.
3. The bot creates a collage image (showdown.jpg) by combining the images of the two characters.
4. The character names are added to the bottom of each square in the collage image.
5. The bot sends a message in the specified Discord channel, attaching the collage image and starting a poll.
6. Users can vote for their favorite character by reacting to the poll message with a blue circle emoji (🔵) or a red circle emoji (🔴).
7. After the voting duration (voting_duration), the bot calculates the vote counts and percentages.
8. The bot announces the voting results in the Discord channel and exits.

### Example
![](https://i.imgur.com/SV3jV4M.png)
![](https://i.imgur.com/mrRrNa9.png)