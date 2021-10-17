import discord, requests
from discord.ext import commands

class shiba(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['dog', 'doge', 'dogeg','shibainu'])
    async def shiba(self,ctx):
        #Get shiba picture
        shiba_url = requests.get("http://shibe.online/api/shibes").json()

        #Create embed and assigned Shiba picture to it
        shiba_embed = discord.Embed()
        shiba_embed.set_image(url=shiba_url[0])

        #Send embedded shiba picture
        await ctx.send(embed=shiba_embed)

def setup(client):
    client.add_cog(shiba(client))
