import asyncio
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, \
    ContextTypes, Application, \
    CommandHandler, MessageHandler

from os import environ as env
from functools import partial

import logging
log = logging.getLogger('tgram_bot.build.py')
log.setLevel(logging.INFO)

def bot(functions: dict) -> Application:
    TOKEN = env['TGRAM_TOKEN']
    app = ApplicationBuilder().token(TOKEN).build()

    # Necesary data for 1 or more handle functions
    options = {
        'app': app,
        'parse_mode': 'MarkdownV2',
    }

    log.info('Initializing CommandHandlers ...')
    for key,value in zip(functions.keys(),functions.values()):
        # CommandHandlers inicialization
        value_h = partial(value,data=options)
        app.add_handler(CommandHandler(key,value_h))
    
    async def bot_set_commands(app: Application, functions: dict):
        commands = []
        for key,value in zip(functions.keys(),functions.values()):
            commands.append(BotCommand(key,value.__doc__))
        
        async with app: await app.bot.set_my_commands(commands)

    log.info('Setting Command List ...')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot_set_commands(app,functions))    


    return app
