import asyncio
from telegram import Update, BotCommand, Bot
from telegram.ext import ApplicationBuilder, \
    ContextTypes, Application, \
    CommandHandler, MessageHandler, CallbackQueryHandler

from os import environ as env
from functools import partial

import logging
log = logging.getLogger('tgram_bot.build.py')
log.setLevel(logging.INFO)

def app(commandhandlers: dict, querycallbackhandlers: dict) -> Application:
    TOKEN = env['TGRAM_TOKEN']
    
    try: app = ApplicationBuilder().token(TOKEN).build()
    except Exception as ex: logging.exception(ex)


    # Necesary data for 1 or more handle functions
    options = {
        'trans_table':str.maketrans({
            '.':r'\.', '>':r'\>',
            '[':r'\[',']':r'\]',
            '(':r'\(',')':r'\)',
            '-':r'\-','=':r'\='
        }),
        'app': app,
        'parse_mode': 'MarkdownV2',
    }

    log.info('Initializing CommandHandlers ...')
    for key,value in zip(commandhandlers.keys(),commandhandlers.values()):
        # CommandHandlers inicialization
        value_h = partial(value,data=options)
        app.add_handler(CommandHandler(key,value_h))
    
    async def bot_set_commands(app: Application, functions: dict):
        commands = []
        functions = dict(sorted(functions.items()))
        for key,value in functions.items():
            commands.append(BotCommand(key,value.__doc__))
        async with app: await app.bot.set_my_commands(commands)

    log.info('Initializing QueryCallbackHandlers')
    for key,value in querycallbackhandlers.items():
        app.add_handler(CallbackQueryHandler(value, pattern=key))

    log.info('Setting Command List ...')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot_set_commands(app,functions= commandhandlers))

    return app

def bot():
    TOKEN = env['TGRAM_TOKEN']
    try: bot = Bot(token=TOKEN)
    except Exception as ex: logging.exception(ex)

    return bot
