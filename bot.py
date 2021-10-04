# bot.py
import discord, os
from dotenv import load_dotenv
import nacl
import youtube_dl
import os
from discord.ext import commands, tasks
'''
Heyo Sag, this is pickler here.-
    Sorry if the comments aren't serious, but you might've seen that one coming when you asked me to help you out.
    The code doesn't exactly follow clean code principals as described in Robert Cecil Martin's landmark book that no one read-
    But oh well, it works, right? Also, I can understand it the way it is so- Don't **need** to fix it really.

    Reminders for dependencies:
        youtube_dl, ffmpeg
        I'm like 90% sure that's it. They can both probably be installed by command line, however iirc one is outdated if you do it like so.
        So if it breaks, just tell me.
'''
# is a .env file inside the folder to leave the token for the bot outside the git
load_dotenv()

# bot commands have prefix ! so all messages start with ! will trigger the bot commands
client = commands.Bot(command_prefix='!')
#Music Related
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
backlog = []
voicestopped = False
guild2 = 'Null'
# when the bot is initialized it will print has connected to the terminal
@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")
    await nextinqueue.start()
# Not at all necessary, but I like a version notes command, and the one I've used in the past looks nice.
@client.command(name='version')
async def version(context):

    mainEmbed = discord.Embed(title="Kakapo Version Notes", description="SESO's Multi-Use Discord Bot", color=0x0E8643)
    mainEmbed.add_field(name="Version Code:", value="v0.0.1", inline=False)
    mainEmbed.add_field(name="Date Released:", value="September 27, 2021", inline=False)
    mainEmbed.set_footer(text="Kakapo written by Dildo Sagbag#8107, Pickle423#0408.")

    await context.message.channel.send(embed=mainEmbed)
#This has some debugging phrases that print to the console. Not really necessary anymore, but would be helpful if something were to go wrong.
@tasks.loop(seconds=5)
async def nextinqueue():
    global guild2
    global backlog
    global voicestopped
    if voicestopped == False:
        voice = discord.utils.get(client.voice_clients, guild = guild2)
        print(voice)
        if voice == None:
            print('None')
        elif voice.is_playing():
            print('Already Playing')
        else:
            try:
                videolink = next(iter(backlog))
                ydl_opts = {'format': 'bestaudio'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(videolink, download=False)
                    URL = info['formats'][0]['url']
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                backlog.remove(videolink)
                print(backlog)
            except:
                pass
        if voice != None:
            if voice.is_playing == True:
                await timeout.start()
    else:
        print('Stopped')
@tasks.loop(minutes=25)
async def timeout():
    voice = discord.utils.get(client.voice_clients, guild = guild2)
    if voice.is_playing == True:
        await timeout.stop()
    elif voice.is_connected == True:
        await voice.disconnect
#Looks weird, probably could be cleaner, but works this way.
#The youtube-dl shit that actually plays the music could be made into a function to avoid copy pasting several times, but this is for free so. ¯\_(ツ)_/¯
#Also don't touch this part without telling me, it'll probably break if you so much as breathe on it.
@client.command()
async def play(ctx, video_link : str):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    global backlog
    global guild2
    global voicestopped
    voicestopped = False
    guild2 = ctx.guild
    voiceChannel = ctx.author.voice.channel
    if video_link == 'Next':
        video_link = next(iter(backlog))
    elif voice != None:
        if voice.is_playing():
            try:
                ydl_opts = {'format': 'bestaudio'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_link, download=False)
                    URL = info['formats'][0]['url']
                backlog.append(video_link)
                ListEmbed = discord.Embed(title="Added to Queue", description=backlog, color=0x0000ff)
                ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
                await ctx.message.channel.send(embed=ListEmbed)
            except:
                await ctx.send("Bad Link")
        else:
            try:
                voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
                ydl_opts = {'format': 'bestaudio'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_link, download=False)
                    URL = info['formats'][0]['url']
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            except:
                await ctx.send("Bad Link")
    else:
        try:
            ydl_opts = {'format': 'bestaudio'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_link, download=False)
                URL = info['formats'][0]['url']
            await voiceChannel.connect()
            voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        except:
            await ctx.send("Bad Link")
@client.command()
async def skip(ctx):
    global voicestopped
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.stop()
    videolink = next(iter(backlog))
    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(videolink, download=False)
        URL = info['formats'][0]['url']
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    backlog.remove(videolink)
    voicestopped = False
    print(backlog)
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send('The bot is not connected to a voice channel.')
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        ctx.send('No audio is playing currently.')
@client.command(aliases=['Unpause', 'unpause', 'Resume'])
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        ctx.send('Audio is not paused.')
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    voice.stop()
    global voicestopped
    voicestopped = True
@client.command()
async def queue(ctx):
    ListEmbed = discord.Embed(title="In queue", description=backlog, color=0x0000ff)
    ListEmbed.set_footer(text="Music Functionality written by Pickle423#0408")
    await ctx.message.channel.send(embed=ListEmbed)
@client.command(aliases=['Clear', 'clear', 'Empty'])
async def empty(ctx):
    global backlog
    backlog = []
    await ctx.send('Queue cleared.')

client.run(os.getenv("discord_token"))