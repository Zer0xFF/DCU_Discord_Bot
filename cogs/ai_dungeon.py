import sys
sys.path.append('../ai_dungeon_cli/')

from ai_dungeon_cli import ai_dungeon_cli
import aiohttp
import discord
from discord.ext import commands
import collections


class AI_Dungeon(commands.Cog):
    """I_Dungeon"""
    def __init__(self, bot):
        self.bot = bot
        self.pending_msg = collections.deque()
        self.pending_input = collections.deque()
        self.session = ai_dungeon_cli.AiDungeon()
        ai_dungeon_cli.set_input(lambda *args : self.pending_input.popleft())
        ai_dungeon_cli.set_print(lambda txt : self.discord_queue_msg(txt))

        # Login if necessary
        if not self.session.get_auth_token():
            self.session.login()

        # Update the session authentication token
        self.session.update_session_auth()


    def cog_unload(self):
        pass

    def discord_get_msg(self):
        if(len(self.pending_msg) > 0):
            return self.pending_msg.popleft()

    def discord_queue_msg(self, txt):
        self.pending_msg.append("```{}```".format(txt))

    @commands.has_any_role("OVERLORDS", "Mahmood")
    @commands.command()
    async def start_game(self, ctx, setting_id, character_id, character_name="Zer0xFF"):
        """Ai Dungeon"""
        self.pending_input.append(setting_id)
        self.pending_input.append(character_id)
        if(setting_id == "5"):
            self.pending_input.append(character_name)

        # Loads the current session configuration
        self.session.choose_config()
        # Initializes the story
        self.session.init_story()
        while(len(self.pending_msg) > 0):
            await ctx.send(self.discord_get_msg())

        self.pending_input.clear()

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.author.bot
            or not (
                isinstance(message.channel, discord.DMChannel)
                or message.channel.permissions_for(message.guild.me).send_messages
            )
            or not message.content or message.content[0] == '!'
        ):
            return

        if(message.channel.name == "ai_dungeon2"):
            self.pending_input.append(message.content)

            self.session.process_next_action()
            while(len(self.pending_msg) > 0):
                await message.channel.send(self.discord_get_msg())

def setup(bot):
    bot.add_cog(AI_Dungeon(bot))
