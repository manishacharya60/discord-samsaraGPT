import os
import discord
import asyncio
from pathlib import Path
from openai import OpenAI
from discord.ext import commands
from dotenv import load_dotenv

# Constants
MAX_LENGTH = 2000  # Discord's max message length

load_dotenv()

# Your OpenAI API key goes here
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Your Discord bot token goes here
DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')

# Intents are required to receive messages from the guild
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure message content intent is enabled in your bot on Discord Developer Portal

bot = commands.Bot(command_prefix='!', intents=intents)

def truncate_message(message):
    if len(message) > MAX_LENGTH:
        return message[:MAX_LENGTH - 3] + "..."  # Truncate and add ellipsis
    return message

# Split the message into chunks of 2000 characters
def split_message(message, chunk_size=2000):
    return [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]

# Paginate the message and add reactions to navigate through the pages
async def paginate_message(ctx, message, chunk_size=1900):
    """
    Sends a paginated message and adds reactions to navigate through the pages.
    Each page is up to `chunk_size` characters long.
    """
    # Split the message into chunks
    chunks = [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

    current_page = 0
    total_pages = len(chunks)
    
    # Send the first chunk to the channel
    msg = await ctx.send(f"Page {current_page+1}/{total_pages}\n\n{chunks[current_page]}")
    
    # Don't add reactions if there's only one page
    if total_pages <= 1:
        return

    # Add reaction controls
    await msg.add_reaction("⬅️")
    await msg.add_reaction("➡️")

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0*30.0, check=check)
            
            if str(reaction.emoji) == "➡️" and current_page < total_pages - 1:
                current_page += 1
                await msg.edit(content=f"Page {current_page+1}/{total_pages}\n\n{chunks[current_page]}")
                await msg.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "⬅️" and current_page > 0:
                current_page -= 1
                await msg.edit(content=f"Page {current_page+1}/{total_pages}\n\n{chunks[current_page]}")
                await msg.remove_reaction(reaction, user)
            else:
                await msg.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            break

# Fetch a response from the OpenAI API
async def fetch_response_from_openai(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who helps to understand mathematical and computer concepts in easier ways through real life examples and applications."},
                {"role": "user", "content": question},
            ])
        full_message = response.choices[0].message.content
        return full_message
    except Exception as e:
        return f'An error occurred: {e}'

# Event listener for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Define a command to ask questions
@bot.command()
async def ask(ctx, *, question):
    temp_message = await ctx.send('🔄 Processing your request...')
    response_text = await fetch_response_from_openai(question)
    await temp_message.edit(content='Here is the information you requested:')
    await paginate_message(ctx, response_text)

# Define a command to generate emoji for the text
@bot.command()
async def emoji(ctx, *, question):
    temp_message = await ctx.send('🔄 Processing your request...')
    try:
        # Call the OpenAI API
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Change to the model you are using
        messages=[
            {"role": "system", "content": "You convert the text into emojis. Please avoid using regular texts. Strictly try to use emojis only."},
            {"role": "user", "content": question},
        ])
        full_message = response.choices[0].message.content

        await temp_message.edit(content=full_message)
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')

# Define a command to generate a coding interview question
@bot.command()
async def coding(ctx, *, question):
    temp_message = await ctx.send('🔄 Processing your request...')
    try:
        # Call the OpenAI API
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Change to the model you are using
        messages=[
            {"role": "system", "content": "Generate a coding interview question with a randomly selected difficulty level (easy, medium, or hard). The question should be suitable for a coding interview at top tech companies like Google, Facebook, Amazon, Microsoft, etc. Include the following details in your response, each clearly separated:\n1. **Difficulty Level:** Specify whether the question is easy, medium, or hard.\n2. **Question:** Provide the coding interview question. \n3. **Examples:** Include example inputs and outputs to illustrate how the problem and solution work. \n4. **Solution:** Give a detailed solution to the problem. \n5. **Explanation:** Provide an explanation of how the solution works. \n6. **Time Complexity:** Analyze the time complexity of the solution. \n7. **Space Complexity:** Analyze the space complexity of the solution. \nUse this clear separator (`**`) for each section without deviation. Your response should strictly adhere to this formatting guideline to ensure clarity and consistency."},
            {"role": "user", "content": question},
        
        ])

        print(response)
        full_message = response.choices[0].message.content

        await temp_message.edit(content=full_message)
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')

# Define a command to convert the text to speech
@bot.command(name='speak', help='Converts text to speech using OpenAI TTS model.')
async def speak(ctx, *, text: str):
    # Define the path for the temporary speech file
    speech_file_path = Path(__file__).parent / "speech.mp3"
    
    try:
        # Use OpenAI's TTS model to generate speech from the provided text
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        
        # Stream the generated audio to a file
        response.stream_to_file(str(speech_file_path))
        
        # Send the generated audio file in response
        await ctx.send(file=discord.File(speech_file_path))
        
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        
    finally:
        # Clean up by removing the temporary speech file after sending
        if speech_file_path.exists():
            speech_file_path.unlink()

# Define a command to return the explanation of the given question
@bot.command(name='explain', help='Converts text to speech using OpenAI TTS model.')
async def explain(ctx, *, text: str):
    # Define the path for the temporary speech file
    speech_file_path = Path(__file__).parent / "speech.mp3"
    
    try:
        reading_message = await fetch_response_from_openai(text)
        # Use OpenAI's TTS model to generate speech from the provided text
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=reading_message
        )
        
        # Stream the generated audio to a file
        response.stream_to_file(str(speech_file_path))
        
        # Send the generated audio file in response
        await ctx.send(file=discord.File(speech_file_path))
        
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        
    finally:
        # Clean up by removing the temporary speech file after sending
        if speech_file_path.exists():
            speech_file_path.unlink()

# Define a command to generate an image with DALL·E
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
