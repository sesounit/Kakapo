import nextcord, requests, time
from nextcord.ext import commands

#formFeedback Cog
class FormFeedBack(commands.Cog):
    
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        self.autoSlot = self.client.get_cog("autoSlot")

    #@nextcord.slash_command(name="form")
    #async def form(self, interaction, operationid=None):
        #await interaction.response.send_modal(FeedbackModal(operationId))

    async def serveForm(self, interaction, operationId):
        if operationId == None:
            await interaction.response.send_message("Operation not found, submissions have most likely closed.")
            return
        await interaction.response.send_modal(FeedbackModal(operationId, self.autoSlot))

class FeedbackModal(nextcord.ui.Modal):
    def __init__(self, operationId=None, autoSlot=None):
        super().__init__(
            "Operation Feedback",
        )

        self.operationId = operationId
        
        self.autoSlot = autoSlot

        self.webHook = "https://script.google.com/macros/s/AKfycbzTvQGupZo6HolKi9wiGRz5uk-gR4_A2fW1lPc9BH5RJRP6w6VN4TPeGYOVuyomLNlmYw/exec?gid=212667745"

        # Currently select options are not supported in modals.
        #self.emEnjRating = nextcord.ui.StringSelect(placeholder = "Your overall enjoyment rating", min_values=1, max_values=1)
        #for i in range(1, 11):
        #    self.emEnjRating.add_option(label=i, value=i)
        self.emEnjRating =  nextcord.ui.TextInput(label = "Your overall enjoyment Rating", min_length=1, max_length=3, required=True, placeholder="Enter your rating from 1-10 here!")
        self.emEnjFeedback = nextcord.ui.TextInput(label = "Your overall enjoyment feedback", style=nextcord.TextInputStyle.paragraph, min_length=1, max_length=1024, required=False, placeholder="How did you generally enjoy the operation?")
        self.emDesignRating =  nextcord.ui.TextInput(label = "Your operation design Rating", min_length=1, max_length=3, required=False, placeholder="Enter your rating from 1-10 here!")
        self.emDesignFeedback = nextcord.ui.TextInput(label = "Your operation design feedback", style=nextcord.TextInputStyle.paragraph, min_length=1, max_length=1024, required=False, placeholder="What do you think of the operation's design?")
        self.emLeadershipFeedback = nextcord.ui.TextInput(label = "Your leadership feedback", style=nextcord.TextInputStyle.paragraph, min_length=1, max_length=1024, required=False, placeholder="What do you think of the leadership?")
       
        self.add_item(self.emEnjRating)
        self.add_item(self.emEnjFeedback)
        self.add_item(self.emDesignRating)
        self.add_item(self.emDesignFeedback)
        self.add_item(self.emLeadershipFeedback)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()

        em = nextcord.Embed(title=str(interaction.channel.name.removesuffix(" Feedback")), description=f"Feedback submitted for {interaction.channel.name.removesuffix(' Feedback')}!")
        em.set_author(name=str(interaction.user).removesuffix('#0'), icon_url=interaction.user.avatar)

        host = interaction.guild.get_member(self.autoSlot.database['operations'][self.operationId]['author']).name

        payload = {"operation date" : self.autoSlot.database['operations'][self.operationId]['operation_timestamp'], "submission date" : time.time(), 
                "operation name" : interaction.channel.name.removesuffix(" Feedback"),
                "host" : host, "author" : interaction.user.name,
                "enjoyment rating" : self.emEnjRating.value, "enjoyment feedback" : self.emEnjFeedback.value, "design rating" : self.emDesignRating.value, 
                "design feedback" : self.emDesignFeedback.value, "leadership feedback" : self.emLeadershipFeedback.value}

        response = requests.request("POST", self.webHook, data=payload)

        return await interaction.followup.send(embed=em)

        '''
        em = nextcord.Embed(title=f"{str(interaction.user).removesuffix('#0')}\'s feedback", description="Operation Name")
        em.add_field(name=f"Overall Enjoyment: {self.emEnjRating.value}/10", value=self.emEnjFeedback.value)
        if self.emDesignRating.value != "" or self.emDesignFeedback.value != "":
            em.add_field(name=f"Operation Design: {self.emDesignRating.value}/10", value=self.emDesignFeedback.value, inline=False)
        if self.emLeadershipFeedback.value != "":
            em.add_field(name="Leadership:", value=self.emLeadershipFeedback.value, inline=False)
        return await interaction.response.send_message(embed=em)
        '''

    
    
def setup(client):
    client.add_cog(FormFeedBack(client))