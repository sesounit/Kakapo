import wavelink
from nextcord.ext import commands

class Music(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""

    #def __init__(self, bot: commands.Bot):
    #    self.bot = bot
    def __init__(self, client: commands.Bot):
        self.client = client

        #self.title = data.get('title')
        #self.web_url = data.get('webpage_url')
        #self.duration = data.get('duration')

        client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.client.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.client,
                                            host='0.0.0.0',
                                            port=2333,
                                            password="yoyoyo, it's me! mario!")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')

    @commands.command(aliases=['continue','resume','re','res'])
    async def play(self, ctx: commands.Context, search: wavelink.YouTubeTrack):
        if search:
            #partial = wavelink.PartialTrack(query=search, cls=wavelink.YouTubeTrack)
            """Play a song with the given search query.

            If not connected, connect to our voice channel.
            """
            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
                await ctx.send(f'**Joined `{ctx.author.voice.channel}`**')
            else:
                vc: wavelink.Player = ctx.voice_client

            await vc.play(search)
        else:
            await wavelink.Player.resume()
        await ctx.message.add_reaction('▶️')
        await ctx.send(f'**Now playing:** `{vc.track.title}`')


    @commands.command(aliases=['ps'])
    async def pause(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.pause()
        await ctx.message.add_reaction('⏸️')

    @commands.command()
    async def stop(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.stop()
        await ctx.message.add_reaction('⏹️')

    @commands.command(aliases=['dis', 'fukoff', 'fukof', 'fuckoff'])
    async def disconnect(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()
        await ctx.message.add_reaction('⏏️')

    @commands.command(aliases=['vol', 'v'])
    async def volume(self, ctx: commands.Context, volume):
        volume = int(volume)
        vc: wavelink.Player = ctx.voice_client
        await vc.set_volume(int(volume))
        if volume == 0:
            await ctx.message.add_reaction('🔇')
        if volume >= 0 and volume < 50:
            await ctx.message.add_reaction('🔈')
        elif volume >= 50 and volume < 70:
            await ctx.message.add_reaction('🔉')
        elif volume >= 70 and volume <= 100:
            await ctx.message.add_reaction('🔊')
        else:
            await ctx.message.add_reaction('❓')

    
    #@commands.command()
    #async def np(self, ctx: commands.Context):
    #    upcoming = list(itertools.islice(player.queue._queue, 0, int(len(player.queue._queue))))
    #    fmt = '\n'.join(f"`{(upcoming.index(_)) + 1}.` [{_['title']}]({_['webpage_url']}) | ` {duration} Requested by: {_['requester']}`\n" for _ in upcoming)
    #    fmt = f"\n__Now Playing__:\n[{vc.source.title}]({vc.source.web_url}) | ` {duration} Requested by: {vc.source.requester}`\n\n__Up Next:__\n" + fmt + f"\n**{len(upcoming)} songs in queue**"
    #    embed = nextcord.Embed(title=f'Queue for {ctx.guild.name}', description=fmt, color=nextcord.Color.green())
    #    embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)
#
    #    await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Music(client))