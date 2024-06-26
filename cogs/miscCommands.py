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
        mainEmbed.add_field(name="Changes:", value=f"Launched compliance concern report form, operatives can now discretely submit concerns when they give feedback. \n .1 Patch allows forms to be fixed after bot restart.")
        mainEmbed.add_field(name="Version Code:", value="v1.7.1", inline=False)
        mainEmbed.add_field(name="Date Released:", value="April 20, 2024", inline=False)
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

    @commands.command()
    async def loa(self, ctx, target=None):
        if target:
            if (len([x for x in ctx.author.roles if x in ["Operations Command", "Command Consultant"]]) > 0):
                return await ctx.send(f'{ctx.author.mention} is not an admin. Only admins can assign others LOA.')
            target = ctx.guild.get_member(int(target.translate({ord(i): None for i in '@<>'})))
        else:
            target = ctx.author

        roleId = 464175395651190805
        if target.get_role(roleId):
            await target.remove_roles(ctx.guild.get_role(roleId))
            return await ctx.send(f"{target.mention} is now off LOA, welcome back!")
        
        role = ctx.guild.get_role(roleId)
        await target.add_roles(role)
        return await ctx.send(f"{target.mention} is now on LOA, see you when you get back!")

def setup(client):
    client.add_cog(miscCommands(client))
