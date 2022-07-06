import logging
import random

from enum import Enum

from conf import HANGMAN_RESPONSE, HANGMAN_WORDS, HANGMAN_IMAGE_FMT

GUESS_MAX_COUNT = 9


class HangmanGuessType(Enum):
    GUESS_BAD = 0
    GUESS_PREVIOUS = 1
    GUESS_OK = 2
    GUESS_TOOMANY = 3
    GUESS_SUCCESS = 4


    def __str__(self) -> str:
        return HANGMAN_RESPONSE[self.value]


class HangmanGame:
    def __init__(self, player_name: str) -> None:
        self._player = player_name
        self._secret = self.choose_secret_word(HANGMAN_WORDS)
        self._progress = "-" * len(self._secret)
        self._previous = set()
        self._guess_count = 0


    def get_status(self) -> tuple[int, list[str], str, str]:
        """
        Returns an information about the currect game status:
        - number of bad attempts
        - list of previously used letters
        - a word with the known letters unmasked
        - path to an image file
        """
        result = (
            self._guess_count,
            sorted(list(self._previous)),
            self._progress,
            HANGMAN_IMAGE_FMT.format(self._guess_count) if self._guess_count > 0 else ""
        )
        return result


    def choose_secret_word(self, path: str) -> str:
        """
        Choose a secret word from a text file (one word per line).

        Args:
            path (str): Path to a source file

        Returns:
            str: A secret word

        Raises:
            Exceptions related to file operations
        """
        with open(path, encoding="UTF-8") as f:
            words = f.readlines()

        result = random.choice(words).strip().lower()
        logging.debug(f"Secret word: {result}")
        return result


    def make_guess(self, letter: str) -> HangmanGuessType:
        """
        Make a guess and return if it was a successful one
        or what type of guess it was.

        Args:
            letter (str): A letter guessed by the player

        Returns:
            One of HangmanGuessType.GUESS_* constants.
        """
        self._guess_count += 1      # Probably a bad guess
        if letter in self._previous:    # Letter used previously
            result = HangmanGuessType.GUESS_PREVIOUS
        else:
            if letter not in self._secret:  # Bad guess
                result = HangmanGuessType.GUESS_BAD
            else:   # Good guess
                self._guess_count -= 1  # Revert previously added attempt
                self._progress = self._replace_char(letter)
                result = HangmanGuessType.GUESS_OK
                if self._progress == self._secret:
                    result = HangmanGuessType.GUESS_SUCCESS

        self._previous.add(letter)
        if self._guess_count >= GUESS_MAX_COUNT:
            result = HangmanGuessType.GUESS_TOOMANY
        return result

    
    def _replace_char(self, letter: str) -> str:
        """
        Replace all hidden characters in guessed word by a letter
        if the letter is in the secret word.

        Args:
            letter (str): A letter guessed by the user

        Returns:
            str: A string with known letters already visible and
            unknowns still hidden
        """
        result = ""
        for orig, guessed in zip(self._secret, self._progress):
            ch = "-"
            if guessed != "-":  # A already known letter
                ch = guessed
            elif letter == orig:    # Good guess
                ch = orig
            result += ch
        return result
