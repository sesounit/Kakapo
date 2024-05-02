
import nextcord, re, os.path, json
from nextcord.ext import commands, tasks
from typing import Optional

#Guild object to represent servers
class vcGuild:
    def __init__(self, guildId, newSessionId, textChannel, locked_voice_channels=[], created_voice_channels={}, settings={'maxChannels': 5, 'renameOn': True, 'renameAdmin': True, 'lockedOn': True, 'lockedAdmin': True}):
        self.guildId = guildId
        self.newSession = newSessionId
        self.locked_voice_channels = locked_voice_channels
        self.created_voice_channels = created_voice_channels
        self.textChannel = textChannel
        self.settings = settings
        #TODO Settings have been added, monitor for likely bugs and exploits.
        # Settings should include: Max channels, rename on/off, rename channels admin-only, locked channels on/off, locked channels admin-only.

    # Dumps data to json
    def saveData(self):
        origin = os.path.abspath('')
        origin = origin.replace('\\', "/")
        server = {'newSession' : self.newSession, 'locked_voice_channels' : self.locked_voice_channels, 'created_voice_channels' : self.created_voice_channels, 'textChannel' : self.textChannel, 'settings' : self.settings}

        with open(f'{origin}/jsons/VCServers/{self.guildId}-voiceChannel.json', 'w') as f:
            json.dump(server, f)

