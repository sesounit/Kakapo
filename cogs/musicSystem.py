import discord, os, sys, random
from dotenv import load_dotenv
import nacl
from yt_dlp import YoutubeDL
from discord.ext import commands, tasks
from youtubesearchpython.__future__ import *

#Music Related
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
backlog = []
voicestopped = False
guild2 = 'Null'
ydl_opts = {'format': 'bestaudio', 'default_search' : 'auto'}
#musicSystem Cog
class musicSystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        print("Music System Online")
        await self.nextinqueue.start()
    
    #This has some debugging phrases that print to the console. Not really necessary anymore, but would be helpful if something were to go wrong.
    @tasks.loop(seconds=5)
    async def nextinqueue(self):
        global ydl_opts
        global guild2
        global backlog
        global voicestopped
        if voicestopped == False:
            voice = discord.utils.get(self.client.voice_clients, guild = guild2)
            print(voice)
            if voice == None:
                print('None')
            elif voice.is_playing():
                print('Already Playing')
            else:
                try:
                    videolink = next(iter(backlog))
                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(videolink, download=False)
                        URL = info['format'][0]['url']
                    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    backlog.remove(videolink)
                    print(backlog)
                except:
                    pass
            if voice != None:
                if voice.is_playing == False:
                    await self.timeout.start()
        else:
            print('Stopped')

    @tasks.loop(minutes=25)
    async def timeout(self):
        voice = discord.utils.get(self.client.voice_clients, guild = guild2)

        if voice.is_playing == True:
            await self.timeout.stop()

        elif voice.is_connected == True:
            await voice.disconnect

    #Looks weird, probably could be cleaner, but works this way.
    #The youtube-dl shit that actually plays the music could be made into a function to avoid copy pasting several times, but this is for free so. ¯\_(ツ)_/¯
    #Also don't touch this part without telling me, it'll probably break if you so much as breathe on it.

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, video_link : str):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        global ydl_opts
        global backlog
        global guild2
        global voicestopped
        voicestopped = False
        guild2 = ctx.guild
        voiceChannel = ctx.author.voice.channel

        if video_link == 'Next':
            video_link = next(iter(backlog))
        
        if "https://" not in video_link:
            videosSearch = VideosSearch(video_link, limit = 1)
            videosResult = await videosSearch.next()
            video_link = videosResult['result'][0]['link']
        if voice != None:
            if voice.is_playing():
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_link, download=False)
                    URL = info['formats'][0]['url']
                backlog.append(video_link)
                ListEmbed = discord.Embed(title="Added to Queue", description=backlog, color=0x0000ff)
                ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
                await ctx.message.channel.send(embed=ListEmbed)

            else:
                voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_link, download=False)
                    URL = info['formats'][0]['url']
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        else:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_link, download=False)
                URL = info['formats'][0]['url']
            await voiceChannel.connect()
            voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

    @commands.command()
    async def skip(self, ctx):
        global voicestopped
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)

        if voice.is_playing():
            voice.stop()
        videolink = next(iter(backlog))
        ydl_opts = {'format': 'bestaudio'}

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(videolink, download=False)
            URL = info['formats'][0]['url']
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        backlog.remove(videolink)
        voicestopped = False
        print(backlog)

    @commands.command()
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send('The bot is not connected to a voice channel.')

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            ctx.send('No audio is playing currently.')

    @commands.command(aliases=['unpause'])
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            ctx.send('Audio is not paused.')

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        voice.stop()
        global voicestopped
        voicestopped = True

    @commands.command()
    async def queue(self, ctx):
        ListEmbed = discord.Embed(title="In queue", description=backlog, color=0x0000ff)
        ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
        await ctx.message.channel.send(embed=ListEmbed)

    @commands.command(aliases=['clear'])
    async def empty(self, ctx):
        global backlog
        backlog = []
        await ctx.send('Queue cleared.')

def setup(client):
    client.add_cog(musicSystem(client))