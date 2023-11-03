import btelegram.build as build

from inspect import getmembers, isfunction
import btelegram.functions as funcs

import logging
logging.basicConfig(
    level=logging.INFO,
    # format="%(asctime)s [%(levelname)s] %(msg)s",
    format="{asctime} [{levelname}] {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S"
)

log = logging.getLogger()

import nest_asyncio
nest_asyncio.apply()

def run_bot():
    functions = dict(getmembers(funcs,isfunction))
    build.bot(functions).run_polling()

run_bot()