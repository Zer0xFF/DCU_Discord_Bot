import aiohttp
import discord
from discord.ext import commands

class Whisper(commands.Cog):
    """Whispers, for DCU Bot."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())

    @commands.dm_only()
    @commands.command(aliases=["whisper"])
    async def get_whisper(self, ctx, *,message: str):
        """Psst Psst"""
        channel = self.bot.get_channel(689165985164558435)
        if ctx.guild is None:
            if ctx.author != self.bot.user:
                await channel.send(message)


def setup(bot):
    bot.add_cog(Whisper(bot))
