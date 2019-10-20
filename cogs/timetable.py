import json
import os
import re

import arrow
import discord
import requests
from discord.ext import commands
from ics import Calendar, Event

cancelled_events = set()
c = Calendar()


class Timetable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loadCal()
        self.LoadCancelFile()

    def loadCal(self):
        with open("CAL_REQ.json", "r") as f:
            global c
            c2 = Calendar()
            data = json.load(f)
            headers = {"Authorization": "basic T64Mdy7m["}
            r = requests.post(
                "https://opentimetable.dcu.ie/broker/api/categoryTypes/241e4d36-60e0-49f8-b27e-99416745d98d/categories/events/filter",
                json=data,
                headers=headers,
            )
            if r.status_code == 200:
                response = json.loads(r.text)
                for event in response[0]["CategoryEvents"]:
                    e = Event()
                    e.begin = event["StartDateTime"]
                    e.end = event["EndDateTime"]
                    e.location = event["Location"]
                    e.description = ""
                    for item in event["ExtraProperties"]:
                        if item["DisplayName"] == "Module Name":
                            e.name = "{} - {}".format(item["Value"], event["EventType"])
                        e.description += "{}: {}\n".format(item["DisplayName"], item["Value"])

                    c2.events.add(e)
                c = c2
                return True
            else:
                print("Request Failed: %d" % r.status_code)
                return False

    def LoadCancelFile(self):
        if os.path.isfile("cancelled_events.txt"):
            with open("cancelled_events.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    cancelled_events.add(line)

    def UpdateCancelFile(self):
        with open("cancelled_events.txt", "w") as f:
            for event in cancelled_events:
                f.write(event)
                f.write("\n")

    def PreEmbed(self, embed, events, day):
        msg = ""
        if events:
            for event in events:
                status_flag = ""
                if event.begin.to("Europe/Dublin").format("HH:mm DD-MM-YYYY") in cancelled_events:
                    status_flag = "~~"
                msg += "{}{} {} hours {} {}{}\n".format(
                    status_flag,
                    event.begin.to("Europe/Dublin").format("HH:mm"),
                    event.duration.seconds // 3600,
                    event.location,
                    event.name,
                    status_flag,
                )
        if not msg:
            msg = "No schedule found for {}.\n".format(day.format("ddd Do-MMM"))
        embed.add_field(name="{}.\n".format(day.format("ddd Do-MMM")), value=msg, inline=False)

    def GetDayOffset(self, day):
        dow = -(int(arrow.utcnow().to("Europe/Dublin").format("d")) - 1) + day
        if int(arrow.utcnow().to("Europe/Dublin").format("d")) > 5:
            dow += 7
        day_arw = arrow.utcnow().to("Europe/Dublin").shift(days=+dow)
        return day_arw

    def GetDayArwSchedEmbed(self, day_arw):
        embed = discord.Embed(title="Schedule for {}".format(day_arw.format("ddd")), color=0x27FF22)

        events = c.timeline.on(day_arw)
        self.PreEmbed(embed, events, day_arw)

        return embed

    def GetDaySchedEmbed(self, day):
        day_arw = self.GetDayOffset(day)
        return self.GetDayArwSchedEmbed(day_arw)

    def GetWeekSchedEmbed(self, week_offset):
        dow = int(arrow.utcnow().to("Europe/Dublin").format("d")) - 1
        start_week = arrow.utcnow().to("Europe/Dublin").shift(days=-dow).shift(weeks=week_offset)
        end_week = start_week.shift(days=+4)
        embed = discord.Embed(
            title="{} Until {}".format(
                start_week.format("ddd Do-MMM"), end_week.format("ddd Do-MMM-YYYY")
            ),
            color=0x27FF22,
        )
        for day in arrow.Arrow.range("day", start_week, end_week):
            events = c.timeline.on(day)
            self.PreEmbed(embed, events, day)

        return embed

    def CancelEvent(self, timedate):
        day = arrow.get(timedate, "HH:mm DD-MM-YYYY", tzinfo="Europe/Dublin")
        events = c.timeline.at(day)
        embed = discord.Embed(
            title="Cancelling event - {}".format(day.format("ddd Do-MMM")), color=0x27FF22
        )
        if events:
            cancelled_events.add(timedate)
            self.UpdateCancelFile()
            self.PreEmbed(embed, events, day)
        else:
            embed.add_field(
                name="Cancellation Failed.",
                value="No event found on {}.\n".format(day.format("HH:mm ddd Do-MMM")),
                inline=False,
            )
        return embed

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        cmd = message.content.casefold()

        if cmd.startswith("!this week"):
            embed = self.GetWeekSchedEmbed(0)
            await message.channel.send(embed=embed)

        if message.content.startswith("!POWER"):
            await message.channel.send("Can you feel the POWER!?!?!?")

        if message.content.startswith("!power"):
            await message.channel.send("No, try `!POWER`")

    @commands.has_any_role("OVERLORDS", "Mahmood")
    @commands.command()
    async def reload(self, ctx):
        """Reload the calender."""
        if self.loadCal():
            await ctx.send("Calender has been reloaded")
        else:
            await ctx.send("Calender failed to reloaded")

    @commands.is_owner()
    @commands.command()
    async def shutdown(self, ctx):
        """Shutdown the bot"""
        await self.bot.logout()

    @commands.command(aliaes=["monday"])
    async def mon(self, ctx):
        """Classes for the following Monday"""
        embed = self.GetDaySchedEmbed(0)
        await ctx.send(embed=embed)

    @commands.command(aliaes=["tuesday"])
    async def tue(self, ctx):
        """Classes for the following Tuesday"""
        embed = self.GetDaySchedEmbed(1)
        await ctx.send(embed=embed)

    @commands.command(aliaes=["wednesday"])
    async def wednesday(self, ctx):
        """Classes for the following Wednesday."""
        embed = self.GetDaySchedEmbed(2)
        await ctx.send(embed=embed)

    @commands.command(aliaes=["thursday"])
    async def thurs(self, ctx):
        """Classes for the following Thursday."""
        embed = self.GetDaySchedEmbed(3)
        await ctx.send(embed=embed)

    @commands.command(aliaes=["friday"])
    async def fri(self, ctx):
        """Classes for the following Friday."""
        embed = self.GetDaySchedEmbed(4)
        await ctx.send(embed=embed)

    @commands.command()
    async def today(self, ctx):
        """Classes for today."""
        day_arw = arrow.utcnow().to("Europe/Dublin")
        embed = self.GetDayArwSchedEmbed(day_arw)
        await ctx.send(embed=embed)

    @commands.command()
    async def tomorrow(self, ctx):
        """Classes for tomorrow."""
        day_arw = arrow.utcnow().to("Europe/Dublin").shift(days=+1)
        embed = self.GetDayArwSchedEmbed(day_arw)
        await ctx.send(embed=embed)

    @commands.has_any_role("OVERLORDS", "Mahmood")
    @commands.command(usage="<time> <date>")
    async def cancel(self, ctx, *, args):
        """Cancel a lecture."""
        args = args.split()
        if len(args) > 2:
            await ctx.send("Expecting 2 arguments, date and time.\nE.g `!cancel 9:00 25-09-19`")
        cmd = " ".join(args)
        m = re.search(r"(\d+:\d+) (\d+\-\d+\-\d+)", cmd)
        if m:
            embed = self.CancelEvent(cmd)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid time date format, please use HH:mm DD-MM-YYYY")

    @commands.group()
    async def next(self, ctx):
        """Next class or next weeks classes."""
        if ctx.invoked_subcommand is None:
            events = c.timeline.start_after(arrow.utcnow().to("Europe/Dublin"))
            event = next(events)
            embed = discord.Embed(title="Next Class", color=0x27FF22)
            self.PreEmbed(embed, [event], event.begin)
            await ctx.send(embed=embed)

    @next.command()
    async def week(self, ctx):
        """Next weeks classes."""
        embed = self.GetWeekSchedEmbed(1)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Timetable(bot))
