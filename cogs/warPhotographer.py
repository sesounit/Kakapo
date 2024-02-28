import nextcord, random, os, time
from nextcord.ext import commands, tasks
#Types of images we'll accept.
image_types = ["png", "jpeg", "jpg"]
# Server filepath: ~/11ty-sesosite/assets/img/raw_media/
filepath = 'attachments/'
global attachments
attachments = []
#Warphotographer Screenshot Uploader Cog
class warPhotographer(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def cog_check(self, ctx):
        #Check if user has war photographer role
        role = nextcord.utils.get(ctx.guild.roles, name='War Photographer')
        if role in ctx.author.roles:
            return True
        else:
            return False
    
    @commands.command(aliases=['uploadscreenshot', 'usc', 'u'])
    async def upload(self, ctx):
        filesUploaded = 0
        for attachment in ctx.message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types) and filesUploaded < 11:
                # Time is inserted for record keeping and to account for attachments of the same name.
                full_filepath = os.path.join(f'{filepath}{ctx.author.display_name}_({time.time()})_{attachment.filename.lower()}')
                full_filepath = os.path.expanduser(full_filepath)
                await attachment.save(full_filepath)
                filesUploaded = filesUploaded + 1
        if filesUploaded != 0:
            await ctx.send(f"{filesUploaded} file(s) successfully uploaded!")
            return
        await ctx.send("Something undefined went wrong processing your request.")


def setup(client):
    client.add_cog(warPhotographer(client))
