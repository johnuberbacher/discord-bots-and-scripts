## GitHub Updates Bot

This is a Discord bot written in Python that checks for recent repository creations by specified GitHub users and sends notifications to a specified Discord channel. The bot utilizes the GitHub API to fetch the repositories and their details.

### Prerequisites
Before running the bot, make sure you have the following prerequisites installed:
- Python 3.x
- discord.py library
- requests library

You will also need to create a Discord bot and obtain its token. Follow these steps:
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on "New Application" and enter a name for your bot.
3. Go to the "Bot" tab and click on "Add Bot".
4. Copy the bot token.


### Setup
1. Clone or download the repository to your local machine.
2. Install the required libraries by running the following command in your terminal:
```
pip install discord.py requests
```
3. Replace the placeholders in the config.py file with your Discord channel ID and bot token:
```
channel_id = YOUR_DISCORD_CHANNEL_ID
bot_token = YOUR_BOT_TOKEN
github_users = ['GITHUB_USERNAME_1', 'GITHUB_USERNAME_2', ...]
```
4. Run the script: 
```
python script.py
```

### How it Works
1. The bot connects to the Discord server using the provided bot token and waits for the `on_ready` event.
2. Once the bot is ready, it calls the `check_github_updates` function.
3. The `check_github_updates` function iterates over the specified GitHub usernames.
4. For each username, the bot sends a request to the GitHub API to fetch the user's repositories.
5. If the request is successful (status code 200), the bot checks each repository's creation date.
6. If a repository was created within the last 24 hours, the bot generates a message with the repository details and sends it to the specified Discord channel.
7. If no new repositories are found for a user or the request fails, the bot logs the corresponding message.
8. After processing all the GitHub usernames, the bot closes the Discord client.
