from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import error as t_error
from telegram.ext import ContextTypes
import tgram_bot.functions_wraps as wr
import logging
import functools as ft
import asyncio


#Logging shit and giggles
log = logging.getLogger("tgram_bot.functions.py")
log.setLevel(logging.INFO)

def log_wrapper(f):
    @ft.wraps(f)
    async def wrap(update: Update, context:ContextTypes.DEFAULT_TYPE,*args,**kwargs):
        async def send_warning_message(update:Update,context:ContextTypes):
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text= "_Something went wrong_",
                parse_mode= "MarkdownV2"
            )
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text= "Check \/log\_file for more information",
                parse_mode= "MarkdownV2"
            )

        log.info(f'*Starting tgram.function.{f.__name__}*')

        try: await f(update,context,*args,**kwargs)

        except t_error.BadRequest as br:
            log.error(f'BadRequest: {br.message}')
            try: 
                for text,index in enumerate(context.user_data['message'].split('\n')) :log.error(f'{index} {text= }')
            except KeyError: log.error('Could not log text string: No send_message() function or message(text) not in context.user_data[\'message\']')
            finally: return

            await send_warning_message(update,context)
        
        except FileNotFoundError as fnf:
            log.error(f'{fnf.args[0]}')
            log.error(f'Filename -> {fnf.filename}')
            await send_warning_message(update,context)
        
        except Exception as ex:
            logging.exception(ex)
            await send_warning_message(update,context)
            
        
        log.info(f'*Finished tgram.function.{f.__name__}*')

    return wrap


# ------------------------------------------------------------------------------------------------------------

# Tha real functions
# Struct: 
#   @wr.{restriction}    <-- Who can execute the function 
#   @log_wrapper        <-- Predifined common loggin info
#   async def {fname}(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict): 

# Command Handlers

@wr.personal
# @wr.unrestricted
@log_wrapper
async def start(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' Welcome mesage '''


    context.user_data['message'] = '_Welcome to the internet \.\.\._'
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data['message'],
        parse_mode=data['parse_mode']
    )

# @wr.unrestricted
@log_wrapper
async def test(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    '''Usage: /test --- Show MarkdownV2 formatting '''

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
    '''Usage: /whoami --- Return sender data '''

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
    
    await context.bot.send_message(
        chat_id=chatid,
        text=context.user_data['message'],
        parse_mode=data['parse_mode']
    )

@wr.personal
@wr.owner
@log_wrapper
async def loot(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' Usage: /loot --- Loot inGameLoot '''

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
async def loot_fgwp(update:Update, context:ContextTypes.DEFAULT_TYPE, data: dict) -> None:
    ''' Usage: /loot_fgwp --- Loot Games '''

    import loot_fgwp
    await loot_fgwp.main('app/cookies.txt')

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='app/data/loot_fgwp.log'
    )



@wr.personal
@wr.owner
@log_wrapper
async def pull_claimed(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' usage: /pull_claimed ¿[type]? [key] --- Get info of all/[key]-named looted offers within [type] offers '''

    from pull import pull_orders_info
    context.user_data['find_key'] = None
    if context.args: context.user_data['find_key'] = context.args[0]

    await pull_orders_info(key = context.user_data['find_key'])
    with open('app/data/pull.log','r') as f: messages = ''.join(f.readlines())
    messages = messages.split('\n\n')
    # if context.user_data['find_key']: messages = (message for message in messages if context.user_data['find_key'] in message.split('\n')[0])

    for context.user_data['message'] in messages:
        if context.user_data['message']:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=context.user_data['message'],
                parse_mode=data['parse_mode']
            )

@wr.personal
@wr.owner
@log_wrapper
async def log_file(update:Update, context:ContextTypes.DEFAULT_TYPE,data:dict) -> None:
    '''Usage: /log_file [key] --- Get latest/[key] log file '''

    context.user_data['file_key'] = ""
    if context.args: context.user_data['file_key'] = context.args[0]
    context.user_data['document'] = f"app/logs/run{context.user_data['file_key']}.log"

    with open(context.user_data['document'],'r') as f: ...          # Purposely raise FileNotFoundError for better handling

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=context.user_data['document']
    )

@log_wrapper
async def pull_loot(update: Update, context:ContextTypes.DEFAULT_TYPE, *args, **kwargs):
    ''' Usage: /pull_loot --- pull menu display '''
    await update.message.reply_text(
                            text=await pull_menu_message(),
                            reply_markup=await pull_menu_keyboard()
    )

# ------------------------------------------------------------------------------------------------------------
# Menu callback functions

async def pull_menu_message():
    return 'Select the type of loot you want to check'

async def pull_menu_keyboard():
    keyboard = [[InlineKeyboardButton('inGameLoot', callback_data='iGL')],
            [InlineKeyboardButton('Games', callback_data='G')]]
    return InlineKeyboardMarkup(keyboard)

# Callback Handlers
@log_wrapper
async def pull_loot_menu_iGL(): ...
