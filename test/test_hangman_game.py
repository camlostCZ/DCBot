import pytest

from conf import HANGMAN_RESPONSE
from hangman_game import HangmanGame, HangmanGuessType

PLAYER = "test"
SECRET = "hello"


@pytest.fixture
def new_game():
    """
    New Hangman game but with a known word.
    """
    result = HangmanGame(PLAYER)
    result._secret = SECRET
    result._progress = "-" * len(result._secret)
    return result


def test_status_new_game(new_game: HangmanGame):
    """
    Test if a newly created game has correct properties.

    """
    count, previous, word, img_path = new_game.get_status()
    assert count == 0
    assert len(previous) == 0
    assert word == "-" * len(new_game._secret)
    assert img_path == ""


def test_make_bad_guess(new_game: HangmanGame):
    """
    Test properties of a game after a bad guess.
    """
    orig_count = new_game._guess_count
    guess = new_game.make_guess("a")
    assert guess == HangmanGuessType.GUESS_BAD
    count, previous, word, img_path = new_game.get_status()
    assert count == orig_count + 1
    assert "a" in previous
    assert "01" in img_path


def test_make_good_guess(new_game: HangmanGame):
    """
    Test game properties after a good guess.
    The number of letters in `word` should be the same as in `SECRET`.
    """
    orig_count = new_game._guess_count
    guess = new_game.make_guess("l")
    assert guess == HangmanGuessType.GUESS_OK
    count, previous, word, img_path = new_game.get_status()
    assert count == orig_count
    assert word.count("l") == SECRET.count("l")


def test_make_toomany_guesses(new_game: HangmanGame):
    """
    Test the result of make_guess() after 9 bad attempts.
    """
    for _ in range(9):
        guess = new_game.make_guess("x")
    assert guess == HangmanGuessType.GUESS_TOOMANY


def test_hangman_guess_type():
    guess_type = HangmanGuessType.GUESS_PREVIOUS
    assert str(guess_type) == HANGMAN_RESPONSE[guess_type.value]
