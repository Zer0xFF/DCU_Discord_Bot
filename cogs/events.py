import discord
import traceback

from datetime import datetime
from discord.ext import commands
from discord.ext.commands import errors


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        await ctx.send_help(str(ctx.invoked_subcommand))
    else:
        await ctx.send_help(str(ctx.command))


class Events(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, errors.MissingRequiredArgument) or isinstance(
            error, errors.BadArgument
        ):
            await send_cmd_help(ctx)

        elif isinstance(error, errors.CommandNotFound):
            pass

        elif isinstance(error, errors.CommandInvokeError):
            error = error.original

            _traceback = "".join(traceback.format_tb(error.__traceback__))
            error = f"```py\n{_traceback}{type(error).__name__}: {error}\n```"

            await ctx.send(
                f"There was an error processing your command.\n Please check your console for more information."
            )
            print(error)

        elif isinstance(error, errors.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown... try again in {error.retry_after:.2f} seconds."
            )

        elif isinstance(error, errors.CheckFailure):
            pass


def setup(bot):
    bot.add_cog(Events(bot))
