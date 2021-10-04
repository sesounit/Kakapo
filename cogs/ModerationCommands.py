import discord
from discord.ext import commands
#Moderation Cog
class Moderation(commands.Cog):
    def _init_(self, client):
        self.client = client
    async def cog_check(self, ctx):
        #Check if user has admin role
        return ctx.author.guild_permissions.manage_messages
    @commands.command()
    @commands.has_role("Operations Command")
    async def clean(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send("Messages have been removed!", delete_after=5)
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
        
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
                return

def setup(client):
    client.add_cog(Moderation(client))