import nextcord, random
from nextcord.ext import commands
gamestage = 0
#welcomeMessage Cog
class AmongUS(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=["Amongus", "Imposter", "ImposterAmongus", "SUSO"])
    async def game(self, ctx, Choice=''):
        global imposterkilled
        global gamestage
        global crewmembers
        global imposter
        if Choice == "Restart" or Choice == "restart" or Choice == "new" or Choice == "New":
            gamestage = 0
            await ctx.send("Game reset.")
        if gamestage == 0:
            imposterkilled = False
            crewmembers = ["D. Sagbag", "Box", "Mace", "Pickle423", "The Dallkorgi", "J. Rydungis", "P. Trevor", "Finch", "Ojax"]
            crewmembernumber = 0
            imposternumber = random.randrange(1, 10)
            imposter = "Null"
            for crew in crewmembers:
                crewmembernumber = crewmembernumber + 1
                if crewmembernumber == imposternumber:
                    imposter = crew
            gameEmbed = nextcord.Embed(title="SESO Text-Entertainment: An Imposter Among Us", description="Who will survive?", color=0x0E8643)
            gameEmbed.add_field(name="Crewmembers", value=crewmembers)
            gameEmbed.add_field(name="Imposters:", value="1", inline=False)
            gameEmbed.add_field(name="Options Available", value="1: Call Emergency Meeting, 2: Forcibly Murder Someone", inline=False)
            gameEmbed.set_footer(text="An Imposter Among Us Presented By: SESO Text-Entertainment Solutions.")
            await ctx.send(embed=gameEmbed)
            gamestage = 1
        elif gamestage == 1:
            if Choice == '':
                await ctx.send("Please make a decision.")
            elif Choice == '1':
                crewmembernumber = 0
                killed = random.randrange(1, 10)
                for crew in crewmembers:
                    if crewmembernumber == killed:
                        if crewmembers[crewmembernumber] != imposter:
                            crewmembers.remove(crew)
                    crewmembernumber = crewmembernumber + 1
                gameEmbed = nextcord.Embed(title="SESO Text-Entertainment: An Imposter Among Us", description="An Emergency Meeting Has Been Called!", color=0x0E8643)
                gameEmbed.add_field(name="Crewmembers", value=crewmembers)
                gameEmbed.add_field(name="Imposters:", value="1", inline=False)
                gameEmbed.add_field(name="Options Available", value="Input the number in the list of the person you'd like to vote for.", inline=False)
                gameEmbed.set_footer(text="An Imposter Among Us Presented By: SESO Text-Entertainment Solutions.")
                await ctx.send(embed=gameEmbed)
                gamestage = 3
            elif Choice == '2':
                crewmembernumber = 0
                killed = random.randrange(1, 10)
                for crew in crewmembers:
                    crewmembernumber = crewmembernumber + 1
                    if crewmembernumber == killed:
                        crewmembers.remove(crew)
                gameEmbed = nextcord.Embed(title="SESO Text-Entertainment: An Imposter Among Us", description="Murder?", color=0x0E8643)
                gameEmbed.add_field(name="Crewmembers", value=crewmembers)
                gameEmbed.add_field(name="Imposters:", value="1", inline=False)
                gameEmbed.add_field(name="Options Available", value="Input the target's number in the list.", inline=False)
                gameEmbed.set_footer(text="An Imposter Among Us Presented By: SESO Text-Entertainment Solutions.")
                await ctx.send(embed=gameEmbed)
                gamestage = 2
        elif gamestage == 2:
            if Choice != '':
                Choice = int(Choice)
                Choice = Choice - 1
                if crewmembers[Choice] == imposter:
                    imposterkilled = True
                crewmembers.remove(crewmembers[Choice])
            else:
                await ctx.send("Make a decision.")
                return
            if imposterkilled != True:
                crewcount = 0
                for crew in crewmembers:
                    crewcount = crewcount + 1
                if crewcount == 1:
                    gameEmbed = nextcord.Embed(title="SESO Text-Entertainment: An Imposter Among Us", description="Player Loss", color=0x0E8643)
                    gameEmbed.add_field(name="Crewmembers", value=f"Just you... And him... {crewmembers}")
                    gameEmbed.add_field(name="Imposters:", value="1", inline=False)
                    gameEmbed.add_field(name="Outcome", value="You've lost.", inline=False)
                    gameEmbed.set_footer(text="An Imposter Among Us Presented By: SESO Text-Entertainment Solutions.")
                    await ctx.send(embed=gameEmbed)
                    gamestage = 0
                else:
                    gameEmbed = nextcord.Embed(title="SESO Text-Entertainment: An Imposter Among Us", description="Who will survive?", color=0x0E8643)
                    gameEmbed.add_field(name="Crewmembers", value=crewmembers)
                    gameEmbed.add_field(name="Imposters:", value="1", inline=False)
                    gameEmbed.add_field(name="Options Available", value="1: Call Emergency Meeting, 2: Forcibly Murder Someone", inline=False)
                    gameEmbed.set_footer(text="An Imposter Among Us Presented By: SESO Text-Entertainment Solutions.")
                    await ctx.send(embed=gameEmbed)
                    gamestage = 1
            else:
                gameEmbed = nextcord.Embed(title="SESO Text-Entertainment: An Imposter Among Us", description="Crew Victory!", color=0x0E8643)
                gameEmbed.add_field(name="Crewmembers", value=crewmembers)
                gameEmbed.add_field(name="Imposter:", value=imposter, inline=False)
                gameEmbed.add_field(name="Outcome", value="The Imposter was bravely, and randomly, killed by the player in an act of violence.", inline=False)
                gameEmbed.set_footer(text="An Imposter Among Us Presented By: SESO Text-Entertainment Solutions.")
                await ctx.send(embed=gameEmbed)
                gamestage = 0
        elif gamestage == 3:
            try:
                Choice2 = int(Choice)
                Choice = Choice2 - 1
                crewcount = 0
                highestvoted = ''
                highestvotes = 0
                for crew in crewmembers:
                    crewcount = crewcount + 1
                didplayergetvoted = random.randrange(1, crewcount + 5)
                if didplayergetvoted == crewcount + 5:
                    gameEmbed = nextcord.Embed(title="SESO Text-Entertainment: An Imposter Among Us", description="Player Loss.", color=0x0E8643)
                    gameEmbed.add_field(name="Crewmembers", value=crewmembers)
                    gameEmbed.add_field(name="Imposters:", value='1', inline=False)
                    gameEmbed.add_field(name="Outcome", value="You were ejected from the ship, the imposter lives on, and worse, you're doomed to drift the void until your oxygen runs out.", inline=False)
                    gameEmbed.set_footer(text="An Imposter Among Us Presented By: SESO Text-Entertainment Solutions.")
                    await ctx.send(embed=gameEmbed)
                    gamestage = 0
                else:
                    for crew in crewmembers:
                        votes = random.randrange(1, crewcount)
                        if crew == crewmembers[Choice]:
                            votes + 1
                        if votes > highestvotes:
                            highestvotes = votes
                            crewinteger = 0
                            for crewnew in crewmembers:
                                if crew == crewmembers[crewinteger]:
                                    highestvoted = crewinteger
                ejected = crewmembers[highestvoted]
                crewmembers.remove(ejected)
                if imposter == ejected:
                    gameEmbed = nextcord.Embed(title="SESO Text-Entertainment: An Imposter Among Us", description="Crew Victory!", color=0x0E8643)
                    gameEmbed.add_field(name="Crewmembers", value=crewmembers)
                    gameEmbed.add_field(name="Imposter:", value=ejected, inline=False)
                    gameEmbed.add_field(name="Outcome", value="The Imposter was successfully ejected from the ship! Yay Democracy!", inline=False)
                    gameEmbed.set_footer(text="An Imposter Among Us Presented By: SESO Text-Entertainment Solutions.")
                    await ctx.send(embed=gameEmbed)
                    gamestage = 0
                else:
                    gameEmbed = nextcord.Embed(title="SESO Text-Entertainment: An Imposter Among Us", description="Who will survive?", color=0x0E8643)
                    gameEmbed.add_field(name="Crewmembers", value=crewmembers)
                    gameEmbed.add_field(name="Ejected", value=ejected)
                    gameEmbed.add_field(name="Imposters:", value="1", inline=False)
                    gameEmbed.add_field(name="Options Available", value="1: Call Emergency Meeting, 2: Forcibly Murder Someone", inline=False)
                    gameEmbed.set_footer(text="An Imposter Among Us Presented By: SESO Text-Entertainment Solutions.")
                    await ctx.send(embed=gameEmbed)
                    gamestage = 1
            except:
                await ctx.send("Error Encountered, Make sure you vote for someone actually available.")
            
                
                

def setup(client):
    client.add_cog(AmongUS(client))