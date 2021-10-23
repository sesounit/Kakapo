import discord, requests
from discord.ext import commands
import random
class miscCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Simple Ping Check
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
    #Sus
    @commands.command()
    async def sus(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send('Silence', delete_after=3)

    @commands.command(aliases=['8ball', 'eightball'])
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.', 'It is decidedly so.', 'Without a doubt', 'Yes - definitely.', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', "Don't count on it.", 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    #Calculate
    @commands.command()
    async def calculate(self, ctx, query_first, query_operator, query_second):
        query_first = int(query_first)
        query_second = int(query_second)
        if (query_operator) == ('+'):
            await ctx.send(query_first + query_second)
        elif (query_operator) == ('-'):
            await ctx.send(query_first - query_second)
        elif (query_operator) == ('*'):
            await ctx.send(query_first * query_second)
        elif (query_operator) == ('/'):
            await ctx.send(query_first / query_second)
        else:
            ctx.send('Calculation failed, remember to use +, -, *, or /, as well as spacing out the request.')
    
            ''' Future-proofing this command. Python 3.10 has a match-case function that we will use when we switch to 3.10
            match query_operator:
                case '+':
                    await ctx.send(query_first + query_second)
                case '-':
                    await ctx.send(query_first - query_second)
                case '*':
                    await ctx.send(query_first * query_second)
                case '/':
                    await ctx.send(query_first / query_second)
                case _:
                    ctx.send('Calculation failed, remember to use +, -, *, or /, as well as spacing out the request.')
        '''

    @commands.command(name='version')
    async def version(self, context):

        mainEmbed = discord.Embed(title="Kakapo Version Notes", description="SESO's Multi-Use Discord Bot", color=0x0E8643)
        mainEmbed.add_field(name="Changes:", value="Music can now be searched for via text, music quality of life additions.")
        mainEmbed.add_field(name="Version Code:", value="v0.9.3", inline=False)
        mainEmbed.add_field(name="Date Released:", value="October 21, 2021", inline=False)
        mainEmbed.set_footer(text="Kakapo written by Pickle423#0408, Fletch#0617, Dildo Sagbag#8107.")

        await context.message.channel.send(embed=mainEmbed)

def setup(client):
    client.add_cog(miscCommands(client))
