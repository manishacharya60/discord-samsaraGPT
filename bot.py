import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import os

# Remove the dotenv import and load_dotenv call, as environment variables will be used directly in Azure

BOT_API = os.getenv('DISCORD_TOKEN')

# Define the required intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Ensure this is enabled in the Discord Developer Portal as well

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
    bot.loop.create_task(wait_for_timer(seconds, ctx.author.id))

async def wait_for_timer(seconds, author_id):
    await asyncio.sleep(seconds)
    if author_id in timers:
        channel = bot.get_channel(timers[author_id]['channel'])
        await channel.send(f"<@{author_id}>, your timer has ended!")
        del timers[author_id]

@bot.command(name='timer')
async def timer(ctx):
    if ctx.author.id not in timers:
        await ctx.send("You don't have an active timer.")
    else:
        remaining_time = timers[ctx.author.id]['end_time'] - datetime.now()
        seconds = int(remaining_time.total_seconds())
        if seconds > 0:
            await ctx.send(f"{ctx.author.mention} Your timer has {seconds} seconds remaining.")
        else:
            await ctx.send(f"{ctx.author.mention} Your timer has ended!")
            del timers[ctx.author.id]  # Remove the timer

# Handle errors globally to prevent bot from crashing
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"An error occurred: {str(error)}")
    else:
        print(f"An error occurred: {str(error)}")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token is no longer necessary as it is set above
bot.run(BOT_API)
