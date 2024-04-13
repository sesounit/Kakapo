import nextcord, wavelink, datetime, time
from nextcord.ext import commands, tasks

class musicHelper:

    # Convert a youtu.be link into a youtube.com link by splitting the original youtu.be link on slashes, 
    # and then on ? to isolate the video id before putting it back into a youtube.com link.
    def convertShort(search):
        return (f"https://www.youtube.com/watch?v={search.split('/')[3].split('?')[0]}")

autodisconnect = {}
class Music(commands.Cog):
    """Music cog to hold wavelink related commands and listeners."""

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

        nodes = [wavelink.Node(uri='http://localhost:2333', password="yoyoyo, it's me! mario!")]
        # cache_capacity is EXPERIMENTAL. Turn it off by passing None
        await wavelink.Pool.connect(nodes=nodes, client=self.client, cache_capacity=None)
        wavelink.Player.autoplay = wavelink.AutoPlayMode.disabled

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.node.identifier}> is ready!')

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track=None, reason=None):
        player = player.player
        if not player.queue.is_empty:
            next = player.queue.get()
            await player.play(next)
            return
        else:
            p = player
            ms = datetime.datetime.now()
            autodisconnect[p] = (time.mktime(ms.timetuple()) * 1000)
            try:
                await self.timeout.start()
            except:
                pass
            return

    #Disconnects after 10 minutes of activity. 600000 = 10 Minutes
    @tasks.loop(minutes=1)
    async def timeout(self):
        ms = datetime.datetime.now()
        for p in list(autodisconnect):
            if not p.playing and (((time.mktime(ms.timetuple()) * 1000) - autodisconnect[p]) > 600000):
                del autodisconnect[p]
                await p.disconnect()
            elif p.playing or not p.queue.is_empty:
                del autodisconnect[p]

    @commands.command(aliases=['continue','resume','re','res', 'p'])
    async def play(self, ctx: commands.Context, *, search: str = None):
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

            if "https://youtu.be/" in search:
                search = musicHelper.convertShort(search)

            if "playlist" in search:
                search = await wavelink.Playable.search(search)
                #if len(search.tracks) > 100:
                    #return await ctx.send("Playlist too large, please limit yourself to playlists smaller than 100.")
                if vc.queue.is_empty and not vc.playing:
                    await vc.play(search.tracks[0])
                    await ctx.message.add_reaction('▶️')
                    await ctx.send(f'**Now playing:** `{search.tracks[0].title}`')
                    i = 0
                    for track in search.tracks:
                        if i == 101:
                            await ctx.send("Playlist limit reached, only 100 songs have been added from the playlist.")
                            break
                        if track == search.tracks[0]:
                            continue
                        await vc.queue.put_wait(track)
                        i += 1
                    return
                else:
                    i = 0
                    for track in search.tracks:
                        if i == 101:
                            await ctx.send("Playlist limit reached, only 100 songs have been added from the playlist.")
                            break
                        await vc.queue.put_wait(track)
                    await ctx.send("Populating queue with playlist.")
                    return
            if vc.queue.is_empty and not vc.playing:
                tracks = await wavelink.Playable.search(search)
                if not tracks:
                    await ctx.send(f'No tracks found with query: `{search}`')
                    return
                try:
                    track = tracks[0]
                except:
                    await ctx.send("Unexpected error encountered.")
                    return
                await vc.play(track)
                await ctx.message.add_reaction('▶️')
                try:
                    await ctx.send(f'**Now playing:** `{vc.current.title}`')
                except:
                    await ctx.send(f'**Now playing:** `Failed to find title`')
            else:
                tracks = await wavelink.Playable.search(search)
                if not tracks:
                    await ctx.send(f'No tracks found with query: `{search}`')
                    return
                try:
                    track = tracks[0]
                except:
                    await ctx.send("Unexpected error encountered.")
                    return
                await vc.queue.put_wait(track)
                await ctx.message.add_reaction('▶️')
                await ctx.send(f'**Added to Queue:** `{track.title}`')

        else:
            vc: wavelink.Player = ctx.voice_client
            await vc.pause(not vc.paused)
            await ctx.message.add_reaction('▶️')
            await ctx.send(f'**Resumed:** `{vc.current.title}`')
    
    @commands.command()
    async def skip(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        #stop calls on_track_end, so nothing beyond stop is actually needed here.
        await vc.stop()
        if not vc.queue.is_empty:
            await ctx.send(f'**Skipped!**')
            await ctx.invoke(self.client.get_command('np'))
        else:
            await ctx.send("Queue is empty.")


    @commands.command(aliases=['ps', 'unpause'])
    async def pause(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.pause(not vc.paused)
        await ctx.message.add_reaction('⏸️')

    @commands.command()
    async def stop(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        if not vc.queue.is_empty:
            vc.queue.clear()
        await vc.stop()
        await ctx.message.add_reaction('⏹️')

    @commands.command()
    async def clear(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        vc.queue.clear()
        await ctx.send("**Queue Cleared**")

    @commands.command(aliases=['dis', 'fukoff', 'fukof', 'fuckoff', 'dc'])
    async def disconnect(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        if not vc.queue.is_empty:
            vc.queue.clear()
        await vc.disconnect()
        await ctx.message.add_reaction('⏏️')

    @commands.command(aliases=['vol', 'v'])
    async def volume(self, ctx: commands.Context, volume):
        volume = int(volume)
        vc: wavelink.Player = ctx.voice_client
        if volume == 0:
            await ctx.message.add_reaction('🔇')
        elif volume >= 0 and volume < 50:
            await ctx.message.add_reaction('🔈')
        elif volume >= 50 and volume < 70:
            await ctx.message.add_reaction('🔉')
        elif volume >= 70 and volume <= 100:
            await ctx.message.add_reaction('🔊')
        else:
            #Do not let people set the volume beyond 100, for the love of god.
            await ctx.message.add_reaction('❓')
            return
        await vc.set_volume(volume)

    
    @commands.command(aliases=["next", 'n', 'nowplaying'])
    async def np(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        if vc == None:
            await ctx.send("Nothing is currently playing!")
            return
        #is_playing doesn't seem to work here, no clue why.
        try:
            test = vc.current.title
        except:
            await ctx.send("Nothing is currently playing!")
            return
        
        seconds = vc.current.length
        seconds = seconds / 1000
        m, s = divmod(seconds, 60)
        m = int(m)
        s = int(s)
        secondspassed = vc.position
        secondspassed = secondspassed / 1000
        mp, sp = divmod(secondspassed, 60)
        mp = int(mp)
        sp = int(sp)
        if s < 10:
            length = ("{0}:0{1}".format(m, s))
        else:
            length = ("{0}:{1}".format(m, s))
        if sp < 10:
            songposition = ("{0}:0{1}".format(mp, sp))
        else:
            songposition = ("{0}:{1}".format(mp, sp))
        if not vc.queue.is_empty:
            upcoming = vc.queue.get()
            #vc.queue.get tells the queue to remove what it just got from the queue, the next line puts it back in.
            vc.queue.put_at_front(upcoming)
            upcomingt = upcoming.title
            upcomingu = upcoming.uri
            fmt = f"\n__Now Playing__:\n[{vc.current.title}]({vc.current.uri})\n`{songposition}/{length}`\n__Up Next:__\n" + f"[{upcomingt}]({upcomingu})" + f"\n**{vc.queue.count} song(s) in queue**"
        else:
            fmt = f"\n__Now Playing__:\n[{vc.current.title}]({vc.current.uri})\n`{songposition}/{length}`\n__Up Next:__\n" + "Nothing" + f"\n**{vc.queue.count} song(s) in queue**"
        embed = nextcord.Embed(title=f'Currently Playing in {ctx.guild.name}', description=fmt, color=nextcord.Color.green())
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['upcoming', 'coming', 'q'])
    async def queue(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        if vc == None:
            await ctx.send("No channel is connected.")
        if vc.queue.is_empty:
            await ctx.send("Nothing is queued!")
            return
        queuetitle = []
        queueurl = []
        for track in vc.queue:
            tracktitle = track.title
            queuetitle.append(tracktitle)
            queueurl.append(track.uri)
        i = 0
        queue = f"0) [{queuetitle[0]}]({queueurl[0]})"
        for song in queuetitle:
            if i > 10:
                queue = (queue + f"\n**Queue has {len(queuetitle) - 10} more tracks in queue.**")
                break
            if i > 0 and i < 11:
                queue = (queue + f"\n{i}) [{song}]({queueurl[i]})")
            i = i + 1
        ListEmbed = nextcord.Embed(title=f"Queue for {ctx.guild.name}", description=queue, color=nextcord.Color.green())
        ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
        await ctx.message.channel.send(embed=ListEmbed)



def setup(client):
    client.add_cog(Music(client))