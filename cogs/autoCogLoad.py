import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

from github import Github

g = Github('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')
cogsList = []

for repo in g.get_user().get_repos():
	if repo.name == "Kakapo":
		for x in repo.get_contents("cogs"):
			cogsList.append(x)

		print(cogsList)



while True:
	for repo in g.get_user().get_repos():
		if repo.name == "Kakapo":
			for x in repo.get_contents("cogs"):
				if x not in cogsList[:]:
					print(x)
					
    

