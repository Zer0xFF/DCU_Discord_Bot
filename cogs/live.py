import discord
from discord.ext import commands
from time import time as now
from asyncio import sleep

# === utils/discord_names.py
async def to_text_channel_name(s):
    # no I won't "just use regex" shut up
    out = ""
    s = s.lower()
    for c in s:
        if 'a' <= c <= 'z' or '0' <= c <= '9':
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
    return f"{name}{number}"

async def resolve_sequel_name(basename, condition):
    """iterate through sequel names until the condition is met"""
    out = basename
    i = 1
    while not condition(out):
        out = await sequel_name(basename, i)
        i += 1
    return out
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
        
        name = await resolve_sequel_name(
                name,
                lambda name : (discord.utils.get(ctx.guild.text_channels, name=name)) is None
            )
        channel = await ctx.guild.create_text_channel(name) 

        await sleep(duration)
        await channel.delete(reason="Expired") #TODO: more verbose reason

        return channel

    @commands.command()
    async def live(self, ctx, *, message : str =""):
        """Create a new live chat which expires after some time"""
        try:
            await self.create_live(ctx)
        except discord.Forbidden:
            await ctx.send("Bot lacks permissions")
        pass

def setup(bot):
    bot.add_cog(Live(bot))

