import nextcord, requests
from itertools import cycle
from nextcord.ext import commands, tasks
from nextcord.ext import commands
status = cycle(['Arma 3', 'Minecraft', 'Left For Dead 2', 'Jackbox Party Pack', 'Among Us', 'Phasmophobia', 'Joe Rogan'])

class statusChange(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Status Changin'
    @tasks.loop(hours=2)
    async def change_status(self):
        await self.client.change_presence(activity=nextcord.Game(next(status)))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        await self.change_status.start()
    
def setup(client):
    client.add_cog(statusChange(client))
