# bot.py
import nextcord, os, sys, random, logging
from dotenv import load_dotenv
import nacl
from nextcord.ext import commands, tasks
intents = nextcord.Intents.default()
intents.members = True
# is a .env file inside the folder to leave the token for the bot outside the git
load_dotenv()

# Debug Helpers
## bool useful for developer-only commands
def developer_only(ctx):
    if ctx.message.author.id == 267469338557153300 or ctx.message.author.id == 68019210814500864 or ctx.message.author.id == 337739057545347072:
        return True
    else:
        False
## Logging
logging.basicConfig(level=logging.INFO)

# bot commands have prefix ! so all messages start with ! will trigger the bot commands
client = commands.Bot(command_prefix='!', intents=intents, help_command = None, case_insensitive=True)

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
        if extension == "all" or extension == "All":
            for filename in os.listdir('./cogs'):
                try:
                    if filename.endswith('.py'):
                        client.reload_extension(f'cogs.{filename[:-3]}')
                        print(f"Successfully reloaded cogs.{filename[:-3]}")
                except:
                    print(f"WARNING: Failed to load cogs.{filename[:-3]}")
            print("Reload complete.")    
        else:
            client.reload_extension(f'cogs.{extension}')
            print(f"Successfully reloaded cogs.{extension}")
    else:
        print("Caller is not a developer")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
        except:
            print(f"WARNING: Failed to load cogs.{filename[:-3]}")

#Kill Bot
@client.command()
async def kill(ctx):
    if developer_only(ctx):
        await ctx.send('Bot Terminated')
        sys.exit()
    else:
        await ctx.send('You do not have the authority to kill the bot.')

client.run(os.getenv("discord_token"))