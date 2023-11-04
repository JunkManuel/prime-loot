from os import environ as env
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
import logging

log = logging.getLogger('tgram_bot.permission_wraps.py')
log.setLevel(logging.INFO)

owner_id = int(env['TGRAM_OWNER_ID'])
if 'TGRAM_ADMINS_IDS' in env:
    admin_ids = env['TGRAM_ADMINS_IDS'].strip('[ ]').split(',')
    admin_ids = [owner_id] + [int(admin) for admin in admin_ids]
else: admin_ids = [owner_id]

def owner(func):
    @wraps(func)
    async def wrapped(update:Update, context:ContextTypes.DEFAULT_TYPE, *args,**kwargs):
        user_id = update.effective_user.id
        user_name = update.effective_user.username
        if user_id != owner_id:
            log.warning(f"Access denied to {user_name}:{user_id}")
            return

        log.info(f"{user_name}:{user_id} executing {func.__name__}")
        return await func(update,context,*args,**kwargs)
    return wrapped

def admin(func):
    @wraps(func)
    async def wrapped(update:Update, context:ContextTypes.DEFAULT_TYPE, *args,**kwargs):
        user_id = update.effective_user.id
        user_name = update.effective_user.username
        if user_id not in admin_ids:
            log.warning(f"Access denied to {user_name}:{user_id}")
            return

        log.info(f"{user_name}:{user_id} issued ...")
        return await func(update,context,*args,**kwargs)
    return wrapped

def unrestricted(func):
    @wraps(func)
    async def wrapped(update:Update, context:ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        log.warning(f"{func.__name__} is available for all users")
        user_id = update.effective_user.id
        user_name = update.effective_user.username

        log.info(f"{user_name}:{user_id} executing {func.__name__}")
        return await func(update,context,*args,**kwargs)
    return wrapped

