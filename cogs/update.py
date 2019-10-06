import aiohttp
import discord
from discord.ext import commands
import subprocess

class Bus(commands.Cog):
    """Updates"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())

    async def get(self, url):
        async with self.session.get(url) as response:
            return await response.json()

    @commands.has_any_role("Mahmood")
    @commands.command()
    async def update(self, ctx):
        """Pull updates fro github"""
        ret = -1
        with subprocess.Popen(["git", "pull", "origin", "master"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as child:
            stdout = "\n".join(child.communicate()[0].decode("utf-8").split("\\n"))
            ret = child.returncode
        if ret == 0:
            embed = discord.Embed(
                colour=ctx.author.colour,
                title=f"Update Successful, Please Restart Bot.",
                description=stdout,
            )
            await ctx.send(embed=embed)
        else:
            print(stdout)
            await ctx.send("Error: {}".format(ret))


def setup(bot):
    bot.add_cog(Bus(bot))
