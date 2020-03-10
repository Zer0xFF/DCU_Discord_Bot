import aiohttp
from aiohttp import web
import discord
from discord.ext import commands
import urllib
from bs4 import BeautifulSoup

class Covid(commands.Cog):
    """Live infected numbers for COVID-19"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())

    async def get(self, url):
        async with self.session.get(url) as response:
            return await response.text()

    @commands.command(aliases=["covid-19", "coronavirus", "covid", "corona"])
    async def get_covid(self, ctx):
        """COVID-19 RealTime Info"""
        res = await self.get(
                "https://www.worldometers.info/coronavirus/")
        soup = BeautifulSoup(res,'html.parser')
        rows = soup.find("div", {"class":"maincounter-number"}).find("span").text
        embed = discord.Embed(
                colour=ctx.author.colour,
                title=f"Number of infected cases: ",
                description=rows
            )
        await ctx.send(embed=embed)
        await ctx.send("https://www.youtube.com/watch?v=cphNpqKpKc4")

def setup(bot):
    bot.add_cog(Covid(bot))
