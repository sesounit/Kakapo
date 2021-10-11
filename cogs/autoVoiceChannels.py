
import discord
import re
from discord.ext import commands
channelnumber=1
lockedchannels=[]
#autoVoiceChannels Cog
class autoVoiceChannels(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print(before.channel.name)
        for channel in lockedchannels:
            if before.channel.name == channel:
                print(channel)
                channelName = discord.utils.get(member.guild.voice_channels, name=channel)
                members = channelName.members
                membercount = 0
                for member in members:
                    membercount = (membercount + 1)
                await channelName.edit(user_limit=membercount)


        if member.voice.channel.id == 694641754686881883:
            global channelnumber
            memberstatus = str(member.status)
            print(memberstatus)
            if memberstatus == 'offline':
                await member.voice.channel.clone(name=f"#{channelnumber} [General]", reason=None)
                newChannel = discord.utils.get(member.guild.voice_channels, name=f"#{channelnumber} [General]")
                await newChannel.move(beginning=True, reason="Automatic")
                await member.move_to(newChannel)
                channelnumber = (channelnumber + 1)
            else:
                try:
                    Channel = discord.utils.get(member.guild.voice_channels, name=f"#NC [{memberstatus}]")
                    await member.voice.channel.clone(name=f"#{channelnumber} [{memberstatus}]", reason=None)
                    newChannel = discord.utils.get(member.guild.voice_channels, name=f"#{channelnumber} [{memberstatus}]")
                    await newChannel.move(beginning=True, reason="Automatic")
                    await member.move_to(newChannel)
                    channelnumber = (channelnumber + 1)
                except:
                    await member.voice.channel.clone(name=f"#NC [{memberstatus}]", reason=None)
                    newChannel = discord.utils.get(member.guild.voice_channels, name=f"#NC [{memberstatus}]")
                    await newChannel.move(beginning=True, reason="Automatic")
                    await member.move_to(newChannel)
    
    @commands.command()
    async def destroy(self, ctx, *, channelName):
        if ctx.message.author.id == 267469338557153300:
            channelName = discord.utils.get(ctx.guild.voice_channels, name=channelName)
            await channelName.delete()
    @commands.command()
    async def limit(self, ctx, limiter, *, channelName):
        if limiter == 'None' or limiter == 'none' or limiter == 0:
            channelName = discord.utils.get(ctx.guild.voice_channels, name=channelName)
            await channelName.edit(user_limit=0)
        else:
            limiter = int(limiter)
            channelName = discord.utils.get(ctx.guild.voice_channels, name=channelName)
            await channelName.edit(user_limit=limiter)
    @commands.command()
    async def lock(self, ctx, *, channelName):
        global lockedchannels
        for channel in lockedchannels:
            if channel == channelName:
                await ctx.send("Channel already locked.")
        else:
            lockedchannels.append(channelName)
            channelName = discord.utils.get(ctx.guild.voice_channels, name=channelName)
            members = channelName.members
            membercount = 0
            for member in members:
                membercount = (membercount + 1)
            await channelName.edit(user_limit=membercount)
    @commands.command()
    async def unlock(self, ctx, *, channelName):
        global lockedchannels
        for channel in lockedchannels:
            if channel == channelName:
                realChannelName = discord.utils.get(ctx.guild.voice_channels, name=channelName)
                members = realChannelName.members
                for member in members:
                    if ctx.message.author == member:
                        lockedchannels.remove(channelName)
                        await realChannelName.edit(user_limit=0)
        

def setup(client):
    client.add_cog(autoVoiceChannels(client))
