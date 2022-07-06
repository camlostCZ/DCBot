# File with Hangman words
HANGMAN_WORDS = "./resources/hangman/hangman_words.txt"

HANGMAN_IMAGE_FMT = "./resources/hangman/hangman-game-{}.png"

HANGMAN_RESPONSE = [
    "Bohužel, toto písmeno není v hledaném slově.",
    "Písmeno již bylo zadáno v předchozích pokusech.",
    "Správně! Písmeno je v hledaném slově.",
    "Jsi mrtev! Počet pokusů byl vyčerpán.",
    "Správně! Zachránil sis holý život!"
]

# Pattern used to validate input before calling eval().
# Allowed chars: 0-9, *, /, +, -, space, (, ), and ^.
PATTERN_CALC_VALIDATION = r"^[0-9+\-*\/^\(\)\. ]+$"

# URL use to fetch jokes
URL_JOKES = "https://vysmatej.cz/nahodne-vtipy/"