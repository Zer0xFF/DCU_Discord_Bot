import os

import discord
from discord.ext.commands import AutoShardedBot, DefaultHelpCommand

TOKEN = "TOKENHERE"


class HelpFormat(DefaultHelpCommand):
    async def send_error_message(self, error):
        destination = self.context.channel
        await destination.send(error)

    async def send_command_help(self, command):
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages()

    async def send_pages(self):
        destination = self.context.channel
        try:
            for page in self.paginator.pages:
                await destination.send(page)
        except discord.Forbidden:
            print("Couldn't send the help due to permission issues.")


class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_message(self, message):
        if (
            not self.is_ready()
            or message.author.bot
            or not (
                isinstance(message.channel, discord.DMChannel)
                or message.channel.permissions_for(message.guild.me).send_messages
            )
        ):
            return

        await self.process_commands(message)


print("Logging in...")
bot = Bot(
    command_prefix="!", prefix="!", command_attrs=dict(hidden=True), help_command=HelpFormat()
)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

bot.run(TOKEN)
