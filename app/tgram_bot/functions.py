from telegram import Update, Bot
from telegram import error as t_error
from telegram.ext import ContextTypes
import tgram_bot.functions_wraps as wr
import logging
import functools as ft


#Logging shit and giggles
log = logging.getLogger("tgram_bot.functions.py")
log.setLevel(logging.INFO)

def log_wrapper(f):
    @ft.wraps(f)
    async def wrap(update: Update, context:ContextTypes.DEFAULT_TYPE,*args,**kwargs):
        log.info(f'*Starting tgram.function.{f.__name__}*')

        try: await f(update,context,*args,**kwargs)
        except t_error.BadRequest as br:
            log.error(f'{br.message}')
            try: 
                for text,index in enumerate(context.user_data['message'].split('\n')) :log.error(f'{index} {text= }')
            except KeyError: log.error('message not in context.user_data[\'message\']')
        log.info(f'*Finished tgram.function.{f.__name__}*')
    return wrap


# Tha real functions
# Struct: 
#   @p.{restriction}    <-- Who can execute the function 
#   @log_wrapper        <-- Predifined common loggin info
#   async def {fname}(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict): 

@wr.personal
# @wr.unrestricted
@log_wrapper
async def start(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' welcome mesage '''


    context.user_data['message'] = '_Welcome to the internet \.\.\._'
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data['message'],
        parse_mode=data['parse_mode']
    )

# @wr.unrestricted
@log_wrapper
async def test(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' show MarkdownV2 formatting '''

    context.user_data['mesagge'] ='*bold \* text* _italic \* text_ __underline__ ~strikethrough~ ||spoiler|| *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold* [inline URL](http://www.example.com/) [inline mention of a user](tg://user?id=123456789) ![👍](tg://emoji?id=5368324170671202286) `inline fixed-width code` ``` pre-formatted fixed-width code block ``` ```python pre-formatted fixed-width code block written in the Python programming language ```'
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data['mesagge'],
        parse_mode=data['parse_mode']
    )
    context.user_data['mesagge'] = '*bold \* text* _italic \* text_ __underline__ ~strikethrough~ ||spoiler|| *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold* [inline URL](http://www.example.com/) [inline mention of a user](tg://user?id=123456789) ![👍](tg://emoji?id=5368324170671202286) `inline fixed-width code` ``` pre-formatted fixed-width code block ``` ```python pre-formatted fixed-width code block written in the Python programming language ```'
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data['mesagge'],
    )

# @wr.unrestricted
@log_wrapper
async def whoami(update:Update, context:ContextTypes.DEFAULT_TYPE, data: dict) -> None:
    ''' return sender data '''

    username = update.effective_user.username
    userid = update.effective_user.id
    name = update.effective_user.first_name
    chatid = update.effective_chat.id

    context.user_data['message']=(
        f'@{username}\n'
        f'{userid = }\n'
        f'{name = }\n'
        f'{chatid = }'
    ).translate(data['trans_table'])
    
    try:
        await context.bot.send_message(
            chat_id=chatid,
            text=context.user_data['message'],
            parse_mode=data['parse_mode']
        )
    except t_error.BadRequest as br:
        log.error()

@wr.personal
@wr.owner
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

@wr.personal
@wr.owner
@log_wrapper
async def pull_claimed(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' get info of already looted offers '''

    from pull import pull_orders_info
    await pull_orders_info()
    with open('app/data/pull.log','r') as f: context.user_data['message'] = ''.join(f.readlines())

    context.user_data['message'] = context.user_data['message'].split('\n\n')

    for text in context.user_data['message']:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=data['parse_mode']
        )

@wr.personal
@wr.owner
@log_wrapper
async def log_file(update:Update, context:ContextTypes.DEFAULT_TYPE,data:dict) -> None:
    ''' get latest log file '''

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='app/logs/run.log'
    )
