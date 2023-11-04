import tgram_bot.build as build

from inspect import getmembers, isfunction
import tgram_bot.functions as funcs

import logging
import logging.handlers as handlers
import sys

logging.basicConfig(
    # format="%(asctime)s [%(levelname)s] %(msg)s",
    format="{name:<40} ({asctime}) [{levelname}] {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        handlers.RotatingFileHandler(
            'app/logs/run.log',
            maxBytes=10*1024*1024,
            backupCount=10
        ),
        logging.StreamHandler(stream=sys.stdout)
    ]
)

log = logging.getLogger("app")
log.setLevel(logging.WARNING)

import nest_asyncio
nest_asyncio.apply()

def run_bot():
    def iscommand(f):
        return isfunction(f) and ('wrapper' not in f.__name__)
    
    functions = dict(getmembers(funcs,iscommand))
    build.bot(functions).run_polling()

log.info("Starting ...")
try: run_bot()
except Exception as ex: log.error(ex)
log.info("Exiting ...")