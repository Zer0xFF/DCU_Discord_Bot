import discord
from discord.ext import commands

class Whisper(commands.Cog):
    """Whispers, for DCU Bot.
    PM the bot with the !whisper prefix,
    along with your message."""

    def __init__(self, bot):
        self.bot = bot

    @commands.dm_only()
    @commands.command(aliases=["whisper"])
    async def psst(self, ctx, *,message: str):
        """Psst - PM the bot with the !whisper prefix,
        along with your message."""
        channel = self.bot.get_channel(689655916223660095)
        await channel.send(message)


def setup(bot):
    bot.add_cog(Whisper(bot))
