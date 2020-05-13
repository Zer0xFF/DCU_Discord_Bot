import discord
from discord.ext import commands

class Live(commands.Cog):
    """Used for the creation of temporary live chats"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())

    @commands.command()
    async def live(self, ctx):
        """Create a new live chat"""
        pass

def setup(bot):
    bot.add_cog(MISC(bot))
