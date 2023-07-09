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
```
python script.py
```

### How it Works
1. The bot connects to Discord using the provided bot token and sets up the necessary configurations.
2. When the bot is ready, it prints a message to indicate that it is online and waits for 1 second.
3. The get_trivia() function is called, which fetches a random movie trivia question from the Open Trivia Database API.
4. The API response is processed, extracting the question and answer from the received data.
5. A message is constructed using the extracted question and answer. The answer is hidden using the spoiler syntax to create an element of surprise.
6. The constructed message is sent to the designated movie channel using the channel.send() method.
7. If the API request fails, an error message is printed to the console.
8. The bot continues to run, listening for events and responding to commands
