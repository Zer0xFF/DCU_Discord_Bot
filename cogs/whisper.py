import os
import discord
import hashlib
from discord.ext import commands

class Whisper(commands.Cog):
    """Whispers, for DCU Bot.
    PM the bot with the !whisper prefix,
    along with your message."""

    def __init__(self, bot):
        self.bot = bot
        self.random_animals = ['Ferret', 'Donkey', 'Robin', 'Platypus', 'Moose', 'Panda', 'Aardvark', 'Dog', 'Ant', 'Cheetah', 'Chicken', 'Duck', 'Eagle', 'Gecko', 'Lion', 'Pig', 'Wolf']
        self.random_adjectives = ['Alert', 'Alive', 'Amused', 'Clever', 'Crazy', 'Dizzy', 'Jolly', 'Brave', 'Tired', 'Busy', 'Bored']

    @commands.dm_only()
    @commands.command(aliases=["whisper"])
    async def psst(self, ctx, *,message: str):
        """Psst - PM the bot with the !whisper prefix,
        along with your message."""


        seed = os.environ.get('WHISPERHASH')
        channel = self.bot.get_channel(689655916223660095)
        namehash = abs(hash(ctx.message.author.mention)*hash(seed)) % (10 ** 8)
        await channel.send(self.random_adjectives[namehash % len(self.random_adjectives)] + " " + self.random_animals[namehash -24 % len(self.random_animals)] + ":  " + message)


def setup(bot):
    bot.add_cog(Whisper(bot))
