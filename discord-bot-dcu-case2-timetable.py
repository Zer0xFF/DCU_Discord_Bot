import requests
import json
from ics import Calendar, Event
import discord
import arrow
import re
import os

TOKEN = 'BRING_YOUR_OWN_KEY'
client = discord.Client()

cancelled_events = set()
c = Calendar()

def loadCal():
    with open("CAL_REQ.json", "r") as f:
        global c
        c2 = Calendar()
        data = json.load(f)
        headers = {'Authorization': 'basic T64Mdy7m['}
        r = requests.post('https://opentimetable.dcu.ie/broker/api/categoryTypes/241e4d36-60e0-49f8-b27e-99416745d98d/categories/events/filter', json=data, headers=headers)
        if(r.status_code == 200):
            response = json.loads(r.text)
            for event in response[0]['CategoryEvents']:
                e = Event()
                e.begin = event['StartDateTime']
                e.end = event['EndDateTime']
                e.location = event['Location']
                e.description = ''
                for item in event['ExtraProperties']:
                    if(item['DisplayName'] == 'Module Name'):
                        e.name = '{} - {}'.format(item['Value'], event['EventType'])
                    e.description += '{}: {}\n'.format(item['DisplayName'], item['Value'])

                c2.events.add(e)
            c = c2
            return True
        else:
            print("Request Failed: %d" % r.status_code)
            return False

def LoadCancelFile():
    if(os.path.isfile("cancelled_events.txt")):
        with open("cancelled_events.txt", "r") as f:
            for line in f:
                line = line.strip()
                cancelled_events.add(line)

def UpdateCancelFile():
    with open("cancelled_events.txt", "w") as f:
        for event in cancelled_events:
            f.write(event)
            f.write("\n")

def PreEmbed(embed, events, day):
    msg = ""
    if(events):
        for event in events:
            status_flag = ""
            if(event.begin.to('Europe/Dublin').format("HH:mm DD-MM-YYYY") in cancelled_events):
                status_flag = "~~"
            msg += ("{}{} {} hours {} {}{}\n".format(status_flag, event.begin.to('Europe/Dublin').format("HH:mm"), event.duration.seconds // 3600, event.location, event.name, status_flag))
    if(not msg):
        msg = "No schedule found for {}.\n".format(day.format("ddd Do-MMM"))
    embed.add_field(name="{}.\n".format(day.format("ddd Do-MMM")), value=msg, inline=False)

def GetDaySchedEmbed(day):
    dow = - (int(arrow.utcnow().to('Europe/Dublin').format("d")) - 1) + day
    if(int(arrow.utcnow().to('Europe/Dublin').format("d")) > 5):
        dow += 7
    day = arrow.utcnow().to('Europe/Dublin').shift(days=+dow)

    embed = discord.Embed(title="Schedule for {}".format(day.format("ddd")), color=0x27ff22)

    events = c.timeline.on(day)
    PreEmbed(embed, events, day)

    return embed

def GetWeekSchedEmbed(week_offset):
    dow = int(arrow.utcnow().to('Europe/Dublin').format("d")) - 1
    start_week = arrow.utcnow().to('Europe/Dublin').shift(days =- dow).shift(weeks = week_offset)
    end_week = start_week.shift(days=+4)
    embed = discord.Embed(title="{} Until {}".format(start_week.format("ddd Do-MMM"), end_week.format("ddd Do-MMM-YYYY")), color=0x27ff22)
    for day in arrow.Arrow.range('day', start_week, end_week):
        events = c.timeline.on(day)
        PreEmbed(embed, events, day)

    return embed

def CancelEvent(timedate):
    day = arrow.get(timedate, "HH:mm DD-MM-YYYY", tzinfo='Europe/Dublin')
    events = c.timeline.at(day)
    embed = discord.Embed(title="Cancelling event - {}".format(day.format("ddd Do-MMM")), color=0x27ff22)
    if(events):
        cancelled_events.add(timedate)
        UpdateCancelFile()
        PreEmbed(embed, events, day)
    else:
        embed.add_field(name="Cancellation Failed.", value="No event found on {}.\n".format(day.format("HH:mm ddd Do-MMM")), inline=False)
    return embed

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    cmd = message.content.casefold()

    if cmd.startswith('!mon'):
        embed = GetDaySchedEmbed(0)
        await message.channel.send(embed = embed)

    if cmd.startswith('!tue'):
        embed = GetDaySchedEmbed(1)
        await message.channel.send(embed = embed)

    if cmd.startswith('!wed'):
        embed = GetDaySchedEmbed(2)
        await message.channel.send(embed = embed)

    if cmd.startswith('!thur'):
        embed = GetDaySchedEmbed(3)
        await message.channel.send(embed = embed)

    if cmd.startswith('!fri'):
        embed = GetDaySchedEmbed(4)
        await message.channel.send(embed = embed)

    if cmd.startswith('!today'):
        embed = GetDaySchedEmbed(int(arrow.utcnow().to('Europe/Dublin').format("d")) - 1)
        await message.channel.send(embed = embed)

    if cmd.startswith('!tomorrow'):
        embed = GetDaySchedEmbed(int(arrow.utcnow().to('Europe/Dublin').format("d")))
        await message.channel.send(embed = embed)

    if cmd.startswith('!this week'):
        embed = GetWeekSchedEmbed(0)
        await message.channel.send(embed = embed)

    if cmd.startswith('!next week'):
        embed = GetWeekSchedEmbed(1)
        await message.channel.send(embed = embed)


    if True:
        if cmd.startswith('!close'):
            await client.close()

        if cmd.startswith('!cancel'):
            args = cmd.split()
            if(len(args) < 3):
                await message.channel.send("Expecting 2 arguments, date and time.\nE.g `!cancel 9:00 25-09-19`")

            m = re.search("!cancel (\d+:\d+) (\d+\-\d+\-\d+)", cmd)
            if(m):
                embed = CancelEvent(" ".join(args[1:]))
                await message.channel.send(embed = embed)
            else:
                await message.channel.send("Invalid time date format, please use HH:mm DD-MM-YYYY")

        if cmd.startswith('!reload'):
            if(loadCal()):
                await message.channel.send("Calender has been reloaded")
            else:
                await message.channel.send("Calender failed to reloaded")

    if message.content.startswith('!POWER'):
        await message.channel.send("Can you feel the POWER!?!?!?")

    if message.content.startswith('!power'):
        await message.channel.send("No, try `!POWER`")
    


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

LoadCancelFile()
if(loadCal()):
    client.run(TOKEN)
