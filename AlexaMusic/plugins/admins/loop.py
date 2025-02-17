from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from AlexaMusic import app
from AlexaMusic.utils.database.memorydatabase import get_loop, set_loop
from AlexaMusic.utils.decorators import AdminRightsCheck


@app.on_message(filters.command(["loop", "cloop", "تكرار", "التكرار"],"") & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def admins(cli, message: Message, _, chat_id):
    usage = _["admin_24"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    user_mention = message.from_user.mention if message.from_user else "المشـرف"
    if state.isnumeric():
        state = int(state)
        if 1 <= state <= 10:
            got = await get_loop(chat_id)
            if got != 0:
                state = got + state
            if int(state) > 10:
                state = 10
            await set_loop(chat_id, state)
            return await message.reply_text(
                _["admin_25"].format(message.from_user.first_name, state)
            )
        else:
            return await message.reply_text(_["admin_26"])
    elif state.lower() == "enable" or state == "تفعيل":
        await set_loop(chat_id, 10)
        return await message.reply_text(
            _["admin_25"].format(message.from_user.first_name, state)
        )
    elif state.lower() == "disable" or state == "تعطيل":
        await set_loop(chat_id, 0)
        return await message.reply_text(_["admin_27"])
    else:
        return await message.reply_text(usage)
