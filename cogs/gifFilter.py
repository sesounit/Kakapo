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
        if message.channel != channel:
            not_allow = message.content
            not_allow_true = re.search("^https://tenor.com/",not_allow)
            not_allow_alternatetrue = re.search("^https.*gif$",not_allow)
            if (not_allow_true or not_allow_alternatetrue):
                await message.delete()

def setup(client):
    client.add_cog(gifFilter(client))