import discord
from discord.ext import commands
import re

class News(commands.Cog):
    """News command, for DCU Bot."""

    def __init__(self, bot):
        self.bot = bot
    
    async def validate(self, raw_message):
        URL = raw_message
        try:
            regex = re.compile(
            r'^(?:http)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE|re.UNICODE)
            return (re.match(regex, URL))
        except:
            return False

    @commands.command()
    async def news(self, ctx, url_link:str):
        """Send news links to the news channel
        Message the bot with the !news prefix along with your 
        news link to have it appear in the news channel."""
        user = ctx.message.author
        channel = self.bot.get_channel(<INSERT-CHANNEL-ID>)
        if await self.validate(url_link):
            output = "{:s} : {:s}".format(user.display_name,url_link)
            await channel.send(output)
        else:
            output = "The Given URL is invalid."
            await ctx.send(output)
def setup(bot):
    bot.add_cog(News(bot))