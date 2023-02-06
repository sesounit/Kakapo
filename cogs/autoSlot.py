import nextcord, sys, datetime, json, collections, os.path
from nextcord.ext import commands

global database
database = {'operations' : {},'highest_mission_id' : 0}
#autoSlot Cog
class autoSlot(commands.Cog):
    def __init__(self, client):
        self.client = client
    
     
    @commands.Cog.listener()
    async def on_ready(self):
        #Read the pre-existing JSON
        global database
        if os.path.exists('autoSlot.json'):
            with open('autoSlot.json') as json_file:
                database = json.load(json_file)
                print(database)

    @commands.command(name = "addMission", help = "Adds a new mission with given name. Use quotations for multi-word names")
    @commands.has_permissions(administrator=True)
    async def addMission(self, ctx, mission: str, date: str, time: str):
        global database
        #Make channel name that is compatible with discord's channel restrctions
        c = nameconvert(mission)
        missionoriginal = mission
        if (mission != c):
            await ctx.send("{} Your mission's channel will be renamed from {} to {}".format(ctx.author.mention, mission, c))
            mission = c

        highest_mission_id = database['highest_mission_id']
        mission_id = str(highest_mission_id + 1)
        database['operations'].update({mission_id : {'groups' : {},'assignments' : {}, 'channelname' : mission, 'name' : missionoriginal,'author' : ctx.author.id,'date' : date,'time' : time} })

        send_message = "{} Your mission ID for {} is: {}".format(ctx.author.mention, mission, mission_id)
        highest_mission_id = highest_mission_id + 1
        database.update({'highest_mission_id' : highest_mission_id})
        await ctx.send(send_message)
        saveData()

    @commands.command(name = "addslots")
    @commands.has_permissions(administrator=True)
    async def addSlots(self, ctx, id, *, slots):
        global database
        try:
            if id not in database['operations']:
                await ctx.send("There is no mission present in the database with this ID.")
                return
        except:
            await ctx.send("A problem occured with the mission id.")
            return
        grouplist, groupdict = parser(slots)
        if grouplist == False:
            await ctx.send("Your request did not match the required formatting, please check your input for issues.")
            return
        database = update_dict(database, {'operations' : {id : {'groups' : groupdict}}})
        server = ctx.guild
        categories = server.categories
        missionscategory = None
        missionchannel = None
        cname = database['operations'][id]['channelname']
        for c in categories:
            if c.name == 'kakapo-missions':
                missionscategory = c
                break
        if missionscategory == None:
            missionscategory = await server.create_category('kakapo-missions')
        else:
            for c in missionscategory.channels:
                if c.name == (f"{id}-{cname}"):
                    missionchannel = c
                    break
        if missionchannel == None:
            missionchannel = await missionscategory.create_text_channel(f'{id}-{cname}')
            await missionchannel.send(preparemessage(ctx, id, grouplist))
        else:
            m = await missionchannel.history().get(author__id = self.client.user.id)
            await m.edit(preparemessage(ctx, id, grouplist))
        saveData()

    @commands.command(aliases=['takeslot', 'claimslot', 'cslot', 'tslot', 'slot','assignslot'])
    async def aslot(self, ctx, missionid, slotid, target=None):
        global database
        user = ctx.author
        if target != None:
            if ctx.author.guild_permissions.manage_messages != True:
                await ctx.send('You do not have permissions to remove the slot of someone other than yourself.')
                return
            user = ctx.guild.get_member(int(target.translate({ord(i): None for i in '@<>'})))
            if user == None:
                await ctx.send("Failed to find user.")         
        if database['operations'].get(missionid) == None:
            await ctx.send(f"MissionID of {missionid} not found.")
            return
        grouplist = []
        slotdict = {}
        for group in database['operations'][missionid]['groups']:
            grouplist.append(group)
        for group in grouplist:
            slotdict.update(database['operations'][missionid]['groups'][group])
        if slotdict.get(slotid) == None:
            await ctx.send("Slot not found.")
            return
        database = update_dict(database, {'operations' : {missionid : {'assignments' : {slotid : user.id}}}})
        missionscategory = None
        for c in ctx.guild.categories:
            if c.name == 'kakapo-missions':
                missionscategory = c
                break
        if missionscategory == None:
            await ctx.send("No channel can be found for this mission can be found. Have roles been added yet?")
            return
        channel = nextcord.utils.get(ctx.guild.channels, name=f"{missionid}-{database['operations'][missionid]['channelname']}", category=missionscategory)
        m = await channel.history().get(author__id = self.client.user.id)
        await m.edit(preparemessage(ctx, missionid, grouplist))
        saveData()

    @commands.command(aliases=['deslot','removeslot'])
    async def rslot(self, ctx, missionid, slotid):
        global database
        if database['operations'].get(missionid) == None:
            await ctx.send(f"MissionID of {missionid} not found.")
            return
        grouplist = []
        slotdict = {}
        for group in database['operations'][missionid]['groups']:
            grouplist.append(group)
        for group in grouplist:
            slotdict.update(database['operations'][missionid]['groups'][group])
        if slotdict.get(slotid) == None:
            await ctx.send("Slot not found.")
            return
        if database['operations'][missionid]['assignments'].get(slotid) != ctx.author.id:
            if ctx.author.guild_permissions.manage_messages != True:
                await ctx.send('You do not have permissions to remove the slot of someone other than yourself.')
                return
        del database['operations'][missionid]['assignments'][slotid]
        missionscategory = None
        for c in ctx.guild.categories:
            if c.name == 'kakapo-missions':
                missionscategory = c
                break
        if missionscategory == None:
            await ctx.send("No channel can be found for this mission can be found. Have roles been added yet?")
            return
        channel = nextcord.utils.get(ctx.guild.channels, name=f"{missionid}-{database['operations'][missionid]['channelname']}", category=missionscategory)
        m = await channel.history().get(author__id = self.client.user.id)
        await m.edit(preparemessage(ctx, missionid, grouplist))
        saveData()

    @commands.command(aliases=['delmission', 'delmis', 'rmmission', 'removemission'])
    @commands.has_permissions(administrator=True)
    async def deletemission(self, ctx, id):
        global database
        if database['operations'].get(id) == None:
            await ctx.send("No mission found with that ID.")
            return
        missionscategory = None
        for c in ctx.guild.categories:
            if c.name == 'kakapo-missions':
                missionscategory = c
                break
        if missionscategory != None:
            channel = nextcord.utils.get(ctx.guild.channels, name=f"{id}-{database['operations'][id]['channelname']}", category=missionscategory)
            if channel != None:
                await channel.delete()
                await ctx.send("Channel deleted.")
        del database['operations'][id]
        await ctx.send(f"{ctx.author.mention}Mission removed!")
        saveData()

