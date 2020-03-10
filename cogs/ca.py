import json
import os
import re
import arrow
import discord
import requests
from discord.ext import commands
import time
import sys
from datetime import datetime

upcoming = []

#CA stands for Continuous Assessment :¬)'''
class CA(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.load_upcoming_file()

    def load_upcoming_file(self):
    #Load file which contains all upcoming CA
        if os.path.isfile("upcoming.txt"):
            with open("upcoming.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    upcoming.append(line)

    def update_upcoming_file(self):
    #Update file which contains all upcoming CA'''
        with open("upcoming.txt", "w") as f:
            for event in upcoming:
                f.write(event)
                f.write("\n")

    def desc_formatter(self):
        formatted = []
        for line in upcoming:
            line = line.strip().split()
            formatted.append(f"{line[0]} {line[1]} - {' '.join(line[2:])}\n")
        return formatted

    def sorter(self):
        upcoming.sort(key=lambda date: datetime.strptime(date[0:14], "%d/%m/%y %H:%M"))

    @commands.command(aliases=["CA"])
    async def ca(self,ctx):
        formatted = self.desc_formatter()
        embed = discord.Embed(title="{}".format("**Upcoming Continuous Assessment**", color=0x27FF22), description="\n".join(formatted))
        await ctx.send(embed=embed)

    @commands.command(aliases=["addCA"])
    async def addca(self,ctx, *, args):
        spec = args.strip()
        upcoming.append(spec.strip())
        self.sorter()
        self.update_upcoming_file()

def setup(bot):
    bot.add_cog(CA(bot))