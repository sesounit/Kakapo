import nextcord, random, os
from nextcord.ext import commands, tasks
#Types of images we'll accept.
image_types = ["png", "jpeg", "jpg"]
filepath = '~/11ty-sesosite/assets/img/raw_media/'
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
        messages = await ctx.channel.history(limit=2).flatten()
        for msg in messages:
            if msg.author == ctx.author:
                for attachment in msg.attachments:
                    if any(attachment.filename.lower().endswith(image) for image in image_types):
                        full_filepath = os.path.join(f'{filepath}{ctx.author.display_name}_{attachment.filename.lower()}')
                        # If filename is unknown, generate a random one
                        if 'unknown' in attachment.filename:
                            full_filepath = os.path.join(f'{filepath}{ctx.author.display_name}_({random.randrange(1, (9999))})_{attachment.filename.lower()}')
                        full_filepath = os.path.expanduser(full_filepath)
                        await attachment.save(full_filepath)
                        await ctx.send("File successfully uploaded!")
                        return
            else:
                await ctx.send("Last message is not your own.")
                return
        await ctx.send("Something undefined went wrong processing your request.")


def setup(client):
    client.add_cog(warPhotographer(client))
