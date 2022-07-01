import random

import discord
from discord.ext import commands


class GuessNumberGame(commands.Cog):
    MAX_NUMBER = 100
    MIN_NUMBER = 1


    def __init__(self, bot) -> None:
        self.bot = bot
        self._is_running = False
        self._secret_number = -1


    def start_game(self):
        self._secret_number = random.randint(
            GuessNumberGame.MIN_NUMBER,
            GuessNumberGame.MAX_NUMBER)
        self._is_running = True


    def stop_game(self):
        self._is_running = False


    @commands.command(name="guess", help="Hra hádání čísel", brief="Syntax: !guess start|stop|<číslo>")
    async def guess(self, ctx, arg: str):
        cmd = arg.lower()
        if cmd == "start":  # Start a new game
            if self._is_running:
                await ctx.send("Hra již běží.")
            else:
                self.start_game()
                await ctx.send(f"Hádej číslo od {GuessNumberGame.MIN_NUMBER} do {GuessNumberGame.MAX_NUMBER}.")
        elif cmd == "stop":  # Stop the current game
            if self._is_running:
                self.stop_game()
                await ctx.send(f"Hra ukončena. Hledané číslo: {self._secret_number}.")
            else:
                await ctx.send("Hra něběží. Nelze ji ukončit.")
        else:  # This is a guess
            sender = ctx.author.display_name
            if self._is_running:
                try:
                    guess = int(arg)
                    if guess == self._secret_number:
                        self.stop_game()
                        await ctx.send(f"@{sender} Vyhrál! Hledané číslo: {self._secret_number}")
                    elif guess < self._secret_number:
                        await ctx.send(f"@{sender} Hledané číslo je větší.")
                    else:
                        await ctx.send(f"@{sender} Hledané číslo je menší.")
                except ValueError:
                    await ctx.send(f"@{sender} Chybné zadání.")
            else:
                await ctx.send(f"@{sender} Hra neběží. Nejprve ji spusť příkazem !guess start.")
