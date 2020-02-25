import aiohttp
import discord
from discord.ext import commands
import urllib

class Covid(commands.Cog):
    """Live infected numbers for COVID-19"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())

    async def get(self, url):
        async with requests.get(url) as response:
            return await response

    @commands.dm_only()
    @commands.command(aliases=["covid-19", "coronavirus"])
    async def realtime(self):
        """COVID-19 RealTime Info"""
        res = await self.get(
                "https://www.worldometers.info/coronavirus/")
        soup = BeautifulSoup(res.content,'html.parser')
        rows = soup.find("div", {"class":"maincounter-number"}).find("span").text
        embed = discord.Embed(
                colour=ctx.author.colour,
                title=f"Number of infected cases: ",
                description=rows
            )
        await ctx.send(embed=embed)
        else:
            ctx.send("errormessage")

def setup(bot):
    bot.add_cog(covid(bot))
