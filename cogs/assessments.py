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

assessments = []


class Assessments(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.load_assessments_file()

    def load_assessments_file(self):
        #Load file which contains all upcoming assessments
        if os.path.isfile("assessments.txt"):
            with open("assessments.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    assessments.append(line)
        else:
            open('assessments.txt', 'a').close()

    def update_assessments_file(self):
        #Update file which contains all upcoming assessments
        with open("assessments.txt", "w") as f:
            for assessment in assessments:
                f.write(assessment)
                f.write("\n")

    def desc_formatter(self):
        #Description formatting
        formatted = []
        for line in assessments:
            line = line.strip().split()
            formatted.append(f"{line[0]} {line[1]} - {' '.join(line[2:])}\n")
        return formatted

    def date_validator(self, day, month, year, hour, minute):
        #validates a date
        try:
            datetime(year=int(year),month=int(month),day=int(day),hour=int(hour), minute=int(minute))
        except ValueError:
            return False
        return True

    def date_sorter(self):
        #sorts asssessments by dates and times
        assessments.sort(key=lambda date: datetime.strptime(date[0:14], "%d/%m/%y %H:%M"))

    def remove_entry(self, entry):
        #removes entry at index entry
        del assessments[entry]
        self.update_assessments_file()

    @commands.command(aliases=["CA", "assessments"])
    async def ca(self,ctx):
        if len(assessments) > 0:
            formatted = self.desc_formatter()
            embed = discord.Embed(title="{}".format("**Upcoming Assessment(s)**"),color=0x78ff83, description="\n".join(formatted))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="{}".format("**Upcoming Assessment(s)**"),color=0x78ff83, description="You are free....for now >:)")
            await ctx.send(embed=embed)

    @commands.has_any_role("OVERLORDS", "Mahmood", "Class Rep")
    @commands.command(aliases=["addCA"])
    async def addca(self,ctx,date,time,module,*,description):
        #Adds entries
        isValidDate = False
        split_date = date.split("/")
        split_time = time.split(":")
        if (len(split_date) == 3) and (len(split_time) == 2):   #deals with date/time not being first 2 inputs.
            day, month, year = split_date
            hour, minute = split_time
            isValidDate = self.date_validator(day, month, year, hour, minute)

        if isValidDate:
            assessments.append(f"{date} {time} {module} {description.strip()}")
            self.date_sorter()
            self.update_assessments_file()
            await ctx.send("Add successful.")
        else:
            await ctx.send("Invalid date or time, use DD/MM/YY and HH:MM (24 hour clock).")

    @commands.has_any_role("OVERLORDS", "Mahmood", "Class Rep")
    @commands.command(aliases=["RemoveCA", "removeCA"])
    async def removeca(self,ctx,entry):
        #removes entries - 0 is first entry in ca list.
        if re.search(r"\d", entry) and int(entry) <= len(assessments) - 1 and int(entry) >= 0:
            self.remove_entry(int(entry))
            await ctx.send("Remove successful.")
        else:
            if len(assessments) > 0:
                await ctx.send(f"Invalid entry, use an index of {len(assessments)-1} or below.")
            else:
                await ctx.send("Invalid entry, there are currently no active assignments.")

def setup(bot):
    bot.add_cog(Assessments(bot))
