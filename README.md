# Discord Bot with OpenAI Integration

This Discord bot integrates with OpenAI's API to provide dynamic responses based on user commands. It generates answers, explanations, and even images based on prompts provided in the Discord chat.

## Features

A few features I have implemented in this project are:

1. **Dynamic Response Generation:** Leverages OpenAI's powerful models to generate responses.
2. **Multiple Commands:** Includes commands like `ask`, `emoji`, `coding`, `speak`, `explain`, and `generate` to interact with OpenAI's models.  
3. **Text to Speech:** Converts text to speech for an interactive experience.
4. **Speech Explanation:** Provides speech explanation for given prompt


## Installation

Follow the instruction below to install and run the discord bot on your system:

1. Clone the project into your system
    ```
    git clone https://github.com/manishacharya60/discord-samsaraGPT.git
    ```
2. Navigate to the bot directory and run the following command to install required dependencies
    ```
    $ pip install -r requirements.txt
    ```
5. Create a new `.env` file and set up environment variables 
    ```
    OPENAI_API_KEY: <Your OpenAI API key>
    DISCORD_TOKEN: <Your Discord bot token>
    ```
6. Then, run one of the following command to run the bot
    ```
    $ python bot.py
    $ ./startup.sh
    ```
7. Open your discord and test the bot
   
## Usage

After inviting the bot to your Discord server, use the following commands:

1. **!ask [question]:** Generates a response from OpenAI
2. **!emoji [text]:** Converts text to emojis
3. **!coding [prompt]:** Generates a coding problem
4. **!generate [prompt]:** Creates an image based on the prompt
5. **!speak [prompt]:** Converts the given text into speech
6. **!explain [prompt]:** Generates the text explanation for the given question
