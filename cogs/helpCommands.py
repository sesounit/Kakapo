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
			elif 'time' in message:
				embedMessage = nextcord.Embed(title = 'Time', description = 'The Time command gives the User the time in all different time zones.', color=0x0E8643)
				embedMessage.set_footer(text = "Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				await context.message.channel.send(embed = embedMessage)
			elif 'modlist' in message:
				embedMessage = nextcord.Embed(title = 'ModList', description = 'The Modlist Command shows you where to find the ModLists for operations.', color=0x0E8643)
				embedMessage.set_footer(text = "Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				await context.message.channel.send(embed = embedMessage)
			else:
				embedMessage = nextcord.Embed(title="Help", description="Plaese Contact a Server Admin.", color=0x0E8643)
				embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				await context.message.channel.send(embed= embedMessage)

		else:
			await context.send(f'{context.author.mention} please state what you need help with.')



	@commands.command(aliases=['ipaddress', 'ip-address'])
	async def ip(self, context):
		embedMessage = nextcord.Embed(title = "IP ADDRESS:", description = "The IP address to the server is 173.208.192.234", color=0x0E8643)
		embedMessage.add_field(name = "Main Server Port:", value = "2302.")
		embedMessage.add_field(name = "Secondary Server Port:", value = "2305.")

		embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		await context.message.channel.send(embed = embedMessage)


	@commands.command(aliases=['timezone', 'timezones'])
	async def time(self, context, *, message = None):
		def fuckTwentyFourHourClocksWhyCantTheyJustBeOneMillionHoursLongLikeWhyDoIHaveToWrapThisAroundToWorkIHateMyLifeHeySiriHowDoITieANoose(timeOne, timeDifference):
			base = 2400
			if int(timeOne) + timeDifference*100 > base:
				newTime = str((base-int(timeOne))+(timeDifference*100))

				if int(newTime) < 1000:
					newTime = '0' + newTime

				newTime = newTime[:2] + ":" + newTime[2:]
				return newTime

			elif int(timeOne) + timeDifference*100 < 0:
				newTime = str((base + int(timeOne)) + timeDifference*100)

				newTime = newTime[:2] + ":" + newTime[2:]
				return newTime

			else:
				newTime = str(int(timeOne) + (timeDifference*100))
				if int(newTime) < 1000:
					newTime = '0' + newTime

				newTime = newTime[:2] + ":" + newTime[2:]
				return newTime

		timeZone = ''
		if message == None:
			timenow = datetime.datetime.now()
			embedMessage = nextcord.Embed(title = 'Time Zones', description = 'Here is a list of different time zones based on the current time.', color=0x0E8643)
			embedMessage.add_field(name="PST (UTC-7)", value=f"{timenow.hour-3}:{timenow.minute}:{timenow.second}")
			embedMessage.add_field(name="MST (UTC-6)", value=f"{timenow.hour-2}:{timenow.minute}:{timenow.second}")
			embedMessage.add_field(name="CST (UTC-5)", value=f"{timenow.hour-1}:{timenow.minute}:{timenow.second}")
			embedMessage.add_field(name="EST (UTC-4)", value=f"{timenow.hour}:{timenow.minute}:{timenow.second}")
			embedMessage.add_field(name="UTC", value=f"{timenow.hour+4}:{timenow.minute}:{timenow.second}")
			embedMessage.add_field(name="BST (UTC+1)", value=f"{timenow.hour+5}:{timenow.minute}:{timenow.second}")
			embedMessage.add_field(name="CEST (UTC+2)", value=f"{timenow.hour+6}:{timenow.minute}:{timenow.second}")
			embedMessage.add_field(name="MSK (UTC+3)", value=f"{timenow.hour+7}:{timenow.minute}:{timenow.second}")
			embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
			await context.message.channel.send(embed = embedMessage)
			#print(timenow.hour)
			#print(timenow.minute)
			#print(timenow.second)

		else:

			for x in message[:]:
				if x == ":":
					newMessage = message.replace(x, '')
					for x in newMessage[:]:
						if x == " ":
							newMessage = newMessage.replace(newMessage[newMessage.index(x):], '')

			for x in message[:]:
				if x == " ":
					timeZone = message[message.index(x)+1:]
					#newMessage.replace()

			if timeZone.lower() == 'est':
				timeValue = fuckTwentyFourHourClocksWhyCantTheyJustBeOneMillionHoursLongLikeWhyDoIHaveToWrapThisAroundToWorkIHateMyLifeHeySiriHowDoITieANoose(newMessage, -4)
				embedMessage = nextcord.Embed(title = 'Time Zones', description = 'Here is the time conversion from UTC to EST.', color=0x0E8643)
				embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				embedMessage.add_field(name="EST (UTC-4)", value = f"{timeValue}")
				await context.message.channel.send(embed = embedMessage)

			if timeZone.lower() == 'pst':
				timeValue = fuckTwentyFourHourClocksWhyCantTheyJustBeOneMillionHoursLongLikeWhyDoIHaveToWrapThisAroundToWorkIHateMyLifeHeySiriHowDoITieANoose(newMessage, -7)
				embedMessage = nextcord.Embed(title = 'Time Zones', description = 'Here is the time conversion from UTC to PST.', color=0x0E8643)
				embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				embedMessage.add_field(name="PST (UTC-7)", value = f"{timeValue}")
				await context.message.channel.send(embed = embedMessage)

			if timeZone.lower() == 'mst':
				timeValue = fuckTwentyFourHourClocksWhyCantTheyJustBeOneMillionHoursLongLikeWhyDoIHaveToWrapThisAroundToWorkIHateMyLifeHeySiriHowDoITieANoose(newMessage, -6)
				embedMessage = nextcord.Embed(title = 'Time Zones', description = 'Here is the time conversion from UTC to MST.', color=0x0E8643)
				embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				embedMessage.add_field(name="MST (UTC-6)", value = f"{timeValue}")
				await context.message.channel.send(embed = embedMessage)

			if timeZone.lower() == 'cst':
				timeValue = fuckTwentyFourHourClocksWhyCantTheyJustBeOneMillionHoursLongLikeWhyDoIHaveToWrapThisAroundToWorkIHateMyLifeHeySiriHowDoITieANoose(newMessage, -5)
				embedMessage = nextcord.Embed(title = 'Time Zones', description = 'Here is the time conversion from UTC to CST.', color=0x0E8643)
				embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				embedMessage.add_field(name="CST (UTC-5)", value = f"{timeValue}")
				await context.message.channel.send(embed = embedMessage)

			if timeZone.lower() == 'bst':
				timeValue = fuckTwentyFourHourClocksWhyCantTheyJustBeOneMillionHoursLongLikeWhyDoIHaveToWrapThisAroundToWorkIHateMyLifeHeySiriHowDoITieANoose(newMessage, 1)
				embedMessage = nextcord.Embed(title = 'Time Zones', description = 'Here is the time conversion from UTC to BST.', color=0x0E8643)
				embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				embedMessage.add_field(name="BST (UTC+1)", value = f"{timeValue}")
				await context.message.channel.send(embed = embedMessage)

			if timeZone.lower() == 'cest':
				timeValue = fuckTwentyFourHourClocksWhyCantTheyJustBeOneMillionHoursLongLikeWhyDoIHaveToWrapThisAroundToWorkIHateMyLifeHeySiriHowDoITieANoose(newMessage, 2)
				embedMessage = nextcord.Embed(title = 'Time Zones', description = 'Here is the time conversion from UTC to CEST.', color=0x0E8643)
				embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				embedMessage.add_field(name="CEST (UTC+2)", value = f"{timeValue}")
				await context.message.channel.send(embed = embedMessage)

			if timeZone.lower() == 'msk':
				timeValue = fuckTwentyFourHourClocksWhyCantTheyJustBeOneMillionHoursLongLikeWhyDoIHaveToWrapThisAroundToWorkIHateMyLifeHeySiriHowDoITieANoose(newMessage, 3)
				embedMessage = nextcord.Embed(title = 'Time Zones', description = 'Here is the time conversion from UTC to MSK.', color=0x0E8643)
				embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
				embedMessage.add_field(name="MSK (UTC+3)", value = f"{timeValue}")
				await context.message.channel.send(embed = embedMessage)

			

			#print(timeZone)
			#print(newMessage)




	@commands.command(aliases=['mod', 'mods', 'modlists', 'mod-list', 'mod-lists'])
	async def modlist(self, context):
		embedMessage = nextcord.Embed(title = 'ModList', description = "All of the Engagement Modlists can be found in #mod-list.", color=0x0E8643)
		embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		await context.message.channel.send(embed = embedMessage)

	@commands.command(aliases=['teamspeak3', 'ts', 'ts3'])
	async def teamspeak(self, context):
		embedMessage = nextcord.Embed(title = 'Teamspeak', description = "All of the TeamSpeak info can be found in #teamspeak-info.", color=0x0E8643)
		embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		await context.message.channel.send(embed = embedMessage)

	@commands.command(aliases=['acre2', 'radio'])
	async def acre(self, context):
		embedMessage = nextcord.Embed(title = 'Acre', description = "The Acre2 Installation tutorial can be found in #acre2-info", color=0x0E8643)
		embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		await context.message.channel.send(embed = embedMessage)

	@commands.command(aliases=['tfarvsacre', 'acrevstfar'])
	async def tfar(self, context):
		embedMessage = nextcord.Embed(title = 'TFAR', description = "S.E.S.O. unfortunately does not use TFAR. Instead we use ACRE 2.", color=0x0E8643)
		embedMessage.set_footer(text = "Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		await context.message.channel.send(embed = embedMessage)

	@commands.command(aliases=['tactics', 'manual', 'manuals'])
	async def training(self, context):
		embedMessage = nextcord.Embed(title = "Manuals", description ="All of our Unit's Manuals can be found in #manuals.", color=0x0E8643)
		embedMessage.set_footer(text = "Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		await context.message.channel.send(embed = embedMessage)

	@commands.command(aliases=['emblem', 'unitemblem', 'unitlogo', 'patch', 'unitpatch'])
	async def logo(self, context):
		embedMessage = nextcord.Embed(title = "Embelm", description ="S.E.S.O.'s unit emblem can be found in #ingame-emblem", color=0x0E8643)
		embedMessage.set_footer(text = "Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		await context.message.channel.send(embed = embedMessage)

	@commands.command(aliases=['unitrules'])
	async def rules(self, context):
		embedMessage = nextcord.Embed(title = "Rules", description ="The Rules to S.E.S.O. operations and nextcord can be found in #unit-rules.", color=0x0E8643)
		embedMessage.set_footer(text = "Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		await context.message.channel.send(embed = embedMessage)

	@commands.command(aliases=['nextcord', 'howtouse'])
	async def new(self, context):
		embedMessage = nextcord.Embed(title = "Tutorial", description ="""
Bulletin Board
#announcements - Contains unit-wide announcements and non-Arma events
#engagement-announcements - Contains Arma 3 engagements from hosts such as Operations Hosts, and Engagements Hosts. Only pings Operators so make sure to get the right role in #2 
#dev-announcements - Contains Bohemia Interactive's updates about the Arma franchise's development

Tutorials & Info
#mod-list - Contains mod presets for various operations and missions
#teamspeak-info - Tutorial on setting up Teamspeak 3 for SESO
#ingame-emblem - Tutorial on setting up a SESO emblem on your in-game avatar
#acre2-info - Tutorial on setting up ACRE2
#manuals - In-depth documents about best practices

General Text Channels
#introduce-yourself - Channel for newcomers
#general - General text chat. Feel free to open thread here
#nsfw-memes-no-porn - Channel to post one's memes. Does not have to be NSFW, can be SFW too
#screenshots-n-videos - Post Arma 3 media here
#loa - Report LOA (Leave of Absence) for when you are away for any period of time
#suggestions - Suggest anything to Operations Command regarding SESO
#operation-feedback - Provide feedback for host's operations and engagements
#bot-commands - Command the Discord bots here

General Voice Channels
- Contain voice channels for casual use""", color=0x0E8643)
		embedMessage.set_footer(text = "Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		await context.message.channel.send(embed = embedMessage)



def setup(client):
	client.add_cog(helperCommands(client))