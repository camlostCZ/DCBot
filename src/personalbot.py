import logging

from creds import *
from client import bot

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"


logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT)

bot.run(TOKEN)
