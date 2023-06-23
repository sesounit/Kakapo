import nextcord, random
from nextcord.ext import commands, tasks
filepath = '~/serverfiles/mpmissions/'

#Mission Upload cog
class missionUpload(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def cog_check(self, ctx):
        #Check if user has requisite roles
        ch = nextcord.utils.get(ctx.guild.roles, name='Campaign Host')
        oh = nextcord.utils.get(ctx.guild.roles, name='Operation Host')
        if ch in ctx.author.roles or oh in ctx.author.roles or ctx.author.guild_permissions.administrator:
            return True
        return False

    @commands.command(aliases=['serverUpload', 'um', 'su'])
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
        await ctx.send("Filetype is incorrect, please only upload pbo's.")


def setup(client):
    client.add_cog(missionUpload(client))
