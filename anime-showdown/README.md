## Anime Showdown Bot

This Discord bot creates anime showdowns by randomly selecting two top anime characters and allowing users to vote for their favorite.

- Fetches the top anime characters from the Jikan API.
- Selects two random characters for the showdown.
- Generates an image with the characters' images and names.
- Sends the image and a voting poll to the designated anime channel.
- Calculates the voting results after a specified duration.
- Displays the final voting results and percentage of votes for each character.

### Setup
- Install the required dependencies:
- Obtain a bot token from the Discord Developer Portal.
- Create a config.py file in the same directory as the code with the following content:
```
movie_channel_id = YOUR_ANIME_CHANNEL_ID
bot_token = 'YOUR_BOT_TOKEN'
```
- Replace YOUR_ANIME_CHANNEL_ID with the ID of your movie channel and 'YOUR_BOT_TOKEN' with the obtained bot token.
- Run the script: 
```
python script.py
```
