import nextcord
from nextcord.ext import commands

#welcomeMessage Cog
class WelcomeMessage(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        global welcomemessagechannel
        channel = nextcord.utils.get(member.guild.text_channels, name="lobby")
        server = member.guild
        sag = server.get_member(68019210814500864)
        ryder = server.get_member(397573639785938945)
        await channel.send(f"{member.mention}, welcome to [S.E.S.O.] Casual Milsim. \n \n See Channels & Roles to choose your roles.  \n \nIf you are new to Arma 3, see the New Operative Guide to get started: \nhttps://wiki.sesounit.org/guides/new_operative")

def setup(client):
    client.add_cog(WelcomeMessage(client))