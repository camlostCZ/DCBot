import logging

import discord
from discord.ext import commands

from conf import HANGMAN_RESPONSE
from hangman_game import HangmanGame, HangmanGuessType


class CogHangman(commands.Cog):
    def __init__(self, bot) -> None:
        self._bot = bot
        self._games: dict[str, HangmanGame] = {}     # Dictionary of running games, player name is the key


    def start_game(self, player: str) -> str:
        result = "Hra Hangman již běží. Hádej písmeno."
        if player not in self._games:
            try:                
                game = HangmanGame(player)
                self._games[player] = game
                word = game._progress
                result = f"Hra byla spuštěna.\nHledané slovo: `{word}`"
            except:
                result = "Hangman - došlo k neočekávané chybě."
                logging.error("Hangman - error in start_game(). Missing file?")
        return result


    def stop_game(self, player: str) -> str:
        result = "Hru Hangman zatím nehraješ. Spusť ji příkazem !hangman."
        if player in self._games:
            game = self._games.pop(player)
            game.stop()
            _, _, _, path = game.get_status()
            result = f"Jsi mrtev.\nHledané slovo bylo: `{game._secret}`"
        return (result, path)


    def play_game(self, player: str, letter: str) -> tuple[str, str]:
        logging.debug(f"play_game(): player={player}, letter={letter}")
        result = "Hru Hangman zatím nehraješ. Spusť ji příkazem !hangman."
        if player in self._games:
            logging.debug(f"play_game(): game found for player {player}.")
            game = self._games[player]
            guess = game.make_guess(letter)
            logging.debug(f"play_game(): guess result: {guess}")
            steps, history, word, path = game.get_status()
            used_letters = " ,".join(history)
            logging.debug(f"play_game(): game status: steps={steps}, history={used_letters}, word={word}, img={path}")
            result = f"""
                {HANGMAN_RESPONSE[guess.value]}\n
                Tipovaná písmena: {used_letters}
                Postup: `{word}`
                """
            if guess == HangmanGuessType.GUESS_TOOMANY:
                result = self.stop_game(player)
            elif guess == HangmanGuessType.GUESS_SUCCESS:
                self.stop_game(player)
                result = HANGMAN_RESPONSE[guess]
        return (result, path)


    @commands.command(name="hangman", help="Hra Hangman / Oběšenec - hádání slov")
    async def hangman(self, ctx, *args):
        cmd = ("".join(args)).lower()
        sender = ctx.author

        path = ""
        response = "Chyba - je třeba zadat jen jedno písmeno."
        if len(cmd) == 1:   # a letter - a guess
            response, path = self.play_game(sender.display_name, cmd)
        elif cmd == "":     # Start a game
            response = self.start_game(sender.display_name)
        elif cmd == "/kill":
            response, path = self.stop_game(sender.display_name)

        await sender.create_dm()
        if path:
            await sender.dm_channel.send(response, file=discord.File(path))
        else:
            await sender.dm_channel.send(response)
