import nextcord, datetime, time
from nextcord.ext import commands, tasks
global activity
activity = {}
global iteration
iteration = 0
global server
server = None
#Moderation Cog
class autoAWOL(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.roleAssignment.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        global server
        server = message.guild
        role = nextcord.utils.get(server.roles, name='Operative')
        if role in message.author.roles:
            global activity
            id = message.author.id
            ms = datetime.datetime.now()
            timems = time.mktime(ms.timetuple()) * 1000
            activity[id] = timems

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        role = nextcord.utils.get(server.roles, name='Operative')
        if role in member.roles:
            global activity
            id = member.id
            ms = datetime.datetime.now()
            timems = time.mktime(ms.timetuple()) * 1000
            activity[id] = timems

    @tasks.loop(hours=168)
    async def roleAssignment(self):
        global iteration
        if iteration == 0:
            iteration = 1
        else:
            for id in activity:
                ms = datetime.datetime.now()
                timems = time.mktime(ms.timetuple()) * 1000
                if activity[id] < (timems - 3456000000):
                    user = server.get_member(id)
                    role = nextcord.utils.get(server.roles, name='AWOL')
                    await user.add_roles(role)
            operativelist = []
            operative = nextcord.utils.get(server.roles, name='Operative')
            for member in server.members:
                if operative in member.roles:
                    operativelist.append(member.id)
            for id in operativelist:
                activity.get(id)
                if id == None:
                    user = server.get_member(id)
                    role = nextcord.utils.get(server.roles, name='AWOL')
                    await user.add_roles(role)
                

        
    
def setup(client):
    client.add_cog(autoAWOL(client))