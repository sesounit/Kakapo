import nextcord, os, sys, random
from dotenv import load_dotenv
import nacl
from yt_dlp import YoutubeDL
from nextcord.ext import commands, tasks
from youtubesearchpython.__future__ import *

#Music Related
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
backlog = []
nextinqueueactive = False
voicestopped = False
guild2 = 'Null'
ydl_opts = {'format': 'bestaudio'}
nowPlaying = 'Nada'
#musicSystem Cog
class musicSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
    nextinqueueactive = False
    voicestopped = False
    @commands.command(aliases=['np'])
    async def nowPlaying(self, ctx):
        global nowPlaying
        ListEmbed = nextcord.Embed(title="Now Playing:", description=nowPlaying, color=0x0000ff)
        ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
        await ctx.message.channel.send(embed=ListEmbed)

    @commands.Cog.listener()
    async def on_ready(self):
        global nextinqueueactive
        nextinqueueactive = True
        await self.nextinqueue.start()
    #This has some debugging phrases that print to the console. Not really necessary anymore, but would be helpful if something were to go wrong.
    @tasks.loop(seconds=5)
    async def nextinqueue(self):
        global nowPlaying
        global ydl_opts
        global guild2
        global backlog
        global voicestopped
        voice = nextcord.utils.get(self.client.voice_clients, guild = guild2)
        if voicestopped == False:
            if voice == None:
                pass
            elif voice.is_playing():
                pass
            else:
                try:
                    video_link = next(iter(backlog))
                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_link, download=False)
                        URL = info['formats'][0]['url']
                    voice.play(nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    backlog.remove(video_link)
                    nowPlaying = video_link
                except:
                    print('')
                
        if voice != None:
            if voice.is_playing == False:
                await self.timeout.start()

    @tasks.loop(minutes=25)
    async def timeout(self):
        voice = nextcord.utils.get(self.client.voice_clients, guild = guild2)

        if voice.is_playing == True:
            await self.timeout.stop()

        elif voice.is_connected == True:
            await voice.disconnect

    #Looks weird, probably could be cleaner, but works this way.
    #The youtube-dl shit that actually plays the music could be made into a function to avoid copy pasting several times, but this is for free so. ¯\_(ツ)_/¯
    #Also don't touch this part without telling me, it'll probably break if you so much as breathe on it.

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, video_link : str):
        global nextinqueueactive
        print(nextinqueueactive)
        if nextinqueueactive == False:
            await ctx.send("Setup Function Called, retry request.")
            nextinqueueactive = True
            await self.nextinqueue.start()
        global nowPlaying
        voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
        global ydl_opts
        global backlog
        global guild2
        global voicestopped
        voicestopped = False
        guild2 = ctx.guild
        voiceChannel = ctx.author.voice.channel

        if video_link == 'Next':
            video_link = next(iter(backlog))
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
                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_link, download=False)
                        URL = info['formats'][0]['url']
                    backlog.append(video_link)
                    ListEmbed = nextcord.Embed(title="Added to Queue", description=backlog, color=0x0000ff)
                    ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
                    await ctx.message.channel.send(embed=ListEmbed)

                else:
                    voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_link, download=False)
                        URL = info['formats'][0]['url']
                    voice.play(nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    nowPlaying = video_link
                    await ctx.invoke(self.client.get_command('nowPlaying'))
            else:
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_link, download=False)
                    URL = info['formats'][0]['url']
                await voiceChannel.connect()
                voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
                voice.play(nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                nowPlaying = video_link
                await ctx.invoke(self.client.get_command('nowPlaying'))
        except:
            await ctx.send("A problem occured while trying to play.")
    @commands.command()
    async def skip(self, ctx):
        try:
            global nowPlaying
            global voicestopped
            global ydl_opts
            voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
            if voice.is_playing():
                voice.stop()
            videolink = next(iter(backlog))
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(videolink, download=False)
                URL = info['formats'][0]['url']
            voice.play(nextcord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            backlog.remove(videolink)
            voicestopped = False
            nowPlaying = videolink
            await ctx.invoke(self.client.get_command('nowPlaying'))
        except:
            await ctx.send("There is nothing in the queue.")

    @commands.command()
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
        global nowPlaying
        voice = nextcord.utils.get(self.client.voice_clients, guild = ctx.guild)
        voice.stop()
        global voicestopped
        voicestopped = True
        nowPlaying = 'Nada'

    @commands.command(aliases=["Q"])
    async def queue(self, ctx):
        ListEmbed = nextcord.Embed(title="In queue", description=backlog, color=0x0000ff)
        ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
        await ctx.message.channel.send(embed=ListEmbed)

    @commands.command(aliases=['clear'])
    async def empty(self, ctx):
        global backlog
        backlog = []
        await ctx.send('Queue cleared.')

def setup(client):
    client.add_cog(musicSystem(client))