import nextcord, os, sys, random
import nacl
from yt_dlp import YoutubeDL
from nextcord.ext import commands, tasks
from youtubesearchpython.__future__ import *

#Music Related
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
backlog = ['Nada']
backlogtitle = ['Nada']
nextinqueueactive = False
voicestopped = False
guild2 = 'Null'
ydl_opts = {'format': 'bestaudio'}

#Player Extras
class musicExtras():
    def findsongtitle(url):
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            return title
    #Moving the extraction process to this class for some god damn reason made it go far faster.
    def extract(url):
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            title = info['title']
        return URL, title

#musicSystem Cog
class musicSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
    nextinqueueactive = False
    voicestopped = False
    @commands.command(aliases=['np', 'now'])
    async def nowPlaying(self, ctx, url=None, title=None):
        #The Formatting here hyperlinks the URL to the title.
        if url == None:
            if voicestopped == False:
                try:
                    ListEmbed = nextcord.Embed(title="Now Playing:", description=f"[{backlogtitle[1]}]({backlog[1]})", color=0x0000ff)
                    ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
                    await ctx.message.channel.send(embed=ListEmbed)
                except:
                    ListEmbed = nextcord.Embed(title="Now Playing:", description="Nothing", color=0x0000ff)
                    ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
                    await ctx.message.channel.send(embed=ListEmbed)
            else:
                await ctx.send("No music is currently playing.")
        else:
            ListEmbed = nextcord.Embed(title="Now Playing:", description=f"[{title}]({url})", color=0x0000ff)
            ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
            await ctx.message.channel.send(embed=ListEmbed)

    @commands.command(aliases=['lp', 'last'])
    async def lastPlayed(self, ctx):
        #Try-Except for if last played is 'nada'
        try:
            ListEmbed = nextcord.Embed(title="Last Played:", description=f"[{backlogtitle[0]}]({backlog[0]})", color=0x0000ff)
            ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
            await ctx.message.channel.send(embed=ListEmbed)
        except:
            ListEmbed = nextcord.Embed(title="Last Played:", description=backlog[0], color=0x0000ff)
            ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
            await ctx.message.channel.send(embed=ListEmbed)

    @commands.command(aliases=['n'])
    async def next(self, ctx):
        try:
            ListEmbed = nextcord.Embed(title="Next to be Played:", description=f"[{backlogtitle[2]}]({backlog[2]})", color=0x0000ff)
            ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
            await ctx.message.channel.send(embed=ListEmbed)
        except:
            await ctx.send('Nothing in queue.')

    @commands.Cog.listener()
    async def on_ready(self):
        global nextinqueueactive
        nextinqueueactive = True
        await self.nextinqueue.start()
    #Handles Queue
    @tasks.loop(seconds=5)
    async def nextinqueue(self):
        global backlog
        global backlogtitle
        global voicestopped
        global guild2
        voice = nextcord.utils.get(self.client.voice_clients, guild = guild2)
        if voicestopped == False:
            if voice != None and voice.is_playing() != True:
                try:
                    video_link = backlog[2]
                    URL, title = musicExtras.extract(video_link)
                    try:
                        voice.play(nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                        backlog.remove(backlog[0])
                        backlogtitle.remove(backlogtitle[0])
                    except:
                        pass
                    
                except:
                    try:
                        if voice.is_playing() != True:
                            t = backlog[1]
                            backlog.remove(backlog[0])
                            backlogtitle.remove(backlogtitle[0])
                    except:
                        pass
        #if voice != None:
            #if voice.is_playing != True:
                #await self.timeout.start()
    #Supposed to be called when nextinqueue discovers nothing is playing, is never called.
    #@tasks.loop(minutes=25)
    #async def timeout(self):
        #voice = nextcord.utils.get(self.client.voice_clients, guild = guild2)

        #if voice.is_playing == True:
            #await self.timeout.stop()

        #elif voice.is_connected == True:
            #await voice.disconnect

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        global backlog
        global backlogtitle
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                try:
                    voice = nextcord.utils.get(self.client.voice_clients, guild = guild2)
                    voice.stop()
                    backlog2 = []
                    backlogtitle2 = []
                    try:
                        backlog2.append(backlog[1])
                        backlogtitle2.append(backlogtitle[1])
                    except:
                        backlog2 = ['Nada']
                        backlogtitle2 = ['Nada']
                    backlog = backlog2
                    backlogtitle = backlogtitle2
                    await voice.disconnect()
                except:
                    pass

    #Looks weird, probably could be cleaner, but works this way.
    #Also don't touch this part without telling me, it'll probably break if you so much as breathe on it.

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, video_link : str):
        global nextinqueueactive
        if nextinqueueactive == False:
            await ctx.send("Setup Function Called, retry request.")
            nextinqueueactive = True
            await self.nextinqueue.start()
        voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
        global ydl_opts
        global backlog
        global backlogtitle
        global guild2
        global voicestopped
        voicestopped = False
        guild2 = ctx.guild
        voiceChannel = ctx.author.voice.channel

        try:
            if "https://" not in video_link:
                videosSearch = VideosSearch(video_link, limit = 1)
                videosResult = await videosSearch.next()
                video_link = videosResult['result'][0]['link']
        except:
            await ctx.send("A problem occured while trying to search Youtube.")
        try:
            if voice != None:
                if voice.is_playing():
                    URL, title = musicExtras.extract(video_link)
                    ListEmbed = nextcord.Embed(title="Added to Queue", description=f"[{title}]({URL})", color=0x0000ff)
                    ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
                    backlog.append(video_link)
                    backlogtitle.append(title)
                    await ctx.message.channel.send(embed=ListEmbed)

                else:
                    voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
                    URL, title = musicExtras.extract(video_link)
                    voice.play(nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    backlog.append(video_link)
                    backlogtitle.append(title)
                    await ctx.invoke(self.client.get_command('nowPlaying'), url=video_link, title=title)
            else:
                URL, title = musicExtras.extract(video_link)
                await voiceChannel.connect()
                voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
                voice.play(nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                backlog.append(video_link)
                backlogtitle.append(title)
                await ctx.invoke(self.client.get_command('nowPlaying'), url=video_link, title=title)
        except:
            await ctx.send("A problem occured while trying to play.")
    @commands.command()
    async def skip(self, ctx):
        try:
            global voicestopped
            global ydl_opts
            global backlog
            global backlogtitle
            voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
            if voice.is_playing():
                voice.stop()
            videolink = backlog[2]
            URL, title = musicExtras.extract(videolink)
            voice.play(nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            backlog.remove(backlog[0])
            backlogtitle.remove(backlogtitle[0])
            voicestopped = False
            await ctx.invoke(self.client.get_command('nowPlaying'), url=videolink, title=title)
        except:
            await ctx.send("There is nothing in the queue.")

    @commands.command(aliases=['gtfo', 'exit', 'stop', 'disconnect', 'dc'])
    async def leave(self, ctx):
        global backlog
        global backlogtitle
        voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_connected():
            voice.stop
            backlog2 = []
            backlogtitle2 = []
            try:
                backlog2.append(backlog[1])
                backlogtitle2.append(backlogtitle[1])
            except:
                pass
            backlog = backlog2
            backlogtitle = backlogtitle2
            await voice.disconnect()
        else:
            await ctx.send('The bot is not connected to a voice channel.')

    @commands.command()
    async def pause(self, ctx):
        voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            ctx.send('No audio is playing currently.')

    @commands.command(aliases=['unpause'])
    async def resume(self, ctx):
        voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            ctx.send('Audio is not paused.')

    @commands.command(aliases=["Q"])
    async def queue(self, ctx):
        global backlog
        count = 0
        i = 0
        for item in backlog:
            if i > 1:
                count = count + 1
            i = i + 1
        ListEmbed = nextcord.Embed(title="In Queue", description=f"{count} in Queue.", color=0x0000ff)
        ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
        await ctx.message.channel.send(embed=ListEmbed)

    @commands.command(aliases=['clear'])
    async def empty(self, ctx):
        global backlog
        global backlogtitle
        backlog2 = []
        backlogtitle2 = []
        backlog2.append(backlog[0])
        backlog2.append(backlog[1])
        backlogtitle2.append(backlogtitle[0])
        backlogtitle2.append(backlogtitle[1])
        backlog = backlog2
        backlogtitle = backlogtitle2
        await ctx.send("Queue Cleared!")
def setup(client):
    client.add_cog(musicSystem(client))