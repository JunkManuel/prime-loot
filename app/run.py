import tgram_bot.build as build

from inspect import getmembers, isfunction
import tgram_bot.functions as funcs

import logging
import sys
logging.basicConfig(
    # format="%(asctime)s [%(levelname)s] %(msg)s",
    format="{asctime} [{levelname}] {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.handlers.RotatingFileHandler(
            'app/logs/tgram_bot_run.log',
            maxBytes=10*1024*1024,
            backupCount=10
        ),
        logging.StreamHandler(stream=sys.stdout)
    ]
)

log = logging.getLogger(name="telegram-bot")
log.setLevel(logging.WARNING)

import nest_asyncio
nest_asyncio.apply()

def run_bot():
    functions = dict(getmembers(funcs,isfunction))
    build.bot(functions).run_polling()

run_bot()