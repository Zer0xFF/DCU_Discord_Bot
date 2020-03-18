import aiohttp
import discord
from discord.ext import commands

class Whisper(commands.Cog):
    """Whispers, for DCU Bot."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
        # self.client = commands.Bot(command_prefix="whisper")

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())

    @commands.Cog.listener()
    async def on_message(self, message):
        # channel id for public server
        channel = self.bot.get_channel(689165985164558435)
        if message.guild is None:
            if message.author != self.bot.user:
                if message.content.startswith("!whisper "):
                    await channel.send(message.content[8:])

def setup(bot):
    bot.add_cog(Whisper(bot))
