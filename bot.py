# bot.py
import discord, os, sys, random
from dotenv import load_dotenv
import nacl
import youtube_dl
from discord.ext import commands, tasks
intents = discord.Intents.default()
intents.members = True
# is a .env file inside the folder to leave the token for the bot outside the git
load_dotenv()

# Debug Helpers
def developer_only(ctx):
    if ctx.message.author.id == 267469338557153300 or ctx.message.author.id == 68019210814500864 or ctx.message.author.id == 337739057545347072:
        return True
    else:
        False

# bot commands have prefix ! so all messages start with ! will trigger the bot commands
client = commands.Bot(command_prefix='!', intents=intents, help_command = None)

# when the bot is initialized it will print has connected to the terminal
@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")

#Cogs Loader
@client.command()
async def load(ctx, extension):
    if developer_only(ctx):
        client.load_extension(f'cogs.{extension}')
        print(f"Successfully loaded cogs.{extension}")
    else:
        print("Caller is not a developer")

@client.command()
async def unload(ctx, extension):
    if developer_only(ctx):
        client.unload_extension(f'cogs.{extension}')
        print(f"Successfully unloaded cogs.{extension}")
    else:
        print("Caller is not a developer")

@client.command()
async def reload(ctx, extension):
    if developer_only(ctx):
        client.reload_extension(f'cogs.{extension}')
        print(f"Successfully reloaded cogs.{extension}")
    else:
        print("Caller is not a developer")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Not at all necessary, but I like a version notes command, and the one I've used in the past looks nice.
@client.command(name='version')
async def version(context):

    mainEmbed = discord.Embed(title="Kakapo Version Notes", description="SESO's Multi-Use Discord Bot", color=0x0E8643)
    mainEmbed.add_field(name="Changes:", value="Gif filter added, role reaction system actually ready")
    mainEmbed.add_field(name="Version Code:", value="v0.8.0", inline=False)
    mainEmbed.add_field(name="Date Released:", value="October 6, 2021", inline=False)
    mainEmbed.set_footer(text="Kakapo written by Pickle423#0408, Fletch#0617, Dildo Sagbag#8107.")

    await context.message.channel.send(embed=mainEmbed)

#Kill Bot
@client.command()
async def kill(ctx):
    if developer_only(ctx):
        await ctx.send('Bot Terminated')
        sys.exit()
    else:
        await ctx.send('You do not have the authority to kill the bot.')

#Simple Ping Check
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

client.run(os.getenv("discord_token"))