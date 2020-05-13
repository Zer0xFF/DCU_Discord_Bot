import discord
from discord.ext import commands

# === Dummy functions ===
def SCHEDULE(*args, **kwargs):
    pass
def NOW():
    return 0
# === end dummy functions ===

# === utils/sequel_name.py
# TODO: use Fast naming convention instead of boring Windows convention
def sequel_name(name, number):
    """increments a string to prevent naming conflicts"""
    if number <= 1:
        return name
    return f"{name}({number})"

def resolve_sequel_name(basename, condition):
    """iterate through sequel names until the condition is met"""
    out = basename
    i = 1
    while condition(out):
        out = sequel_name(out, i)
        i += 1
    return out
# == end

class Live(commands.Cog):
    """Used for the creation of temporary live chats"""

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())

    def create_live(self, ctx, name="live-chat", start=None, topic=None, duration=3600, **kwargs):
        if start != None:
            SCHEDULE(start, create_live, name, start, topic, duration, **kwargs)
        
        name = resolve_sequel_name(
                name,
                lambda name : len(discord.utils.get(ctx.guild.text_channels, name=name)) == 0
            )
        channel = ctx.guild.create_text_channel(name, topic) 
        SCHEDULE(NOW() + duration, channel.delete, "Expired") #TODO: more verbose reason

    @commands.command()
    async def live(self, ctx, *, message : str):
        """Create a new live chat"""
        pass

def setup(bot):
    bot.add_cog(Live(bot))
