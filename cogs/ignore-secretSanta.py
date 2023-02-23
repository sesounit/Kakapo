import nextcord
from nextcord.ext import tasks, commands
import time
from datetime import *
import random

msg = ''
msg_id = ''
participatingList = []
b = ''
santas =[] 
guild_id = 0
messagedFlag = False

class santa(commands.Cog):
	def __init__(self, client):
		self.client = client


	@tasks.loop(seconds=10)
	async def timeCheck(self):
		global participatingList
		global guild_id
		global messagedFlag 


		t = datetime.today()
		firstPos = 0
		
		if t.month == 12:
			if t.day == 18:
				if t.hour == 00:
					if t.minute == 00:
						if participatingList != None:
							random.shuffle(participatingList)
							#337739057545347072 my id for this purpose
							if messagedFlag == False:
								for x in participatingList[:]:
									if participatingList.index(x) == 0:
										firstPos = x

									#user = server.get_member(int(x))
									server = self.client.get_guild(guild_id)
									user = server.get_member(int(x))
									#print('uuuuuju')
									#print(participatingList.index(x))
									#print('hfihjgijigj')
									#print(participatingList.index(x)+1)
									try:
										santaTarget = server.get_member(participatingList[participatingList.index(x)+1])
									except:
										santaTarget = server.get_member(firstPos)
										
									await user.send(f'Your secret santa will be {santaTarget}')
									#print(str(user)+' + '+str(santaTarget))

								messagedFlag = True


	@commands.command()
	async def secretSanta(self,context, emojiOne):
#define globals
		global msg 
		global msg_id
		global b
		global participatingList
#clear the initial message  
		await context.channel.purge(limit=1)

		b = emojiOne

#Create the reactable message.
		embedMessage = nextcord.Embed(title="S.E.S.O. 2022 Secret Santa", description="""
			On Sunday the 18th, You will receive a DM with your secret Santa.
			Gifts must be atleast $10.
			Gifts also must be submitted on the 24th of december using Steam Gift system.
			""", color=0x0E8643)
		embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")
		msg = await context.message.channel.send(embed=embedMessage)

#add the reactions to the message, if it doesnt work then state you must use emojis from this discord
		try:
			await msg.add_reaction(emojiOne)
			self.timeCheck.start()
		except:
			await context.channel.purge(limit=1)
			await context.send('Please Use emojis from this discord')

		msg_id = msg.id
#watch for a reaction.
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		global msg_id
		global msg
		global b
		global participatingList
		global guild_id
		message_id = payload.message_id
		member = payload.member

		if message_id == msg_id:

			guild_id = payload.guild_id
			#print(guild_id)
			guild = nextcord.utils.find(lambda g : g.id == guild_id, self.client.guilds)
			
		#guild_id = guild
		#print(guild.id)
		guild_id = payload.guild_id
		#print(guild_id)
		eOne = payload.emoji

		if str(eOne) == b:
			if payload.user_id == 911070041653538907:
				print('Kakapo Santa Reaction.')
			else:
				participatingList.append(payload.user_id)
				#print(participatingList)
			#print(participatingList)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		global msg_id
		global participatingList
		global b

		message_id = payload.message_id
		member = payload.member
		#print(payload)
		if message_id == msg_id:
			guild_id = payload.guild_id
			guild = nextcord.utils.find(lambda g : g.id == guild_id, self.client.guilds)

		eOne = payload.emoji

		if str(eOne) == b:
			if payload.user_id in participatingList[:]:
				participatingList.remove(payload.user_id)
				#print(participatingList)
		
	


def setup(client):
	client.add_cog(santa(client))