#autoVoiceChannels Cog
class autoVoiceChannels(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.VCGuilds = {}
        # Start the cleaner at cog load
        self.cleaner.start()
    
    @commands.Cog.listener()
    async def on_ready(self):
        #Read the pre-existing JSON
        origin = os.path.abspath('')
        origin = origin.replace('\\', "/")
        for file in os.listdir(f'{origin}/jsons/VCServers'):
            if 'json' in file:
                parts = file.split('-')
                with open(f'{origin}/jsons/VCServers/{file}') as json_file:
                    guildjson = json.load(json_file)
                    self.VCGuilds[int(parts[0])] = vcGuild(parts[0], guildjson['newSession'], guildjson['textChannel'], guildjson['locked_voice_channels'], guildjson['created_voice_channels'], guildjson['settings'])
    
    # Check and delete channels with less than 1 members every 5 mins
    @tasks.loop(minutes=5)
    async def cleaner(self):
        # Iterate through all created channels and clean them.
        for guildObjKey in self.VCGuilds:
            for channelKey in self.VCGuilds[guildObjKey].created_voice_channels.copy():
                channel = await self.client.fetch_channel(self.VCGuilds[guildObjKey].created_voice_channels[channelKey])
                if len(channel.members) < 1:
                    await channel.delete()
                    self.VCGuilds[guildObjKey].created_voice_channels.pop(channelKey)
                    self.VCGuilds[guildObjKey].saveData()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # Ignore mute/unmute events and Leave events
        if before.channel == after.channel or after.channel == None:
            return
        
        # Return guild object from self.VCGuilds
        # At the same time, discover if guild even has autoVC enabled.
        if member.guild.id in self.VCGuilds:
            guildObj = self.VCGuilds[member.guild.id]
        else:
            return

        # When member leaves a locked channel, update the user limit or remove channel
        for locked_channel in guildObj.locked_voice_channels:
            if before.channel.id == locked_channel:
                if len(before.channel.members) < 1:
                    guildObj.locked_voice_channels.remove(before.channel.id)
                await before.channel.edit(user_limit=len(before.channel.members))
                
        # I'm going to regret putting in another for loop, but reading over the docs I don't think there's an easier way to do this.
        guildchannelids = []
        for channel in member.guild.voice_channels:
            guildchannelids.append(channel.id)

        # list.copy() creates a duplicate of the list, so that we can modify the original list while looping through the new, temporary one.
        for channelKey in self.VCGuilds[member.guild.id].created_voice_channels.copy():
            if self.VCGuilds[member.guild.id].created_voice_channels[channelKey] not in guildchannelids:
                self.VCGuilds[member.guild.id].created_voice_channels.pop(channelKey)

        if after.channel.id == guildObj.newSession:
            newChannelId = None
            for i in range(1, guildObj.settings['maxChannels'] + 1):
                if str(i) not in guildObj.created_voice_channels:
                    newChannelId = i
                    break
            else:
                textChannel = nextcord.utils.get(await member.guild.fetch_channels(), id=guildObj.textChannel)
                await textChannel.send(f"There are currently {guildObj.settings['maxChannels']} active sessions, please wait for old ones to be cleaned before creating a new session. \nIf you believe this to be in error, please report this to the support server.")
                return
            # Create channel and append to created_voice_channels
            channel_name = f"#{newChannelId} [General]"
            created_channel = await member.voice.channel.clone(name=channel_name, reason=None)
            guildObj.created_voice_channels[str(newChannelId)] = created_channel.id

            # Move created channel to beginning and move member into it
            await created_channel.move(beginning=True, reason="Automatic")
            await member.move_to(created_channel)

            # Dump data now that a new channel has been created.
            guildObj.saveData()

    @nextcord.slash_command(name='destroy',description="Admin Only, gracefully destroy a channel. Not necessary, mostly present for debugging.")
    async def destroy(self, ctx, *, channel_name):
        if not ctx.user.guild_permissions.administrator:
            return await ctx.response.send_message("You are not authorized to run this command.", ephemeral=True)
        channel_name = nextcord.utils.get(ctx.guild.voice_channels, name=channel_name)
        await channel_name.delete()
        self.VCGuilds[ctx.guild.id].created_voice_channels.pop(channel_name.id)
        self.VCGuilds[ctx.guild.id].saveData()

    @nextcord.slash_command(name='setvcsettings',description="Admin Only, sets the settings for the automatic voice channel system.")
    async def setVcSettings(self, ctx, newsessionchannel: Optional[nextcord.VoiceChannel] = nextcord.SlashOption(required=False), maxchannels:  Optional[int] = nextcord.SlashOption(required=False), renameon:  Optional[bool] = nextcord.SlashOption(required=False), renameadmin:  Optional[bool] = nextcord.SlashOption(required=False), lockedon:  Optional[bool] = nextcord.SlashOption(required=False), lockedadmin:  Optional[bool] = nextcord.SlashOption(required=False)):
        if not ctx.user.guild_permissions.administrator:
            return await ctx.response.send_message("You are not authorized to run this command.", ephemeral=True)
        # Ensure auto-VC has been setup already.
        if ctx.guild_id not in self.VCGuilds:
            return await ctx.response.send_message("AutoVC has not been initialized on this server.")
        
        # Ensure maxChannels is in bounds, rest should be boolean so no concerns.
        if maxchannels != None:
            if maxchannels > 8 or maxchannels < 1:
                return await ctx.response.send_message("Max Channels can not be greater than 8 or less than 0.")
        
        # If max channels is in bound, defer response just incase.
        await ctx.response.defer()
        
        guildObj = self.VCGuilds[ctx.guild_id]

        if newsessionchannel != None:
            guildObj.newSession = newsessionchannel.id
        
        settings = {'maxChannels': maxchannels, 'renameOn': renameon, 'renameAdmin': renameadmin, 'lockedOn': lockedon, 'lockedAdmin': lockedadmin}
        # Loop through settings and determine if they were set. If a setting is equal to none, it was not set, continue to the next setting in the list.
        for setting in settings:
            if settings[setting] == None:
                continue
            guildObj.settings[setting] = settings[setting]

        guildObj.saveData()

        await ctx.followup.send("VC settings have been updated.")


    @nextcord.slash_command(name='setupvc',description="Admin Only, sets up the autoVC cog for this server.")
    async def setUpVc(self, ctx, newsessionchannel: nextcord.VoiceChannel):
        if not ctx.user.guild_permissions.administrator:
            return await ctx.response.send_message("You are not authorized to run this command.", ephemeral=True)
        if ctx.guild.id in self.VCGuilds:
            del self.VCGuilds[ctx.guild.id]
        self.VCGuilds[ctx.guild.id] = vcGuild(ctx.guild.id, newsessionchannel.id, ctx.channel.id)
        self.VCGuilds[ctx.guild.id].saveData()
        await ctx.response.send_message("The Auto-Voice channels feature has been enabled in this discord!")

    @nextcord.slash_command(name='limit',description="Set a static limit for this channel.")
    async def limit(self, ctx, limiter: str):
        if not self.VCGuilds[ctx.guild.id].settings['lockedOn'] or (self.VCGuilds[ctx.guild.id].settings['lockedAdmin'] and not ctx.user.guild_permissions.administrator):
            return await ctx.response.send_message("This server's settings have prevented you from setting a channel limit.")
        for channel in self.VCGuilds[ctx.guild.id].created_voice_channels:
            if self.VCGuilds[ctx.guild.id].created_voice_channels[channel] == ctx.user.voice.channel.id:
                break
        else:
            await ctx.response.send_message("Permanent Discord channels cannot be limited.")
            return
        if  limiter.lower() == 'none' or int(limiter) < 1:
            await ctx.user.voice.channel.edit(user_limit=0)
        else:
            limiter = int(limiter)
            await ctx.user.voice.channel.edit(user_limit=limiter)
        await ctx.response.send_message("Channel limit updated!")

    @nextcord.slash_command(name='lock',description="Dynamically lock a channel")
    async def lock(self, ctx):
        # TODO: Lock function should get a new way to determine if it's a permanent channel. A for-break is not ideal.
        if not self.VCGuilds[ctx.guild.id].settings['lockedOn'] or (self.VCGuilds[ctx.guild.id].settings['lockedAdmin'] and not ctx.user.guild_permissions.administrator):
            return await ctx.response.send_message("This server's settings have prevented you from locking this channel.")
        authors_voice_channel = ctx.user.voice.channel
        if authors_voice_channel.id in self.VCGuilds[ctx.guild.id].locked_voice_channels:
            await ctx.response.send_message("Channel already locked.")
            return
        for channel in self.VCGuilds[ctx.guild.id].created_voice_channels:
            if self.VCGuilds[ctx.guild.id].created_voice_channels[channel] == authors_voice_channel.id:
                break
        else:
            await ctx.response.send_message("Permanent Discord channels cannot be locked.")
            return
        
        self.VCGuilds[ctx.guild.id].locked_voice_channels.append(authors_voice_channel.id)
        await authors_voice_channel.edit(user_limit=len(authors_voice_channel.members))
        self.VCGuilds[ctx.guild.id].saveData()
        await ctx.response.send_message("Channel locked!")

    @nextcord.slash_command(name='unlock',description="Unlock a channel")
    async def unlock(self, ctx):
        if (self.VCGuilds[ctx.guild.id].settings['lockedAdmin'] and not ctx.user.guild_permissions.administrator):
            return await ctx.send("This server requires you to be an admin to unlock a channel.")
        authors_voice_channel = ctx.user.voice.channel
        if (authors_voice_channel.id in self.VCGuilds[ctx.guild.id].locked_voice_channels):
            self.VCGuilds[ctx.guild.id].locked_voice_channels.remove(authors_voice_channel.id)
            await authors_voice_channel.edit(user_limit=0)
            self.VCGuilds[ctx.guild.id].saveData()
            await ctx.response.send_message("Channel unlocked!")

    @nextcord.slash_command(name='rename',description="Rename a channel")
    async def rename(self, ctx, new_name: str):
        if not self.VCGuilds[ctx.guild.id].settings['renameOn'] or (self.VCGuilds[ctx.guild.id].settings['renameAdmin'] and not ctx.user.guild_permissions.administrator):
            return await ctx.response.send_message("This server's settings have prevented you from renaming this channel.")
        authors_voice_channel = ctx.user.voice.channel
        for channel in self.VCGuilds[ctx.guild.id].created_voice_channels:
            if self.VCGuilds[ctx.guild.id].created_voice_channels[channel] == authors_voice_channel.id:
                break
        else:
            await ctx.response.send_message("Permanent Discord channels cannot be locked.")
            return
        if len(new_name) > 19:
            await ctx.response.send_message('New name is too long! Please limit it to 19 characters or less.')
            return
        number = int(re.search(r'\d+', authors_voice_channel.name).group())
        try:
            await authors_voice_channel.edit(name=f"#{number} [{new_name}]")
            await ctx.response.send_message(f"Channel renamed to #{number} [{new_name}]")
        except:
            await ctx.response.send_message('An error was encountered attempting to edit the channel name.')

        

def setup(client):
    client.add_cog(autoVoiceChannels(client))
