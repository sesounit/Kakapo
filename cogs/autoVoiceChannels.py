import nextcord, re
from nextcord.ext import commands, tasks

#autoVoiceChannels Cog
class autoVoiceChannels(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.locked_voice_channels = []
        self.created_voice_channels = []
        self.latest_channel_number = 0
        # Start the cleaner at cog load
        self.cleaner.start()

    # Check and delete channels with less than 1 members every 5 mins
    @tasks.loop(minutes=5)
    async def cleaner(self):
        # If created_voice_channels is empty, iterate through server to find stragglers and add them to created_voice_channels
        self.created_voice_channels = [channel for server in self.client.guilds for channel in server.voice_channels if ('#' in channel.name)]

        # Delete any created_voice_channels with no current members
        for created_voice_channel in self.created_voice_channels.copy():
            if len(created_voice_channel.members) < 1:
                await created_voice_channel.delete()
                self.created_voice_channels.remove(created_voice_channel)

        # After clean up, set channel_number to latest channel number
        # Possible logic error since channel number may be higher than length of created_voice_channels
        if len(self.created_voice_channels) >= 1:
            self.latest_channel_number = int(re.search(r'\d+', self.created_voice_channels[-1].name).group())+1
        else:
            self.latest_channel_number = len(self.created_voice_channels)+1



    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # Ignore mute/unmute events
        if before.channel == after.channel:
            return

        # When member leaves a locked channel, update the user limit or remove channel
        for locked_channel in self.locked_voice_channels:
            if before.channel == locked_channel:
                if len(locked_channel.members) < 1:
                    self.locked_voice_channels.remove(before.channel.id)
                await before.channel.edit(user_limit=len(locked_channel.members))

        #SESO Discord new session channel id: 694641754686881883
        #Kakapo Red Testing Discord new session channel id: 911066596456415268
        if member.voice != None and member.voice.channel.id == 694641754686881883:
            # Create channel and append to created_voice_channels
            channel_name = f"#{self.latest_channel_number} [General]"
            created_channel = await member.voice.channel.clone(name=channel_name, reason=None)
            self.created_voice_channels.append(created_channel)

            # Move created channel to beginning and move member into it
            await created_channel.move(beginning=True, reason="Automatic")
            await member.move_to(created_channel)

            # Update channel_number according to created_voice_channels length
            if len(self.created_voice_channels) >= 1:
                self.latest_channel_number = int(re.search(r'\d+', self.created_voice_channels[-1].name).group())+1
            else:
                self.latest_channel_number = len(self.created_voice_channels)+1

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def destroy(self, ctx, *, channel_name):
        channel_name = nextcord.utils.get(ctx.guild.voice_channels, name=channel_name)
        await channel_name.delete()

    @commands.command()
    async def limit(self, ctx, limiter):
        channel_name = ctx.message.author.voice.channel.name
        if  limiter < 1 or limiter.lower() == 'none':
            channel_name = nextcord.utils.get(ctx.guild.voice_channels, name=channel_name)
            await channel_name.edit(user_limit=0)
        else:
            limiter = int(limiter)
            channel_name = nextcord.utils.get(ctx.guild.voice_channels, name=channel_name)
            await channel_name.edit(user_limit=limiter)

    @commands.command()
    async def lock(self, ctx):
        authors_voice_channel = ctx.message.author.voice.channel
        if authors_voice_channel in self.locked_voice_channels:
            await ctx.send("Channel already locked.")
        elif authors_voice_channel not in self.created_voice_channels:
            await ctx.send("Permanent Discord channels cannot be locked.")
        else:
            self.locked_voice_channels.append(authors_voice_channel)
            await authors_voice_channel.edit(user_limit=len(authors_voice_channel.members))

    @commands.command()
    async def unlock(self, ctx):
        authors_voice_channel = ctx.message.author.voice.channel
        if (authors_voice_channel in self.locked_voice_channels) and (ctx.message.author in authors_voice_channel.members) and (('#' in authors_voice_channel.name)):
            self.locked_voice_channels.remove(authors_voice_channel)
            await authors_voice_channel.edit(user_limit=0)

    @commands.command(aliases=['ren', 'rn'])
    async def rename(self, ctx, *, new_name):
        authors_voice_channel = ctx.message.author.voice.channel
        if authors_voice_channel in self.created_voice_channels:
            if len(new_name) > 19:
                await ctx.send('New name is too long! Please limit it to 19 characters or less.')
                return
            number = int(re.search(r'\d+', authors_voice_channel.name).group())
            try:
                await authors_voice_channel.edit(name=f"#{number} [{new_name}]")
                await ctx.send(f"Channel renamed to #{number} [{new_name}]")
            except:
                await ctx.send('An error was encountered attempting to edit the channel name.')
        else:
            await ctx.send("Permanent Discord channels cannot be renamed.")
        

def setup(client):
    client.add_cog(autoVoiceChannels(client))
