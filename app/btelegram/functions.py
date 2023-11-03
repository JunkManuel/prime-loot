from telegram import Update
from telegram.ext import ContextTypes

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

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' welcome mesage '''
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='_Welcome to the internet \.\.\._',
        parse_mode=data['parse_mode']
    )

async def loot(update: Update, context:ContextTypes.DEFAULT_TYPE,data: dict) -> None:
    ''' loot things '''
    from experiment import run_async_primeloot
    run_async_primeloot('app/cookies.txt')

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Claimed shit on amazon'
    )