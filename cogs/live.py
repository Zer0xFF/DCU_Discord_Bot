import discord
from discord.ext import commands

# === Dummy functions ===
def SCHEDULE(*args, **kwargs):
    pass
def CHANNEL_EXISTS(name):
    return false
def NOW():
    return 0
# === end dummy functions ===


class Live(commands.Cog):
    """Used for the creation of temporary live chats"""

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())


    # TODO: move to utils
    # TODO: expand and add docstring
    def sequel_name(self, name, number):
        if number <= 1:
            return name
        return f"{name}({number})"
        
    # TODO: much of this logic can be moved to wherever sequel_name is served
    def get_unique_channel_name(self, basename):
        """return the first sequel-name of the given basename which is not currently a channel name"""
        out = basename
        i = 1
        while CHANNEL_EXISTS(out):
            out = sequel_name(out, i)
            i += 1
        return out

    def create_live(self, ctx, name="live-chat", start=None, topic=None, duration=3600, **kwargs):
        if start != None:
            SCHEDULE(start, create_live, name, start, topic, duration, **kwargs)
        
        name = get_unique_channel_name(name)
        channel = ctx.guild.create_text_channel(name, topic) 
        SCHEDULE(NOW() + duration, channel.delete, {'reason':"Expired"}) #TODO: more verbose reason


    @commands.command()
    async def live(self, ctx, *, arg):
        """Create a new live chat"""
        pass

def setup(bot):
    bot.add_cog(Live(bot))
