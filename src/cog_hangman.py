import logging
import random

from discord.ext import commands

from conf import HANGMAN_PATH


class OneGame:
    def __init__(self, player_name: str) -> None:
        self._player = player_name
        self._secret = self.choose_secret_word(HANGMAN_PATH)
        self._progress = "-" * len(self._secret)


    def choose_secret_word(self, path: str) -> str:
        with open(path, encoding="UTF-8") as f:
            words = f.readlines()

        result = random.choice(words).strip()
        logging.debug(f"Secret word: {result}")
        return result


class HangmanGame(commands.Cog):
    def __init__(self, bot) -> None:
        self._bot = bot
        self._games: dict[str, OneGame] = {}     # Dictionary of running games, player name is the key


    def start_game(self, player: str) -> str:
        result = "Hra Hangman již běží. Hádej písmeno."
        if player not in self._games:
            try:                
                game = OneGame(player)
                self._games[player] = game
                secret = game._secret
                result = f"Hra byla spuštěna.\nHledané slovo: `{secret}`"
            except:
                result = "Hangman - došlo k neočekávané chybě."
        return result


    def stop_game(self, player: str) -> str:
        result = "Hru Hangman zatím nehraješ. Spusť ji příkazem !hangman."
        if player in self._games:
            game = self._games.pop(player)
            result = f"Jsi mrtev.\nHledané slovo bylo: `{game._secret}`"
        return result


    @commands.command(name="hangman", help="Hra Hangman / Oběšenec - hádání slov")
    async def hangman(self, ctx, *args):
        cmd = ("".join(args)).lower()
        sender = ctx.author
        response = "Chyba - je třeba zadat jen jedno písmeno."
        if len(cmd) == 1:
            # TODO a letter - a tip
            response = "Pěkný tip. Ale bohužel!"
        elif cmd == "":     #Start a game
            response = self.start_game(sender.display_name)
        elif cmd == "/kill":
            response = self.stop_game(sender.display_name)

        await sender.create_dm()
        await sender.dm_channel.send(response)
