import btelegram.build as build

from inspect import getmembers, isfunction
import btelegram.functions as funcs

def run_bot():
    functions = dict(getmembers(funcs,isfunction))
    build.bot(functions).run_polling()

run_bot()