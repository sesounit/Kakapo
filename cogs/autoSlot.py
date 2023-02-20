import nextcord, json, collections, os.path, datetime, re
from datetime import datetime
from nextcord.ext import commands

#autoSlot Cog
class autoSlot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.database = {'operations' : {}}

    @commands.Cog.listener()
    async def on_ready(self):
        #Check and load pre-existing JSON
        if os.path.exists('autoSlot.json'):
            with open('autoSlot.json', 'r') as json_file:
                self.database = json.load(json_file)

    @commands.command(name = "addmission", help = "Adds a new mission with given name. Use quotations for multi-word names", aliases=["am","addoperation","addop","ao"])
    @commands.has_permissions(administrator=True)
    async def addMission(self, ctx, mission_name: str):
        mission_id = len(self.database['operations'])

        # Make channel name that is compatible with discord's channel restrictions
        mission_name_converted = mission_name.replace(" ", "-").lower()


        # Warn user that mission name is converted for discord channel restrictions
        if (mission_name != mission_name_converted):
            await ctx.send(f"{ctx.author.mention} Your mission's channel will be named {mission_name_converted} from {mission_name}")

        #Warn user if there are more than 10 missions in database
        if len(self.database['operations']) > 10:
            await ctx.send("There are currently 10 active missions on ID's 1-10. Please delete old missions.")
            #return

        # Add operation to database
        self.database['operations'].update({mission_id : {'groups' : {}, 'channel_name' : mission_name_converted, 'name' : mission_name,'author' : ctx.author.id} })

        await ctx.send(f"{ctx.author.mention} Your mission ID for {mission_name_converted} is: {mission_id}")
        self.saveData()

    @commands.command(name = "addslots")
    @commands.has_permissions(administrator=True)
    async def addSlots(self, ctx, id, *, slots):
        # Check if mission ID exists
        try:
            if id not in self.database['operations']:
                return await ctx.send("There is no mission present in the database with this ID.")
        except:
            return await ctx.send("A problem occurred with the mission id.")

        # Parse slots to proper dictionary of groups
        group_dict = self.parseGroups(slots)

        # Save groups to database under specific mission id
        # self.database = self.updateDict(self.database, {'operations' : {id : {'groups' : group_dict}}})
        self.database['operations'][id]['groups'] = group_dict


        # Look for the missions_category and mission_channel
        missions_category = None
        mission_channel = None
        channel_name = self.database['operations'][id]['channel_name']

        # Look for roster category. If it doesnt exist, create it
        #TODO: Logic Error, keeps making a new roster category for every category that isnt called roster
        for category in ctx.guild.categories:
            if category.name == 'rosters':
                missions_category = category
                break
        if missions_category is None:
            missions_category = await ctx.guild.create_category('rosters')

        # Once created, look for the mission channel. Otherwise, create it
        for channel in missions_category.channels:
            if channel.name == (f"{id}-{channel_name}"):
                mission_channel = channel
                break

        if mission_channel is None:
            mission_channel = await missions_category.create_text_channel(f'{id}-{channel_name}')
            await mission_channel.send(self.parseRoster(ctx, id, group_dict))
        else:
            previous_roster = await mission_channel.history().get(author__id = self.client.user.id)
            await previous_roster.edit(self.parseRoster(ctx, id, group_dict))

        # Post the roster
        #m = await mission_channel.history().get(author__id = self.client.user.id)
        #await mission_channel.history().get(author__id = self.client.user.id).edit(self.parseRoster(ctx, id, group_dict))
        self.saveData()

    @commands.command(aliases=['assignslot','takeslot', 'claimslot', 'cslot', 'tslot','slot'])
    async def aslot(self, ctx, missionid, slotid, target=None):
        user = ctx.author
        if target != None:
            if ctx.author.guild_permissions.manage_messages != True:
                await ctx.send('You do not have permissions to remove the slot of someone other than yourself.')
                return
            user = ctx.guild.get_member(int(target.translate({ord(i): None for i in '@<>'})))
            if user == None:
                await ctx.send("Failed to find user.")
        if self.database['operations'].get(missionid) == None:
            await ctx.send(f"MissionID of {missionid} not found.")
            return
        grouplist = []
        slotdict = {}
        for group in self.database['operations'][missionid]['groups']:
            grouplist.append(group)
        for group in grouplist:
            slotdict.update(self.database['operations'][missionid]['groups'][group])
        if slotdict.get(slotid) == None:
            await ctx.send("Slot not found.")
            return
        if self.database['operations'][missionid]['assignments'].get(slotid) != None:
            await ctx.send("Please remove the person from this slot before trying to claim it.")
        self.database = self.updateDict(self.database, {'operations' : {missionid : {'assignments' : {slotid : user.id}}}})
        missionscategory = None
        for c in ctx.guild.categories:
            if c.name == 'rosters':
                missionscategory = c
                break
        if missionscategory == None:
            await ctx.send("No channel can be found for this mission can be found. Have roles been added yet?")
            return
        channel = nextcord.utils.get(ctx.guild.channels, name=f"{missionid}-{self.database['operations'][missionid]['channelname']}", category=missionscategory)
        m = await channel.history().get(author__id = self.client.user.id)
        await m.edit(self.parseRoster(ctx, missionid, grouplist))
        self.saveData()

    @commands.command(aliases=['deleteslot','delslot','removeslot','rmslot'])
    async def rslot(self, ctx, missionid, slotid):
        if self.database['operations'].get(missionid) == None:
            await ctx.send(f"MissionID of {missionid} not found.")
            return
        grouplist = []
        slotdict = {}
        for group in self.database['operations'][missionid]['groups']:
            grouplist.append(group)
        for group in grouplist:
            slotdict.update(self.database['operations'][missionid]['groups'][group])
        if slotdict.get(slotid) == None:
            await ctx.send("Slot not found.")
            return
        if self.database['operations'][missionid]['assignments'].get(slotid) != ctx.author.id:
            if ctx.author.guild_permissions.manage_messages != True:
                await ctx.send('You do not have permissions to remove the slot of someone other than yourself.')
                return
        del self.database['operations'][missionid]['assignments'][slotid]
        missionscategory = None
        for c in ctx.guild.categories:
            if c.name == 'kakapo-missions':
                missionscategory = c
                break
        if missionscategory == None:
            await ctx.send("No channel can be found for this mission can be found. Have roles been added yet?")
            return
        channel = nextcord.utils.get(ctx.guild.channels, name=f"{missionid}-{self.database['operations'][missionid]['channelname']}", category=missionscategory)
        m = await channel.history().get(author__id = self.client.user.id)
        await m.edit(self.prepareMessage(ctx, missionid, grouplist))
        self.saveData()

    # Remove mission
    @commands.command(aliases=['delmission', 'delmis', 'rmmission', 'removemission'])
    @commands.has_permissions(administrator=True)
    async def deleteMission(self, ctx, id):
        if self.database['operations'].get(id) == None:
            await ctx.send("No mission found with that ID.")
            return
        missionscategory = None
        for c in ctx.guild.categories:
            if c.name == 'kakapo-missions':
                missionscategory = c
                break
        if missionscategory != None:
            channel = nextcord.utils.get(ctx.guild.channels, name=f"{id}-{self.database['operations'][id]['channelname']}", category=missionscategory)
            if channel != None:
                await channel.delete()
                await ctx.send("Channel deleted.")
        del self.database['operations'][id]
        await ctx.send(f"{ctx.author.mention}Mission removed!")
        self.saveData()

    # Dumps data to autoSlot.json
    def saveData(self):
        with open('autoSlot.json', 'w') as f:
            json.dump(self.database, f)

    def parseRoster(self,ctx, id, group_dict):
        slots = ""
        assignments = self.database['operations'][id]['assignments']
        for group in group_dict:
            slots = slots + (f"\n**{group}:** \n")
            slotdict = self.database['operations'][id]['groups'][group]
            for slot in slotdict:
                if assignments.get(slot) == None:
                    slots = slots + (f"{slot}: {self.database['operations'][id]['groups'][group][slot]} \n")
                else:
                    slots = slots + (f"{slot}: {self.database['operations'][id]['groups'][group][slot]} - {ctx.guild.get_member(assignments.get(slot)).mention}\n")
        return f"{self.database['operations'][id]['name']} \n By: {ctx.guild.get_member(self.database['operations'][id]['author']).mention} \n {self.database['operations'][id]['date']}, {self.database['operations'][id]['time']} \n {slots}"

    # Parse inputted slots into autoSlot format
    def parseGroups(self,data):

        # Init slots dictionary
        slots = dict()

        # Break up the roles into their own groups
        groups = re.split("\. ?",data)
        for group in groups:
            # Special if statement to remove empty strings
            if len(group) < 2:
                continue
            # Split roles in a group, with the first "role" representing the group's name
            roles = re.split(": |, |\. ",group)
            # Convert roles list to dict for assignments
            roles = { role: None for role in roles[1:] }
            slots[roles[0]] = roles[1:]
            #roles = re.split(": |, |\. ",group)
            #slots[roles[0]] = roles[1:]

        return slots

    def updateDict(self,database, new_dict):
        for k, v in new_dict.items():
            if isinstance(v, collections.Mapping):
                default = v.copy()
                default.clear()
                r = self.updateDict(database.get(k, default), v)
                database[k] = r
            else:
                database[k] = v
        return database

def setup(client):
    client.add_cog(autoSlot(client))
