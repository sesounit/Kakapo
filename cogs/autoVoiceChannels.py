
import discord
from discord.ext import commands, tasks
channelnumber=1
lockedchannels=[]
#autoVoiceChannels Cog
class autoVoiceChannels(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(minutes=5)
    async def cleaner(self, member):
        print("Cleaner Running!")
        voice_channel_list = []
        for server in self.client.guilds:
            for channel in server.channels:
                if str(channel.type) == 'voice':
                    channelstring = channel.name
                    if '#' in channelstring:
                        for channel in voice_channel_list:
                            if channel == channelstring:
                                break
                        else:
                            voice_channel_list.append(channelstring)
        for channel in voice_channel_list:
            channelName = discord.utils.get(member.guild.voice_channels, name=channel)
            members = channelName.members
            membercount = 0
            for member in members:
                membercount = (membercount + 1)
            if membercount == 0:
                await channelName.delete()


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
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
                #The try except block is unecessary, but for some reason, when I removed it, it bricked. So uhh, yeah not sure what's going on there.
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
        
        if '#' in before.channel.name:
            channelName = discord.utils.get(member.guild.voice_channels, name=before.channel.name)
            members = channelName.members
            membercount = 0
            for member in members:
                membercount = (membercount + 1)
            if membercount == 0:
                print("Cleaner about to be activated.")
                await self.cleaner.start(member)

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
