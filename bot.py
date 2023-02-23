# bot.py
import nextcord, os, logging
from dotenv import load_dotenv
from nextcord.ext import commands, tasks
# is a .env file inside the folder to leave the token for the bot outside the git
load_dotenv()

# Debug Helpers
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

debug = bool(os.getenv('DEBUG'))
if debug:
    print('Setting DEBUG log level')
    logger.setLevel(logging.debug)

# Setup intents
intents = nextcord.Intents.default()
intents.guilds = True
intents.message_content = True
intents.reactions = True
intents.members = True

# bot commands have prefix ! so all messages start with ! will trigger the bot commands
client = commands.Bot(command_prefix='!', intents=intents, help_command = None, case_insensitive=True)

# when the bot is initialized it will print has connected to the terminal
@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")

#Cogs Loader
@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(f"Successfully loaded cogs.{extension}")

@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
        client.unload_extension(f'cogs.{extension}')
        print(f"Successfully unloaded cogs.{extension}")

@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
        if extension.lower() == "all":
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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if "ignore" in filename:
            pass
        else:
            try:
                client.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print(f"""WARNING: Failed to load cogs.{filename[:-3]}. Error is defined below:\n{e}""")

client.run(os.getenv("discord_token"))