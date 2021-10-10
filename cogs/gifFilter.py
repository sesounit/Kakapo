import discord
import re
from discord.ext import commands
#gifFilter Cog
class gifFilter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        exception_channels = [discord.utils.get(message.guild.text_channels, name="voice-chat"),discord.utils.get(message.guild.text_channels, name="nsfw-memes-no-porn"),discord.utils.get(message.guild.text_channels, name="bot-commands")]
        if message.channel not in exception_channels:
            not_allow = message.content
            if "https://tenor.com" in not_allow or "https://media.tenor.co" in not_allow or "https://c.tenor.com" in not_allow:
                await message.delete()

def setup(client):
    client.add_cog(gifFilter(client))
