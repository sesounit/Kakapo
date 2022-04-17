import nextcord, random
from nextcord.ext import commands, tasks
#Types of images we'll accept.
image_types = ["png", "jpeg", "jpg"]
global attachments
attachments = []
#Screenshot Poster Cog
class screenshotPoster(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #Builds Message List on Ready
    @commands.Cog.listener()
    async def on_ready(self):
        global attachments
        channel = self.client.get_channel(911066596229910596)
        messages = await channel.history().flatten()
        # messages is now a list of Messages...
        for msg in messages:
            for attachment in msg.attachments:
                if any(attachment.filename.lower().endswith(image) for image in image_types):
                    attachments.append(msg)

    @commands.Cog.listener()
    async def on_message(self, message):
        global unknowniterator
        if message.channel == self.client.get_channel(911066596229910596):
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(image) for image in image_types):
                    attachments.append(message)

    @commands.command()
    async def image(self, ctx):
        global attachments
        #Find the length of the attachments list, pick a random one, then download its image. Shouldn't be any more than 8mb.
        max = len(attachments)
        rand = random.randrange(0, (max))
        msg = attachments[rand]
        for attachment in msg.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                await attachment.save(f'attachments/{attachment.filename.lower()}')
        await ctx.send(files=[nextcord.File(f'attachments/{attachment.filename.lower()}')])


def setup(client):
    client.add_cog(screenshotPoster(client))