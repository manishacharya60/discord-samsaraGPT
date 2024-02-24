import os
import discord
from openai import OpenAI
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
import os

# Your OpenAI API key goes here

# Your Discord bot token goes here
DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')

# Intents are required to receive messages from the guild
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure message content intent is enabled in your bot's settings on Discord Developer Portal

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def ask(ctx, *, question):
    try:
        # Call the OpenAI API
        response = client.chat.completions.create(model="gpt-4",  # Change to the model you are using
        messages=[
            {"role": "system", "content": "You are a helpful assistant who helps to understand mathematical and computer concepts in easier ways through real life examples and applications."},
            {"role": "user", "content": question},
        ])
        message = response.choices[0].message.content
        
        # Send the response back to the Discord channel
        await ctx.send(message)
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')

@bot.command()
async def generate(ctx, *, prompt):
    try:
        # Generate an image with DALL·E
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            quality="standard",
            size="1024x1024"
        )
        # Assuming 'response' contains a URL to the generated image
        image_url = response.data[0].url
        embed = discord.Embed(title="Generated Image")
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f'An error occurred: {str(e)}')

# Run the Discord bot
bot.run(DISCORD_BOT_TOKEN)
