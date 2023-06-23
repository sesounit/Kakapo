import nextcord, requests, aiohttp, json
from nextcord.ext import commands, tasks

class server():
    async def pingServer():
        async with aiohttp.ClientSession() as session:
                async with session.get("https://api.mcsrvstat.us/2/sesounit.org") as request :
                    if request.status == 200:
                        response_info = await request.json()
                        try:
                            serverc = response_info['players']['online']
                            serverm = response_info['players']['max']
                        except:
                            serverc = 0
                            serverm = 16
                            serverl = 'Server is currently offline, checkback later.'
                            return serverc, serverm, serverl
                        try:
                            serverl = response_info['players']['list']
                            return serverc, serverm, serverl
                        except:
                            serverl = 'There is no one online, you can change that!'
                            return serverc, serverm, serverl

#minecraftStatus Cog
class minecraftStatus(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.change_status.start()

    @tasks.loop(minutes=10)
    async def change_status(self):
        serverc, serverm, serverl = await server.pingServer()
        await self.client.change_presence(activity=nextcord.Game(f"Pickloniancraft with {serverc}/{serverm}"))

    @commands.command(aliases=['status','serverstatus', 'players', 'online'])
    async def server(self, ctx):
        serverc, serverm, serverl = await server.pingServer()
        statusEmbed = nextcord.Embed(title="Server Status", description=f"Pickloniancraft's Population is currently {serverc}/{serverm}", color=0x00ff00)
        statusEmbed.add_field(name="Players:", value=serverl, inline=False)
        statusEmbed.set_footer(text="Kakapo Minecraft Functionality by Pickle423#0408")
        await ctx.send(embed=statusEmbed)


def setup(client):
    client.add_cog(minecraftStatus(client))