import nextcord, random
from nextcord.ext import commands, tasks
filepath = '~/serverfiles/mpmissions/'

#Mission Upload cog
class missionUpload(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['serverUpload', 'um', 'su'])
    @commands.has_any_role("Operations Command", "Command Consultant", "Campaign Host", "Operation Host")
    async def uploadMission(self, ctx):
        messages = await ctx.channel.history(limit=2).flatten()
        if len(ctx.message.attachments) < 2 and len(ctx.message.attachments) > 0:
            attachment = ctx.message.attachments[0]
            if 'pbo' in attachment.filename:
                await attachment.save(f'{filepath}/{ctx.author.name}-{attachment.filename}')
                await ctx.send(f'{ctx.author.mention} has uploaded {attachment.filename} to the server.')
                return
        else:
            await ctx.send("Either too many attachments found, or none found.")
            return
        await ctx.send("File type is incorrect, please only upload pbos.")


def setup(client):
    client.add_cog(missionUpload(client))
