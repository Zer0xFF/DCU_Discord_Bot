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
        else:
            open('upcoming.txt', 'a').close()

    def update_upcoming_file(self):
    #Update file which contains all upcoming CA'''
        with open("upcoming.txt", "w") as f:
            for event in upcoming:
                f.write(event)
                f.write("\n")

    def desc_formatter(self):
    #Description formatting
        formatted = []
        for line in upcoming:
            line = line.strip().split()
            formatted.append(f"{line[0]} {line[1]} - {' '.join(line[2:])}\n")
        return formatted

    def date_sorter(self):
    #sorts upcoming by dates and times
        upcoming.sort(key=lambda date: datetime.strptime(date[0:14], "%d/%m/%y %H:%M"))

    def remove_entry(self, entry):
        del upcoming[entry]
        self.update_upcoming_file()

    @commands.command(aliases=["CA"])
    async def ca(self,ctx):
        formatted = self.desc_formatter()
        embed = discord.Embed(title="{}".format("**Upcoming Continuous Assessment**"),color=0x9B30FF, description="\n".join(formatted))
        await ctx.send(embed=embed)

    @commands.has_any_role("OVERLORDS", "Mahmood", "Class Rep")
    @commands.command(aliases=["addCA"])
    async def addca(self,ctx,date,time,module,*,description):
        try:
            r_date = re.compile('[0-3][0-9]/[0-1][0-9]/\d{2}')
            r_time = re.compile('[0-2][0-9]:[0-5][0-9]')
            if r_date.match(date) is not None and r_time.match(time) is not None:
                upcoming.append(f"{date} {time} {module} {description.strip()}")
                self.date_sorter()
                self.update_upcoming_file()
            else:
                await ctx.send("Invalid date or time, use DD/MM/YY and HH:MM (24 hour clock)")
        except:
            await ctx.send("Invalid entry, use: DD/MM/YY HH/MM modulecode description")

    @commands.has_any_role("OVERLORDS", "Mahmood", "Class Rep")
    @commands.command(aliases=["RemoveCA", "removeCA"])
    async def removeca(self,ctx, entry):
    #removes entries - 0 is first entry in ca list.
        try:
            self.remove_entry(int(entry))
        except:
            await ctx.send(f"Entry index out of range, please send index of {len(upcoming)} or below.") 

def setup(bot):
    bot.add_cog(CA(bot))