import logging
import sys

from creds import TOKEN
from client import bot

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"


logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT)

if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN variable missing or empty.",
        file=sys.stderr)
