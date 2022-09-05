import nextcord, random
from nextcord.ext import commands, tasks
from nextcord.ext import commands
status = ['Arma 3', 'Minecraft', 'Left 4 Dead 2', 'Jackbox Party Pack', 'Metal Gear Solid V', 'Phasmophobia', 'Counter-Strike: Global Offensive', 'Garry\'s Mod', 'Barotrauma']

class statusChange(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Status Changin'
    @tasks.loop(hours=2)
    async def change_status(self):
        await self.client.change_presence(activity=nextcord.Game(random.choice(status)))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.change_status.start()
    
def setup(client):
    client.add_cog(statusChange(client))
