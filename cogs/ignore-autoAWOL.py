import nextcord, datetime, time, json, os
from nextcord.ext import commands, tasks
global activity
activity = {}
global server
server = None
global awoltime
guild_id = 451714596227645441
awoltime = 3456000000
awoldmtext = f"**Due to your inactivity in [S.E.S.O.] Casual Milsim, you have been issued the AWOL Role.** \nThis is done in order to help keep the discord tidy. \nThis does not mean that you’re not welcome back! You can always ask any member of operations command/command consultant to remove AWOL and/or put you under a spectator role, Combat Service Support. \nDo recognize however, if OpsComm do not hear from you soon, you may be removed from the server or moved to CSS. \n*This action was performed automatically, replying to this DM will do nothing.*"
#autoAWOL Cog
class autoAWOL(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        #Read the pre-existing activity JSON
        global activity
        if os.path.exists('autoSlot.json'):
            with open('activity-dump.json') as json_file:
                activity = json.load(json_file)
        await self.roleAssignment.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            global server
            role = nextcord.utils.get(server.roles, name='Operative')
            if role in message.author.roles:
                global activity
                id = message.author.id
                ms = datetime.datetime.now()
                timems = time.mktime(ms.timetuple()) * 1000
                activity[str(id)] = str(timems)
        except:
            pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        role = nextcord.utils.get(server.roles, name='Operative')
        if role in member.roles:
            global activity
            id = member.id
            ms = datetime.datetime.now()
            timems = time.mktime(ms.timetuple()) * 1000
            activity[str(id)] = str(timems)

    @tasks.loop(seconds=20)
    async def roleAssignment(self):
        global activity
        global server
        global awoltime
        if server == None:
            server = self.client.get_guild(guild_id)
        #If this is the first time the function has been called, then everyone not previously logged is logged as having activity at this time.
        for id in activity:
            ms = datetime.datetime.now()
            timems = (time.mktime(ms.timetuple()) * 1000)
            if not id == 'place':
                lastactive = activity[id]
                lastactive = int(float(lastactive))
                if lastactive < (timems - awoltime):
                    user = server.get_member(int(id))
                    role = nextcord.utils.get(server.roles, name='AWOL')
                    loa = nextcord.utils.get(server.roles, name='LOA')
                    if loa not in user.roles:
                        if role not in user.roles:
                            await user.add_roles(role)
                            await user.send(awoldmtext)
        operativelist = []
        operative = nextcord.utils.get(server.roles, name='Operative')
        css = nextcord.utils.get(server.roles, name='Combat Service Support')
        bot = nextcord.utils.get(server.roles, name='Bot')
        for member in server.members:
            if operative in member.roles:
                operativelist.append(member.id)
            if operative not in member.roles and css not in member.roles and bot not in member.roles:
                operativelist.append(member.id)
        for id in operativelist:
            if str(id) not in activity:
                ms = datetime.datetime.now()
                timems = time.mktime(ms.timetuple()) * 1000
                activity[str(id)] = str(timems)
        #Dump data into a JSON every call.
        with open('activity-dump.json', 'w') as f:
            json.dump(activity, f)
                

        
    
def setup(client):
    client.add_cog(autoAWOL(client))