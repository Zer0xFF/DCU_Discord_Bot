import aiohttp
import discord
from discord.ext import commands

class MISC(commands.Cog):
    """Random MISC"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())

    async def get(self, url):
        async with self.session.get(url) as response:
            return await response.text()

    @commands.command()
    async def commit(self, ctx):
        """Get Random Commit suggestions"""
        res = await self.get("http://whatthecommit.com/index.txt")
        await ctx.send("```\n{}\n```".format(res))

def setup(bot):
    bot.add_cog(MISC(bot))
