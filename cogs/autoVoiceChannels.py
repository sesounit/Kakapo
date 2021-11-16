
import nextcord
from nextcord.ext import commands, tasks
channelnumber=1
lockedchannels=[]
#autoVoiceChannels Cog
class autoVoiceChannels(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(minutes=5)
    async def cleaner(self, member):
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
            channelName = nextcord.utils.get(member.guild.voice_channels, name=channel)
            members = channelName.members
            membercount = 0
            for member in members:
                membercount = (membercount + 1)
            if membercount == 0:
                await channelName.delete()


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        for channel in lockedchannels:
            try:
                if before.channel.name == channel:
                    channelName = nextcord.utils.get(member.guild.voice_channels, name=channel)
                    members = channelName.members
                    membercount = 0
                    for member in members:
                        membercount = (membercount + 1)
                    await channelName.edit(user_limit=membercount)
            except:
                pass
        try:
            if member.voice.channel.id == 694641754686881883:
                global channelnumber
                memberstatus = str(member.status)
                print(memberstatus)
                if memberstatus == 'offline':
                    await member.voice.channel.clone(name=f"#{channelnumber} [General]", reason=None)
                    newChannel = nextcord.utils.get(member.guild.voice_channels, name=f"#{channelnumber} [General]")
                    await newChannel.move(beginning=True, reason="Automatic")
                    await member.move_to(newChannel)
                    channelnumber = (channelnumber + 1)
                else:
                    #The try except block is unecessary, but for some reason, when I removed it, it bricked. So uhh, yeah not sure what's going on there.
                    try:
                        Channel = nextcord.utils.get(member.guild.voice_channels, name=f"#NC [{memberstatus}]")
                        await member.voice.channel.clone(name=f"#{channelnumber} [{memberstatus}]", reason=None)
                        newChannel = nextcord.utils.get(member.guild.voice_channels, name=f"#{channelnumber} [{memberstatus}]")
                        await newChannel.move(beginning=True, reason="Automatic")
                        await member.move_to(newChannel)
                        channelnumber = (channelnumber + 1)
                    except:
                        await member.voice.channel.clone(name=f"#NC [{memberstatus}]", reason=None)
                        newChannel = nextcord.utils.get(member.guild.voice_channels, name=f"#NC [{memberstatus}]")
                        await newChannel.move(beginning=True, reason="Automatic")
                        await member.move_to(newChannel)
        except:
            pass
        try:
            if '#' in before.channel.name:
                channelName = nextcord.utils.get(member.guild.voice_channels, name=before.channel.name)
                members = channelName.members
                membercount = 0
                for member in members:
                    membercount = (membercount + 1)
                if membercount == 0:
                    print("Cleaner about to be activated.")
                    await self.cleaner.start(member)
        except:
            pass
    @commands.command()
    async def destroy(self, ctx, *, channelName):
        if ctx.message.author.id == 267469338557153300:
            channelName = nextcord.utils.get(ctx.guild.voice_channels, name=channelName)
            await channelName.delete()
    @commands.command()
    async def limit(self, ctx, limiter):
        channelName = ctx.message.author.voice.channel.name
        if limiter == 'None' or limiter == 'none' or limiter == 0:
            channelName = nextcord.utils.get(ctx.guild.voice_channels, name=channelName)
            await channelName.edit(user_limit=0)
        else:
            limiter = int(limiter)
            channelName = nextcord.utils.get(ctx.guild.voice_channels, name=channelName)
            await channelName.edit(user_limit=limiter)
    @commands.command()
    async def lock(self, ctx):
        global lockedchannels
        channelName = ctx.message.author.voice.channel.name
        for channel in lockedchannels:
            if channel == channelName:
                await ctx.send("Channel already locked.")
        else:
            lockedchannels.append(channelName)
            channelName = nextcord.utils.get(ctx.guild.voice_channels, name=channelName)
            members = channelName.members
            membercount = 0
            for member in members:
                membercount = (membercount + 1)
            await channelName.edit(user_limit=membercount)
    @commands.command()
    async def unlock(self, ctx):
        global lockedchannels
        channelName = ctx.message.author.voice.channel.name
        for channel in lockedchannels:
            if channel == channelName:
                realChannelName = nextcord.utils.get(ctx.guild.voice_channels, name=channelName)
                members = realChannelName.members
                for member in members:
                    if ctx.message.author == member:
                        lockedchannels.remove(channelName)
                        await realChannelName.edit(user_limit=0)
        

def setup(client):
    client.add_cog(autoVoiceChannels(client))
