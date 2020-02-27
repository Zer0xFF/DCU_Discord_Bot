import sys
sys.path.append('../ai-dungeon-cli/')

import ai_dungeon_cli
from ai_dungeon_cli.ai_dungeon_cli import AI_D as AI
import aiohttp
import discord
from discord.ext import commands


class AI_Dungeon(commands.Cog):
    """Dublin Bus Times"""

    def __init__(self, bot):
        self.bot = bot
        self.session = AI()
        self.session.start_session()

    def cog_unload(self):
        pass

    @commands.has_any_role("OVERLORDS", "Mahmood")
    @commands.command()
    async def start_game(self, ctx):
        """Ai Dungeon"""
        self.session.set_context(ctx)
        self.session.start_game()
        await self.session.msg()

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.author.bot
            or not (
                isinstance(message.channel, discord.DMChannel)
                or message.channel.permissions_for(message.guild.me).send_messages
            )
            or message.content[0] == '!'
        ):
            return

        if(message.channel.name == "ai_dungeon2"):
            res = self.session.process_next_action(message.content)
            self.session.set_context(message.channel)
            await self.session.msg()
            action_type, action_res = res
            if action_type == 'regular':
                self.session.prompt_i += 2

def setup(bot):
    bot.add_cog(AI_Dungeon(bot))
