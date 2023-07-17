## Game Sales Discord Bot

This Discord bot provides information about top game sales on Steam and Nintendo Switch. It scrapes data from the Steam store and DekuDeals website to fetch the latest deals. The bot sends a message with the top sale games to a specified channel on Discord.

- Fetches the top sale games from Steam and Nintendo Switch.
- Provides game names, sale prices, and discount percentages.
- Sends a Discord message with the game information.
- Includes URLs to the respective store pages for more details.

### Setup
- Install the required dependencies: `pip install discord requests beautifulsoup4 prettytable tabulate`
- Obtain a bot token from the Discord Developer Portal.
- Create a config.py file in the same directory as the code with the following content:
```
game_sales_channel_id = YOUR_GAMES_CHANNEL_ID  # Replace with the channel ID where you want the bot to send the game sales messages.
bot_token = "YOUR_DISCORD_BOT_TOKEN"  # Replace with your Discord bot token.
```
- Replace YOUR_GAMES_CHANNEL_ID with the ID of your movie channel and 'YOUR_BOT_TOKEN' with the obtained bot token.
- Run the code: 
```
python script.py
```

### How it Works
1. The bot scrapes game sales data from the Steam store and DekuDeals website.
2. It retrieves the specified Discord channel and selects a random greeting.
3. The bot formats the game sales data into ASCII tables.
4. A Discord message is sent with the greeting and the top sale games' table, including URLs for more details.

### Example
![](https://i.imgur.com/ECqvENi.png)