import nextcord, random
from nextcord.ext import commands, tasks
#Types of images we'll accept.
image_types = ["png", "jpeg", "jpg"]
filepath = 'uploaded/'
global attachments
attachments = []
#Warphotographer Screenshot Uploader Cog
class warPhotographer(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['uploadscreenshot', 'usc', 'u'])
    @commands.has_permissions(administrator=True)
    async def upload(self, ctx):
        messages = await ctx.channel.history(limit=2).flatten()
        for msg in messages:
            if msg.author == ctx.author:
                for attachment in msg.attachments:
                    if any(attachment.filename.lower().endswith(image) for image in image_types):
                        if 'unknown' in attachment.filename:
                            await attachment.save(f'{filepath}{ctx.author.display_name}({random.randrange(1, (9999))}){attachment.filename.lower()}')
                            await ctx.send("File successfully uploaded!")
                            return
                        await attachment.save(f'{filepath}{ctx.author.display_name}{attachment.filename.lower()}')
                        await ctx.send("File successfully uploaded!")
                        return
            else:
                await ctx.send("Last message is not your own.")
                return
        await ctx.send("Something undefined went wrong processing your request.")


def setup(client):
    client.add_cog(warPhotographer(client))
