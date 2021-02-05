import discord
from discord.ext import commands
from asyncio import sleep
from time import time as now

# === utils/discord_names.py
#not used but will be
async def to_text_channel_name(s):
    """returns the given string as a valid discord text-channel name"""
    out = ""
    s = s.lower()
    for c in s:
        if isalnum(c):
            out += c
        elif c == ' ':
            out += '-'
    return out
# === endutil

# === utils/sequel_name.py
# TODO: use Fast naming convention instead of boring Windows convention
async def sequel_name(name, number):
    """increments a string to prevent naming conflicts"""
    if number <= 1:
        return name
    return f"{name}-{number}"

async def resolve_sequel_name(basename, condition):
    """iterate through sequel names until the condition is met"""
    out = basename
    i = 1
    while not condition(out):
        out = await sequel_name(basename, i)
        i += 1
    return out

async def resolve_channel_sequel_name(basename):
    """iterate through sequel names until a unique channel name is found"""
    return await resolve_sequel_name (
            basename,
            lambda name : (discord.utils.get(ctx.guild.text_channels, name=basename)) is None
        )

# == endutil

class Live(commands.Cog):
    """Used for the creation of temporary live chats"""

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())

    async def create_live(self, ctx, name="live-chat", start=None, topic=None, duration=10):
        if start != None:
            ctx.send(f"scheduled creation of {name} for {start}") #TODO: pretty print time
            await sleep(start - now())
        
        name = await resolve_channel_sequel_name(name)
        channel = await ctx.guild.create_text_channel(name) 

        await sleep(duration)
        await channel.delete(reason="Expired") #TODO: more verbose reason

    @commands.command()
    async def live(self, ctx, *, message : str =""):
        """Create a new live chat which expires after some time"""
        duration = 10
        try:
            if message:
                duration=int(message)
        except ValueError:
            await ctx.send("Usage: `!live <DURATION (SECONDS)>`\nBetter parsing on the way")
        try:
            await self.create_live(ctx, duration=duration)
        except discord.Forbidden:
            await ctx.send("Bot lacks permissions")
        pass

def setup(bot):
    bot.add_cog(Live(bot))

