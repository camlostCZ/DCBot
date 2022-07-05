from discord.ext import commands


class HangmanGame(commands.Cog):
    def __init__(self, bot) -> None:
        self._bot = bot
