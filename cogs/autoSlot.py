import nextcord, sys, datetime, json, collections, os.path
from nextcord.ext import commands

global database
database = {'operations' : {},'highest_mission_id' : 1}
highest_mission_id = 1
#autoSlot Cog
class autoSlot(commands.Cog):
    def __init__(self, client):
        self.client = client
    
     
    @commands.Cog.listener()
    async def on_ready(self):
        #Read the pre-existing activity JSON
        global database
        if os.path.exists('autoSlot.json'):
            with open('autoSlot.json') as json_file:
                database = json.load(json_file)

    @commands.command(name = "addMission", help = "Adds a new mission with given name. Use quotations for multi-word names")
    async def addMission(self, ctx, mission: str, date: str, time: str):
        global highest_mission_id
        # name must be compatible with discord channel name restrictions
        c = name_convert(mission)
        # if not tell the user how is the converted version
        if (mission != c):
            send_message = "{} Your mission will be renamed from >{}< to >{}<".format(ctx.author.mention, mission, c)
            await ctx.send(send_message)
            mission = c

        # Adding the new entry inside the missions table with given name and highest + 1 mission_id
        mission_id = highest_mission_id + 1
        database['operations'].update({mission_id : {'groups' : {},'name' : mission,'author' : ctx.author,'date' : date,'time' : time} })

        # Sending a message to the client with creation information
        send_message = "{} Your mission ID for >{}< is: {}".format(ctx.author.mention, mission, mission_id)
        highest_mission_id = mission_id
        database.update({'highest_mission_id' : highest_mission_id})
        await ctx.send(send_message)

    @commands.command(name = "addslots")
    async def addSlots(self, ctx, id, *, slots):
        global database
        try:
            id = (int(id))
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

        print(update_dict(database, {'operations' : {id : {'groups' : groupdict}}}))

        



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

def name_convert(name):
    """
    return will be name, but compatible with discord channel name restrictions
    """
    return name.replace(" ", "-").lower()

def setup(client):
    client.add_cog(autoSlot(client))
