import random

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from AlexaMusic import app
from AlexaMusic.misc import db
from AlexaMusic.utils.decorators import AdminRightsCheck


@app.on_message(filters.command(["shuffle", "cshuffle", "خلط"],"") & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def admins(Client, message: Message, _, chat_id):
    check = db.get(chat_id)
    if not check:
        return await message.reply_text(_["admin_21"])
    try:
        popped = check.pop(0)
    except:
        return await message.reply_text(_["admin_22"])
    check = db.get(chat_id)
    if not check:
        check.insert(0, popped)
        return await message.reply_text(_["admin_22"])
    random.shuffle(check)
    check.insert(0, popped)
    await message.reply_text(_["admin_23"].format(message.from_user.first_name))
