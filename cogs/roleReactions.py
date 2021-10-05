import discord
import typing
import emojis
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()


class ReactionRoles(commands.Cog):

	def __init__ (self, client):
		self.client = client


	@commands.Cog.listener
	async def on_raw_reaction_add(self, payload):
		message_id = payload.message_id
		if message_id == 894746857610297354:
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

			if payload.emoji.name == 'INSERT EMOJI NAME':
				role = discord.utils.get(guild.roles, name = 'INSERT ROLE NAME')

			member = payload.member
			await member.add_roles(role)


	@commands.Cog.listener
	async def on_raw_reaction_remove(self, payload):
		message_id = payload.message_id
		if message_id == 894746857610297354:
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

			if payload.emoji.name == 'INSERT EMOJI NAME':
				role = discord.utils.get(guild.roles, name = 'INSERT ROLE NAME')

			member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
			await member.remove_roles(role)



def setup(client):
	client.add_cog(ReactionRoles(client))