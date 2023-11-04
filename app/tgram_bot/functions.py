from telegram import Update
from telegram.ext import ContextTypes
import tgram_bot.permission_wraps as p
import logging

log = logging.getLogger("tgram_bot.functions.py")
log.setLevel(logging.INFO)
log_exec = "Executing \\{} chat command ..."
log_fin = "Fin \\{} "

@p.unrestricted
async def test(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' show MarkdownV2 formatting '''
    log.info(log_exec.format("test"))

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='*bold \* text* _italic \* text_ __underline__ ~strikethrough~ ||spoiler|| *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold* [inline URL](http://www.example.com/) [inline mention of a user](tg://user?id=123456789) ![👍](tg://emoji?id=5368324170671202286) `inline fixed-width code` ``` pre-formatted fixed-width code block ``` ```python pre-formatted fixed-width code block written in the Python programming language ```',
        parse_mode=data['parse_mode']
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='*bold \* text* _italic \* text_ __underline__ ~strikethrough~ ||spoiler|| *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold* [inline URL](http://www.example.com/) [inline mention of a user](tg://user?id=123456789) ![👍](tg://emoji?id=5368324170671202286) `inline fixed-width code` ``` pre-formatted fixed-width code block ``` ```python pre-formatted fixed-width code block written in the Python programming language ```',
    )
    
    log.info(log_fin.format("test"))

@p.unrestricted
async def start(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' welcome mesage '''
    log.info(log_exec.format("start"))

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='_Welcome to the internet \.\.\._',
        parse_mode=data['parse_mode']
    )

    log.info(log_fin.format("start"))

@p.owner
async def loot(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' loot things '''
    log.info(log_exec.format("loot"))

    from loot import primelooter
    await primelooter('app/cookies.txt')
    # with open('app/data/loot.log', 'r') as f: data['loot_text'] = ''.join(f.readlines())

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='app/data/loot.log'
        # text=data['loot_text'].replace('.','\\.'),
        # parse_mode=data['parse_mode']
    )

    log.info(log_fin.format("loot"))

@p.owner
async def pull_claimed(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' get info of already looted offers '''
    log.info(log_exec.format("pull_claimed"))

    from pull import pull_orders_info
    await pull_orders_info()
    with open('app/data/pull.log','r') as f: data['pull_text'] = ''.join(f.readlines())

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=data['pull_text'],
        parse_mode=data['parse_mode']
    )

    log.info(log_fin.format("pull_claimed"))

@p.owner
async def log_file(update:Update, context:ContextTypes.DEFAULT_TYPE,data:dict) -> None:
    ''' get latest log file '''
    log.info(log_exec.format("log"))

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='app/logs/run.log'
    )

    log.info(log_fin.format("log"))