## Movie Trivia Bot

This Discord bot provides random movie trivia questions for entertainment in the designated movie channel.

- Retrieves random movie trivia questions from an API.
- Sends trivia questions and answers to the movie channel.
- Restricts the usage of the /trivia command to the movie channel.
- Automatically sends a trivia question when the bot is ready.

### Setup
- Install the required dependencies:
- Obtain a bot token from the Discord Developer Portal.
- Create a config.py file in the same directory as the code with the following content:
```
movie_channel_id = YOUR_MOVIE_CHANNEL_ID
bot_token = 'YOUR_BOT_TOKEN'
```
- Replace YOUR_MOVIE_CHANNEL_ID with the ID of your movie channel and 'YOUR_BOT_TOKEN' with the obtained bot token.
- Run the code: 
`python script.py`
