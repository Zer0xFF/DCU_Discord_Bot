import discord
from discord.ext import commands

# === utils/scheduling.py
import sched, _thread
from time import time as now

async def schedule_abs(time, func, *args, **kwargs):
    delay = time - now()
    await schedule(delay, func, *args, **kwargs)

async def schedule(delay, func, *args, **kwargs):
    #TODO: use existing scheduler and existing thread, instead of spawning each time
    s = sched.scheduler()
    s.enter(delay, 3, func, args, kwargs)
    _thread.start_new_thread(
            lambda  *_: s.run(), #~~~~~~~ted~bundy~did~9~11~~~~
            (0,0)
    )
# === endutil

# === utils/sequel_name.py
# TODO: use Fast naming convention instead of boring Windows convention
async def sequel_name(name, number):
    """increments a string to prevent naming conflicts"""
    if number <= 1:
        return name
    return f"{name}({number})"

async def resolve_sequel_name(basename, condition):
    """iterate through sequel names until the condition is met"""
    out = basename
    i = 1
    while not condition(out):
        out = sequel_name(out, i)
        i += 1
    return out
# == endutil

class Live(commands.Cog):
    """Used for the creation of temporary live chats"""

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.loop.create_task(self.session.detach())

    async def create_live(self, ctx, name="live-chat", start=None, topic=None, duration=10):
        if start != None:
            await schedule_abs(start, create_live, name, start, topic, duration)
            return
            #TODO: find some way to return a reference to the to-be created channel
        
        name = await resolve_sequel_name(
                name,
                lambda name : len(discord.utils.get(ctx.guild.text_channels, name=name)) == 0
            )
        channel = await ctx.guild.create_text_channel(name, topic) 
        await schedule(duration, channel.delete, "Expired") #TODO: more verbose reason

        return channel

    @commands.command()
    async def live(self, ctx, *, message : str):
        """Create a new live chat which expires after some time"""
        await self.create_live(ctx)
        pass

def setup(bot):
    bot.add_cog(Live(bot))

from time import sleep
async def main():
    await schedule(0, sequel_name, "hello-world", 4)
    sleep(5)


import asyncio
if __name__ == "__main__":
    asyncio.run(main())

