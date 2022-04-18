import nextcord
from nextcord.ext import commands, tasks
from dotenv import load_dotenv
import datetime
import time

load_dotenv()


class helperCommands(commands.Cog):

	def __init__ (self, client):
		self.client = client

	@commands.command()
	async def help(self, context, *, message): 

		if message:
			if 'ip' in message:
				embedMessage = nextcord.Embed(title = 'IP', description = "The IP command gives the User the IP address, port, and a short tutorial on how to join the Arma 3 Server.", color=0x0E8643)
				embedMessage.set_footer(text = "Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				await context.message.channel.send(embed = embedMessage)
			else:
				embedMessage = nextcord.Embed(title="Help", description="Please Contact a Server Admin.", color=0x0E8643)
				embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				await context.message.channel.send(embed= embedMessage)

		else:
			await context.send(f'{context.author.mention} please state what you need help with.')



	@commands.command(aliases=['ipaddress', 'ip-address'])
	async def ip(self, context):
		embedMessage = nextcord.Embed(title = "IP ADDRESS:", description = "The IP address to the server is 54.39.131.57", color=0x0E8643)
		embedMessage.add_field(name = "Main Server Port:", value = "2302.")
		embedMessage.add_field(name = "Secondary Server Port:", value = "2305.")
		embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		await context.message.channel.send(embed = embedMessage)

	@commands.command(aliases=['recruit', 'tutorial', 'getting started', 'newoperator'])
	async def new(self, context):
		embedMessage = nextcord.Embed(title = "Tutorial", description ="""
All new recruits should read the New Operative Guide. It covers everything one needs to start playing with SESO ASAP.
https://wiki.sesounit.org/tutorials_guides:operator_guide

Once you are setup, talk with <@877973354164936734> or <@877973354164936734> to play the primer mission.

The primer mission is our custom scenario showcasing our play style.
""", color=0x0E8643)
		embedMessage.set_footer(text = "Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		await context.message.channel.send(embed = embedMessage)



def setup(client):
	client.add_cog(helperCommands(client))