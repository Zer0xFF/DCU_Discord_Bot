import discord
from discord.ext import commands
import subprocess

class Update(commands.Cog):
    """Updates"""

    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role("Mahmood")
    @commands.command()
    async def update(self, ctx):
        """Pull updates from github"""
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
    bot.add_cog(Update(bot))
