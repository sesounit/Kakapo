import discord
import typing
import emojis
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()


class ReactionRoles(commands.Cog):

	def __init__ (self, client):
		self.client = client

	msg_id = 0

	@commands.command()
	async def roleReactMessage(context):
		global msg_id
		await context.channel.purge(limit=1)
		embedMessage = discord.Embed(title="React For Roles!", description="React to get your Discord Role!", color=0x0E8643)
		embedMessage.add_field(name="Operative", value="React with :one: for the Operative Role.")
		embedMessage.add_field(name="Combat Service Support", value="React with :two: for the Combat Service Support Role.", inline=False)
		embedMessage.set_footer(text="Kakapo written by Pickle423#0408, Dildo Sagbag#8107, Fletch#0617.")

		msg = await context.message.channel.send(embed=embedMessage)
		await msg.add_reaction('1️⃣')
		await msg.add_reaction('2️⃣')
		msg_id = msg.id
		#print(msg_id)


	@commands.Cog.listener
	async def on_raw_reaction_add(payload):
		global msg_id
		role = None
		message_id = payload.message_id
		#print(message_id)
		#print(msg_id)
		if message_id == msg_id:
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
			#print(payload.emoji.name)
			if payload.emoji.name == '1️⃣':
			
				role = discord.utils.get(guild.roles, name = 'Operator')
				member = payload.member
				await member.add_roles(role)
				#print(f'giving {member} role')

			if payload.emoji.name == '2️⃣':
				role = discord.utils.get(guild.roles, name = 'Combat Service Support')
				member = payload.member
				await member.add_roles(role)


	@commands.Cog.listener
	async def on_raw_reaction_remove(payload):
		global msg_id
		
		message_id = payload.message_id
		#print(msg_id)
		if message_id == msg_id:
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

			if payload.emoji.name == '1️⃣':
				role = discord.utils.get(guild.roles, name = 'Operator')
				member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
				await member.remove_roles(role)

			elif payload.emoji.name == '2️⃣':
				role = discord.utils.get(guild.roles, name = 'Combat Service Support')
				member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
				await member.remove_roles(role)

			


def setup(client):
	client.add_cog(ReactionRoles(client))
