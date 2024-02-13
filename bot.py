import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file
BOT_API = os.getenv('DISCORD_TOKEN')

# Define the required intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Initialize the bot with the specified intents and command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to keep track of timers
timers = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='settimer')
async def settimer(ctx, seconds: int):
    if seconds <= 0:
        await ctx.send("Please enter a number of seconds greater than 0.")
        return
    
    end_time = datetime.now() + timedelta(seconds=seconds)
    timers[ctx.author.id] = end_time
    
    await ctx.send(f"Timer set for {seconds} seconds.")
    
    # Wait for the timer to finish
    await asyncio.sleep(seconds)
    
    # Check if the timer wasn't deleted (e.g., by the !timer command)
    if ctx.author.id in timers:
        await ctx.send(f"{ctx.author.mention} Your timer has ended!")
        del timers[ctx.author.id]  # Remove the timer

@settimer.error
async def settimer_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to specify the number of seconds for the timer.")


@bot.command(name='timer')
async def timer(ctx):
    if ctx.author.id not in timers:
        await ctx.send("You don't have an active timer.")
    else:
        remaining_time = timers[ctx.author.id] - datetime.now()
        seconds = int(remaining_time.total_seconds())
        if seconds > 0:
            await ctx.send(f"{ctx.author.mention} Your timer has {seconds} seconds remaining.")
        else:
            await ctx.send(f"{ctx.author.mention} Your timer has ended!")
            del timers[ctx.author.id]  # Remove the timer

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run(BOT_API)