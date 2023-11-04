from telegram import Update
from telegram.ext import ContextTypes
import tgram_bot.permission_wraps as p
import logging
import functools as ft

#Logging shit and giggles
log = logging.getLogger("tgram_bot.functions.py")
log.setLevel(logging.INFO)
log_exec = "Executing \\{} chat command ..."
log_fin = "Fin \\{} "

def log_wrapper(f):
    @ft.wraps(f)
    async def wrap(update: Update, context:ContextTypes.DEFAULT_TYPE,*args,**kwargs):
        log.info(f'*Starting tgram.function.{f.__name__}*')
        await f(update,context,*args,**kwargs)
        log.info(f'*Finished tgram.function.{f.__name__}*')
    return wrap


# Tha real functions
# Struct: 
#   @p.{restriction}    <-- Who can execute the function 
#   @log_wrapper        <-- Predifined common loggin info


@p.unrestricted
@log_wrapper
async def test(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' show MarkdownV2 formatting '''

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='*bold \* text* _italic \* text_ __underline__ ~strikethrough~ ||spoiler|| *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold* [inline URL](http://www.example.com/) [inline mention of a user](tg://user?id=123456789) ![👍](tg://emoji?id=5368324170671202286) `inline fixed-width code` ``` pre-formatted fixed-width code block ``` ```python pre-formatted fixed-width code block written in the Python programming language ```',
        parse_mode=data['parse_mode']
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='*bold \* text* _italic \* text_ __underline__ ~strikethrough~ ||spoiler|| *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold* [inline URL](http://www.example.com/) [inline mention of a user](tg://user?id=123456789) ![👍](tg://emoji?id=5368324170671202286) `inline fixed-width code` ``` pre-formatted fixed-width code block ``` ```python pre-formatted fixed-width code block written in the Python programming language ```',
    )
    

@p.unrestricted
@log_wrapper
async def start(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' welcome mesage '''

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='_Welcome to the internet \.\.\._',
        parse_mode=data['parse_mode']
    )

@p.owner
@log_wrapper
async def loot(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' loot things '''

    from loot import primelooter
    await primelooter('app/cookies.txt')
    # with open('app/data/loot.log', 'r') as f: data['loot_text'] = ''.join(f.readlines())

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='app/data/loot.log'
        # text=data['loot_text'].replace('.','\\.'),
        # parse_mode=data['parse_mode']
    )

@p.owner
@log_wrapper
async def pull_claimed(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' get info of already looted offers '''

    from pull import pull_orders_info
    await pull_orders_info()
    with open('app/data/pull.log','r') as f: data['pull_text'] = ''.join(f.readlines())

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=data['pull_text'],
        parse_mode=data['parse_mode']
    )


@p.owner
@log_wrapper
async def log_file(update:Update, context:ContextTypes.DEFAULT_TYPE,data:dict) -> None:
    ''' get latest log file '''
    log.info(log_exec.format("log"))

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='app/logs/run.log'
    )
