import tgram_bot.build as build

from inspect import getmembers, isfunction
from os import environ as env
import asyncio
import tgram_bot.functions as funcs

import logging
import logging.handlers as handlers
import sys

logging.basicConfig(
    # format="%(asctime)s [%(levelname)s] %(msg)s",
    format="({asctime}) {name:<30} [{levelname:>8}] --- {message}",
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
log.setLevel(logging.INFO)

# import nest_asyncio
# nest_asyncio.apply()

async def send_starting(bot: build.Application):
    async with bot:
        await bot.send_message(
            chat_id = env['TGRAM_STATUS_CHAT_ID'],
            text='Starting ...'
        )

# async def send_closing(bot: build.Application):
    # async with bot:
        # await bot.send_message(
            # chat_id = env['TGRAM_STATUS_CHAT_ID'],
            # text='Closing ...'
        # )

async def send_warning_message(bot: build.Application):
    async with bot:
        await bot.send_message(
            chat_id = env['TGRAM_STATUS_CHAT_ID'],
            text= "_Something went *VERY* wrong \.\.\._",
            parse_mode= "MarkdownV2"
        )

def get_app():
    def iscommand(f):
        return isfunction(f) and ('wrapper' not in f.__name__) and ('menu' not in f.__name__)
    
    functions = dict(getmembers(funcs,iscommand))
    return build.app(functions)

def get_bot():
    return build.bot()

app = get_app()
loop = asyncio.get_event_loop()

    
log.info("Starting ...")
loop.run_until_complete(send_starting(get_bot()))

try: app.run_polling()

except Exception as ex:
    loop.run_until_complete(send_warning_message(get_bot()))
    logging.exception(ex)

# log.info("Exiting ...")
# loop.run_until_complete(send_closing(get_bot()))