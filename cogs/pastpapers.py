import discord
import aiohttp
from discord.ext import commands


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]


class PastPapers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
        self.url = "https://dcupastpapers.xyz/api/search"

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    async def request(self, module):
        async with self.session.post(self.url, json={"search": module}) as req:
            try:
                return await req.json()
            except aiohttp.ContentTypeError:
                return {"failed": True}

    @commands.command(aliases=["pp"])
    async def pastpapers(self, ctx, module_code: str):
        """Lookup past papers"""
        data = await self.request(module_code)
        if data.get("failed") is True:
            return await ctx.send("No module found. Please try refining your search")
        a = chunks(data["results"], 10)
        embeds = []
        for exambulk in a:
            msg = ""
            for result in exambulk:
                msg += f"[**{result['code']} - {result['year']}**]({result['link']})\n"
            embed = discord.Embed(
                title=f"Papers for {module_code.upper()}", color=ctx.author.color, description=msg
            )
            embeds.append(embed)
        await ctx.send(embed=embeds[0])  # TBD: Create a menu to loop through various years.


def setup(bot):
    bot.add_cog(PastPapers(bot))
