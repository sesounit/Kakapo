import discord
from discord.ext import commands
#welcomeMessage Cog
class welcomeMessage(commands.Cog):
    def _init_(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        global welcomemessagechannel
        channel = discord.utils.get(member.guild.text_channels, name="introduce-yourself")
        await channel.send(f"Hey {member.mention}, welcome to [S.E.S.O.] Casual Milsim. \n \n Here are some questions you could answer: \n  1. Are you familiar with Arma and MilSims? \n  2. What military roles do you most enjoy? \n  3. And a fun unique fact about yourself. \n \n Feel free to strike up a conversation and to look at #react-for-roles to choose between Operative meaning you'll participate in Ops, and Combat Service Support, which is essentially spectator.  Keep in mind if you do not react to any of them, You will be unable to see all of the channels. \n \n If you are new to Arma and interested in getting some training, react to the role, 'Wants training'. You'll receive pings for any upcoming training that will go over Squad tactics, ACE Medical, and more. \n \n Feel free to ping and approach any of the Operations Command or Command Consultant Host for help.") 

def setup(client):
    client.add_cog(welcomeMessage(client))