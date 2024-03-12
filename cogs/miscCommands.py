import nextcord
from nextcord.ext import commands
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

        mainEmbed = nextcord.Embed(title="Kakapo Version Notes", description="SESO's Multi-Use Discord Bot", color=0x0E8643)
        mainEmbed.add_field(name="Changes:", value=f"New host tools including reminders and automatic event creation added. \nMusic streaming now supports youtube playlists and will disconnect if left alone in a channel. \nWar Photographers can now upload up to 10 images at a time, as opposed to the previous 1.")
        mainEmbed.add_field(name="Version Code:", value="v1.6.0", inline=False)
        mainEmbed.add_field(name="Date Released:", value="February 28, 2024", inline=False)
        mainEmbed.set_footer(text="Kakapo written by pickle423, dildo_sagbag, masterchiefcw, f13tch")

        await context.message.channel.send(embed=mainEmbed)

    @commands.command(aliases=["d", "rolldice", "roll"])
    async def dice(self, ctx, max, operator=None, *, operatornumber=None):
        try:
            dice=int(operator)
            operatorisdicecount = True
        except:
            operatorisdicecount = False
        max = int(max)
        if operatorisdicecount == True:
            whileloop = 0
            diceresults = []
            while whileloop < dice:
                whileloop = whileloop + 1
                diceresults.append(random.randrange(1, max))
            await ctx.send(f"Rolled {operator}d{max} {diceresults}")
        elif operator == None:
            await ctx.send(f"Rolled 1d{max} {random.randrange(1, max)}")
        elif operator == '*':
            await ctx.send(f"Rolled 1d{max} {random.randrange(1, max) * int(operatornumber)}")
        elif operator == '+':
            await ctx.send(f"Rolled 1d{max} {random.randrange(1, max) + int(operatornumber)}")
        elif operator == '-':
            await ctx.send(f"Rolled 1d{max} {random.randrange(1, max) - int(operatornumber)}")
        elif operator == '/':
            await ctx.send(f"Rolled 1d{max} {random.randrange(1, max) / int(operatornumber)}")

def setup(client):
    client.add_cog(miscCommands(client))
