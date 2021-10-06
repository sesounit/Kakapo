import discord
import re
from discord.ext import commands
#welcomeMessage Cog
class gifFilter(commands.Cog):
    def _init_(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        channel = discord.utils.get(message.guild.text_channels, name="voice-chat")
        channel2 = discord.utils.get(message.guild.text_channels, name="nsfw-memes-no-porn")
        channel3 = discord.utils.get(message.guild.text_channels, name="bot-commands")
        if message.channel != channel and message.channel != channel2 and message.channel != channel3:
            not_allow = message.content
            if "https://tenor.com" in not_allow or ".gif" in not_allow:
                await message.delete()

def setup(client):
    client.add_cog(gifFilter(client))
