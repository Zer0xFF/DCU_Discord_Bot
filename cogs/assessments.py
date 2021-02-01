import os
import discord
import sys
from discord.ext import commands, tasks
from datetime import datetime


assessments = []


class Assessments(commands.Cog):
    file = "assessments.txt"

    def __init__(self,bot):
        self.bot = bot
        self.load_assessments_file()

    def load_assessments_file(self):
        #Load file which contains all upcoming assessments
        if os.path.isfile(self.file):
            with open(self.file, "r") as f:
                for line in f:
                    line = line.strip()
                    assessments.append(line)
        else:
            open(self.file, 'a').close()

    def update_assessments_file(self):
        #Update file which contains all upcoming assessments
        with open(self.file, "w") as f:
            for assessment in assessments:
                f.write(assessment)
                f.write("\n")

    def desc_formatter(self):
        #Description formatting
        formatted = []
        line_index = 0
        for line in assessments:
            line = line.strip().split()
            formatted.append(f"**{line_index}.** {line[0][:5]} {line[1]} - {' '.join(line[2:])}\n")
            line_index += 1
        return formatted

    def date_validator(self, date):
        #validates a date
        try:
            datetime.strptime(date.strip(), "%d/%m/%y %H:%M")
        except ValueError:
            return False
        return True

    def date_sorter(self):
        #sorts asssessments by dates and times
        assessments.sort(key=lambda date: datetime.strptime(date[:14], "%d/%m/%y %H:%M"))

    def _add_ca(self, string):
        assessments.append(string)
        self.date_sorter()
        self.update_assessments_file()

    def remove_entry(self, entry):
        #removes entry at index entry
        del assessments[entry]
        self.update_assessments_file()

    async def ca_cleanup(self, ctx):
        nearest_ca_datetime = datetime.strptime(assessments[0][:14], "%d/%m/%y %H:%M")
        while len(assessments) > 0 and nearest_ca_datetime < datetime.now():
            await ctx.send(f"Automatically removed past assessment: {assessments[0]}")
            self.remove_entry(0)
            if len(assessments) > 0:
                nearest_ca_datetime = datetime.strptime(assessments[0][:14], "%d/%m/%y %H:%M")

    def cog_unload(self):
        pass

    @commands.command(aliases=["CA", "assessments", "ass"])
    async def ca(self, ctx):
        if len(assessments) > 0:
            await self.ca_cleanup(ctx)
        if len(assessments) > 0:
            formatted = self.desc_formatter()
            embed = discord.Embed(title="**Upcoming Assessment(s)**", color=0x78ff83, description="\n".join(formatted))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="**Upcoming Assessment(s)**", color=0x78ff83, description="🎉 You are free....for now >:) 🎉")
            await ctx.send(embed=embed)
    
    @commands.command(aliases=["!stress_free"])
    async def stress_free(self, ctx):
        await ctx.send("You have no assessments! (One can dream - Now get back to work!)")

    @commands.has_any_role("Overlord", "Mahmood", "Class Rep", "Jeff", "While Loop Master")
    @commands.command(aliases=["addCA","add_ass"])
    async def addca(self, ctx, date, time, module, *, description):
        #Adds entries
        is_valid_date = False
        if (len(date.split("/")) == 3) and (len(time.split(":")) == 2):   #deals with date/time not being first 2 inputs.
            is_valid_date = self.date_validator(date + " " + time)
        if is_valid_date:
            self._add_ca(f"{date} {time} {module} {description.strip()}")
            await ctx.send("Add successful.")
        else:
            await ctx.send("Invalid date or time, use DD/MM/YY and HH:MM (24 hour clock).")

    @commands.has_any_role("Overlord", "Mahmood", "Class Rep", "Jeff")
    @commands.command(aliases=["RemoveCA", "removeCA", "rmca", "rmCA", "remove_ass"])
    async def removeca(self, ctx, entry: int):
        #removes entries - 0 is first entry in ca list.
        if entry <= len(assessments) - 1 and entry >= 0:
            self.remove_entry(entry)
            await ctx.send("Remove successful.")
        else:
            if len(assessments) > 0:
                await ctx.send(f"Invalid entry, use an index of {len(assessments)-1} or below.")
            else:
                await ctx.send("Invalid entry, there are currently no active assignments.")

    @commands.has_any_role("Overlord", "Mahmood", "Class Rep")
    @commands.command()
    async def clear_all_assessments(self, ctx):
        #clears all assessments, has a long and annoying name to prevent accidental use.
        if len(assessments) > 0:
            while len(assessments) > 0:
                self.remove_entry(0)
            await ctx.send("All assessments cleared.")
        else:
            await ctx.send("Assessments already clear.")

    @commands.has_any_role("Overlord", "Mahmood", "Class Rep", "Jeff")
    @commands.command(aliases=["cleanCA", "clean_ass"])
    async def cleanca(self, ctx):
        if len(assessments) > 0:
            await self.ca_cleanup(ctx)
            await ctx.send("🍑 All clean 🍑")
        else:
            await ctx.send("Unable to cleanup, there are currently no active assessments.")

def setup(bot):
    bot.add_cog(Assessments(bot))
