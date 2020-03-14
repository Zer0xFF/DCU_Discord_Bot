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
    async def get_covid(self, ctx, country=None):
        """COVID-19 RealTime Info"""
        res = await self.get(
                "https://www.worldometers.info/coronavirus/")

        soup = BeautifulSoup(res,'html.parser')
        headers = [h.get_text().strip() for h in soup.find("thead").find_all('th')]
        headers[0] = 'Country'

        if(country):
            info = next(iter([c for c in soup.find("tbody").find_all('tr') if c.td.get_text().strip().casefold() == country.casefold()]), None)
        else:
            info = soup.find_all("tbody")[1]
            info.td.string.replace_with("Global")

        if(info):
            embed = discord.Embed(title="Covid-19 Stats", color=ctx.author.colour)
            data = info.find_all('td')
            for i in range(len(headers)):
                val = data[i].get_text().strip() if data[i].get_text().strip() else "0"
                embed.add_field(name=headers[i], value=val)

            await ctx.send(embed=embed)
            await ctx.send("https://www.youtube.com/watch?v=cphNpqKpKc4")
        else:
            await ctx.send("Country not found.")

def setup(bot):
    bot.add_cog(Covid(bot))
