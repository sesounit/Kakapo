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

    @nextcord.slash_command(name='play',description="Play a song on the bot")
    async def play(self, ctx, search: str = None):
        await ctx.response.defer()
        if search:
            #partial = wavelink.PartialTrack(query=search, cls=wavelink.YouTubeTrack)
            """Play a song with the given search query.

            If not connected, connect to our voice channel.
            """
            if not ctx.guild.voice_client:
                vc: wavelink.Player = await ctx.user.voice.channel.connect(cls=wavelink.Player)
                await ctx.channel.send(f'**Joined `{ctx.user.voice.channel}`**')
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if "https://youtu.be/" in search:
                search = musicHelper.convertShort(search)

            if "/playlist?" in search:
                search = await wavelink.Playable.search(search)
                #if len(search.tracks) > 100:
                    #return await ctx.followup.send("Playlist too large, please limit yourself to playlists smaller than 100.")
                if vc.queue.is_empty and not vc.playing:
                    await vc.play(search.tracks[0])
                    await ctx.followup.send(f'**Now playing:** `{search.tracks[0].title}`')
                    i = 0
                    for track in search.tracks:
                        if i == 101:
                            await ctx.followup.send("Playlist limit reached, only 100 songs have been added from the playlist.")
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
                            await ctx.followup.send("Playlist limit reached, only 100 songs have been added from the playlist.")
                            break
                        await vc.queue.put_wait(track)
                    await ctx.followup.send("Populating queue with playlist.", ephemeral=False)
                    return
            if vc.queue.is_empty and not vc.playing:
                tracks = await wavelink.Playable.search(search)
                if not tracks:
                    await ctx.followup.send(f'No tracks found with query: `{search}`')
                    return
                try:
                    track = tracks[0]
                except:
                    await ctx.followup.send("Unexpected error encountered.")
                    return
                await vc.play(track)
                try:
                    await ctx.followup.send(f'**Now playing:** `{vc.current.title}`', ephemeral=False)
                except:
                    await ctx.followup.send(f'**Now playing:** `Failed to find title`', ephemeral=False)
            else:
                tracks = await wavelink.Playable.search(search)
                if not tracks:
                    await ctx.followup.send(f'No tracks found with query: `{search}`')
                    return
                try:
                    track = tracks[0]
                except:
                    await ctx.followup.send("Unexpected error encountered.")
                    return
                await vc.queue.put_wait(track)
                await ctx.followup.send(f'**Added to Queue:** `{track.title}`', ephemeral=False)

        else:
            vc: wavelink.Player = ctx.guild.voice_client
            await vc.pause(not vc.paused)
            if vc.current == None or vc.current.title == None:
                await ctx.followup.send("Trouble encountered resuming, no title found.")
                return
            await ctx.followup.send(f'**Resumed:** `{vc.current.title}`')
    
    @nextcord.slash_command(name='skip',description="Skip a song")
    async def skip(self, ctx):
        vc: wavelink.Player = ctx.guild.voice_client
        #stop calls on_track_end, so nothing beyond stop is actually needed here.
        queuewasempty = vc.queue.is_empty
        await vc.stop()  
        if queuewasempty:
            await ctx.response.send_message("Queue is empty.")
        else:
            await ctx.channel.send(f'**Skipped!**')
            await self.np(ctx)
        


    @nextcord.slash_command(name='pause',description="Pause the current song")
    async def pause(self, ctx):
        vc: wavelink.Player = ctx.guild.voice_client
        await vc.pause(not vc.paused)
        await ctx.response.send_message("Audio paused!")

    @nextcord.slash_command(name='stop',description="Stop the bot playing entirely, this will clear the queue")
    async def stop(self, ctx):
        vc: wavelink.Player = ctx.guild.voice_client
        if not vc.queue.is_empty:
            vc.queue.clear()
        await vc.stop()
        await ctx.response.send_message("Music stopped!")

    @nextcord.slash_command(name='clear',description="Clear the queued songs")
    async def clear(self, ctx):
        vc: wavelink.Player = ctx.guild.voice_client
        vc.queue.clear()
        await ctx.response.send_message("**Queue Cleared**", ephemeral=False)

    @nextcord.slash_command(name='dc',description="Disconnect from the voice channel, this will clear the queue")
    async def disconnect(self, ctx):
        vc: wavelink.Player = ctx.guild.voice_client
        if not vc.queue.is_empty:
            vc.queue.clear()
        await vc.disconnect()
        await ctx.response.send_message("Disconnected!")

    @nextcord.slash_command(name='volume',description="Set the volume of the bot")
    async def volume(self, ctx, volume: int):
        volume = int(volume)
        vc: wavelink.Player = ctx.guild.voice_client
        if volume > 100:
            #Do not let people set the volume beyond 100, for the love of god.
            await ctx.response.send_message("Volumes above 100 are not permitted.")
            return
        await vc.set_volume(volume)
        await ctx.response.send_message(f"Volume set to {volume}")

    
    @nextcord.slash_command(name='np',description="Shows what's currently playing")
    async def np(self, ctx):
        vc: wavelink.Player = ctx.guild.voice_client
        if vc == None:
            await ctx.response.send_message("Nothing is currently playing!")
            return
        #is_playing doesn't seem to work here, no clue why.
        try:
            test = vc.current.title
        except:
            await ctx.response.send_message("Nothing is currently playing!")
            return
        await ctx.response.defer()
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
            upcoming = vc.queue.peek()
            upcomingt = upcoming.title
            upcomingu = upcoming.uri
            fmt = f"\n__Now Playing__:\n[{vc.current.title}]({vc.current.uri})\n`{songposition}/{length}`\n__Up Next:__\n" + f"[{upcomingt}]({upcomingu})" + f"\n**{vc.queue.count} song(s) in queue**"
        else:
            fmt = f"\n__Now Playing__:\n[{vc.current.title}]({vc.current.uri})\n`{songposition}/{length}`\n__Up Next:__\n" + "Nothing" + f"\n**{vc.queue.count} song(s) in queue**"
        embed = nextcord.Embed(title=f'Currently Playing in {ctx.guild.name}', description=fmt, color=nextcord.Color.green())
        embed.set_footer(text=f"{ctx.user.display_name}", icon_url=ctx.user.avatar.url)
        await ctx.followup.send(embed=embed)

    @nextcord.slash_command(name='queue',description="Displays the current queue")
    async def queue(self, ctx):
        vc: wavelink.Player = ctx.guild.voice_client
        if vc == None:
            await ctx.response.send_message("No channel is connected.")
            return
        if vc.queue.is_empty:
            await ctx.response.send_message("Nothing is queued!")
            return
        await ctx.response.defer()
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
        await ctx.followup.send(embed=ListEmbed)



def setup(client):
    client.add_cog(Music(client))