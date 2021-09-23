# bot.py
import discord, os
from dotenv import load_dotenv
from discord.ext import commands

# is a .env file inside the folder to leave the token for the bot outside the git
load_dotenv()

# bot commands have prefix ! so all messages start with ! will trigger the bot commands
client = commands.Bot(command_prefix='!')

# when the bot is initialized it will print a has connected to the terminal
@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")

client.run(os.getenv("discord_token"))