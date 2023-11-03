import tgram_bot.build as build

from inspect import getmembers, isfunction
import tgram_bot.functions as funcs

import logging
logging.basicConfig(
    # format="%(asctime)s [%(levelname)s] %(msg)s",
    format="{asctime} [{levelname}] {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S"
)

log = logging.getLogger(name="telegram-bot")
log.setLevel(logging.WARNING)

import nest_asyncio
nest_asyncio.apply()

def run_bot():
    functions = dict(getmembers(funcs,isfunction))
    build.bot(functions).run_polling()

run_bot()