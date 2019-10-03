import aiohttp
import discord
from discord.ext import commands


class Bus(commands.Cog):
    """Dublin Bus Times"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())

    async def get(self, url):
        async with self.session.get(url) as response:
            return await response.json()

    @commands.command(aliases=["bus", "stop"])
    async def realtime(self, ctx, stopnumber):
        """Bus RealTime Info"""
        data = await self.get(
            f"https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid={stopnumber}&format=json"
        )
        times = []
        if not data["errormessage"]:
            for bus in data["results"]:
                times.append(f"Route: **{bus['route']}** - Due in: {bus['duetime']} minute(s).")
            embed = discord.Embed(
                colour=ctx.author.colour,
                title=f"Information for stop no {stopnumber}",
                description="\n".join(times),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(data["errormessage"])


def setup(bot):
    bot.add_cog(Bus(bot))
