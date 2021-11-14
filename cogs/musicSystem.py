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
    @commands.command(aliases=['np'])
    async def nowPlaying(self, ctx, url=None, title=None):
        #This is pretty confusing, but basically it's meant to hyperlink.
        if url == None:
            try:
                ListEmbed = nextcord.Embed(title="Now Playing:", description=f"[{backlogtitle[1]}]({backlog[1]})", color=0x0000ff)
                ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
                await ctx.message.channel.send(embed=ListEmbed)
            except:
                ListEmbed = nextcord.Embed(title="Now Playing:", description="Nothing", color=0x0000ff)
                ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
                await ctx.message.channel.send(embed=ListEmbed)
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
    #This has some debugging phrases that print to the console. Not really necessary anymore, but would be helpful if something were to go wrong.
    @tasks.loop(seconds=5)
    async def nextinqueue(self):
        global ydl_opts
        global guild2
        global backlog
        global backlogtitle
        global voicestopped
        voice = nextcord.utils.get(self.client.voice_clients, guild = guild2)
        if voicestopped == False:
            if voice != None and not voice.is_playing():
                try:
                    video_link = backlog[2]
                    URL = musicExtras.extract(video_link)
                    voice.play(nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    backlog.remove(backlog[0])
                    backlog.remove(backlogtitle[0])
                except:
                    pass
        if voice != None:
            if voice.is_playing != True:
                await self.timeout.start()

    @tasks.loop(minutes=25)
    async def timeout(self):
        voice = nextcord.utils.get(self.client.voice_clients, guild = guild2)

        if voice.is_playing == True:
            await self.timeout.stop()

        elif voice.is_connected == True:
            await voice.disconnect

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

    @commands.command(aliases=['gtfo', 'exit'])
    async def leave(self, ctx):
        voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_connected():
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

    @commands.command()
    async def stop(self, ctx):
        global backlog
        global backlogtitle
        voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
        voice.stop()
        global voicestopped
        voicestopped = True
        backlog.remove(backlog[0])
        backlogtitle.remove(backlogtitle[0])

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
        i = 0
        for item in backlog:
            if i > 0:
                backlog.remove(item)
                backlogtitle.remove(backlog[i])
            i = i + 1
        await ctx.send('Queue cleared.')

def setup(client):
    client.add_cog(musicSystem(client))