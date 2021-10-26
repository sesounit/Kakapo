import nextcord, requests, aiohttp
from nextcord.ext import commands

class shiba(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['dog', 'doge', 'dogeg','shibainu', 'shib', 'shub','shobe','shuber','shober'])
    async def shiba(self,ctx):

        async with aiohttp.ClientSession() as session:
            async with session.get("http://shibe.online/api/shibes") as shiba_url :
                if shiba_url.status == 200:
                    shiba_pic = await shiba_url.json()
                    await ctx.send(shiba_pic[0])

def setup(client):
    client.add_cog(shiba(client))