#Centralized function for saving data.
def saveData():
    with open('autoSlot.json', 'w') as f:
        json.dump(database, f)

def preparemessage(ctx, id, grouplist):
    slots = ""
    assignments = database['operations'][id]['assignments']
    for group in grouplist:
        slots = slots + (f"\n**{group}:** \n")
        slotdict = database['operations'][id]['groups'][group]
        for slot in slotdict:
            if assignments.get(slot) == None:
                slots = slots + (f"{slot}: {database['operations'][id]['groups'][group][slot]} \n")
            else:
                slots = slots + (f"{slot}: {database['operations'][id]['groups'][group][slot]} - {ctx.guild.get_member(assignments.get(slot)).mention}\n")
    message = f"{database['operations'][id]['name']} \n By: {ctx.guild.get_member(database['operations'][id]['author']).mention} \n {database['operations'][id]['date']}, {database['operations'][id]['time']} \n {slots}"
    return message

def parser(data):
    '''
    if ':' or '.' not in data:
        return False, False
    '''
    if data[-1] == ',':
        data = data.rstrip(data[-1])
        data = data + '.'
    elif data[-1] != '.':
        data = data + '.'
    datalist = data.split(" ")
    temp = ""
    grouplist = []
    templist = []
    groupdict = {}
    for i in datalist:
        temp = temp + f'{i} '
        if ':' in i:
            temp = temp.rstrip(temp[-1])
            temp = temp.rstrip(temp[-1])
            grouplist.append(temp)
            groupdict.update({temp : 'placeholder'})
            temp = ""
        if ',' in i:
            temp = temp.rstrip(temp[-1])
            temp = temp.rstrip(temp[-1])
            if temp != "":
                templist.append(temp)
                temp = ""
        if '.' in i:
            temp = temp.rstrip(temp[-1])
            temp = temp.rstrip(temp[-1])
            if temp != "":
                templist.append(temp)
                if len(grouplist) > 0:
                    groupdict.update({grouplist[len(grouplist) - 1] : templist})
                else:
                    groupdict.update({grouplist[0] : templist})
                temp = ""
                templist = []
    groupalt = {}
    slots = {}
    slotcounter = 1
    for group in grouplist:
        for slot in groupdict[group]:
            slots.update({str(slotcounter) : slot})
            slotcounter = slotcounter + 1
        groupalt.update({group : slots})
        slots = {}
    groupdict = groupalt
    '''
    if temp != "":
        temp = temp.rstrip(temp[-1])
        roledict.update({temp : grouplist[len(grouplist) - 1]})
        temp = ""
        '''
    return grouplist, groupdict

def update_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            default = v.copy()
            default.clear()
            r = update_dict(d.get(k, default), v)
            d[k] = r
        else:
            d[k] = v
    return d

def nameconvert(name):
    return name.replace(" ", "-").lower()

def setup(client):
    client.add_cog(autoSlot(client))
