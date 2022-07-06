import logging
import random

from discord.ext import commands

from conf import HANGMAN_WORDS, HANGMAN_RESPONSE, HANGMAN_IMAGE_FMT

GUESS_MAX_COUNT = 9


class OneGame:
    GUESS_BAD = 0
    GUESS_PREVIOUS = 1
    GUESS_OK = 2
    GUESS_TOOMANY = 3
    GUESS_SUCCESS = 4


    def __init__(self, player_name: str) -> None:
        self._player = player_name
        self._secret = self.choose_secret_word(HANGMAN_WORDS)
        self._progress = "-" * len(self._secret)
        self._previous = set()
        self._guess_count = 0


    def choose_secret_word(self, path: str) -> str:
        with open(path, encoding="UTF-8") as f:
            words = f.readlines()

        result = random.choice(words).strip().lower()
        logging.debug(f"Secret word: {result}")
        return result


    def make_guess(self, letter: str) -> tuple[int, str, str]:
        if letter in self._previous:
            prev = " ,".join(sorted(list(self._previous)))
            self._guess_count += 1
            result = (OneGame.GUESS_PREVIOUS, self._progress, prev)
            if self._guess_count >= GUESS_MAX_COUNT:
                result = (OneGame.GUESS_TOOMANY, self._progress, prev)
        else:
            self._previous.add(letter)
            prev = " ,".join(sorted(list(self._previous)))
            if letter not in self._secret:
                self._guess_count += 1
                result = (OneGame.GUESS_BAD, self._progress, prev)
                if self._guess_count >= GUESS_MAX_COUNT:
                    result = (OneGame.GUESS_TOOMANY, self._progress, prev)
            else:   # Good guess
                word = self._replace_char(letter)
                self._progress = word
                result = (OneGame.GUESS_OK, word, prev)
                if self._progress == self._secret:
                    result = (OneGame.GUESS_SUCCESS, word, prev)
        return result

    
    def _replace_char(self, letter: str) -> str:
        result = ""
        for orig, guessed in zip(self._secret, self._progress):
            ch = "-"
            if guessed != "-":  # Already a known letter
                ch = guessed
            elif letter == orig:    # Good guess
                ch = orig
            result += ch
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
            result = f"Jsi mrtev.\nHledané slovo bylo: `{game._secret}`"
        return result


    def play_game(self, player: str, letter: str) -> str:
        result = "Hru Hangman zatím nehraješ. Spusť ji příkazem !hangman."
        if player in self._games:
            guess_result, word, previous = self._games[player].make_guess(letter)
            result = f"""
                {HANGMAN_RESPONSE[guess_result]}\n
                Tipovaná písmena: {previous}
                Postup: `{word}`
                """
            if guess_result == OneGame.GUESS_TOOMANY:
                result = self.stop_game(player)
            elif guess_result == OneGame.GUESS_SUCCESS:
                self.stop_game(player)
                result = HANGMAN_RESPONSE[guess_result]
        return result


    @commands.command(name="hangman", help="Hra Hangman / Oběšenec - hádání slov")
    async def hangman(self, ctx, *args):
        cmd = ("".join(args)).lower()
        sender = ctx.author
        response = "Chyba - je třeba zadat jen jedno písmeno."
        if len(cmd) == 1:   # a letter - a guess
            response = self.play_game(sender.display_name, cmd)
        elif cmd == "":     # Start a game
            response = self.start_game(sender.display_name)
        elif cmd == "/kill":
            response = self.stop_game(sender.display_name)

        await sender.create_dm()
        await sender.dm_channel.send(response)
