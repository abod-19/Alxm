from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from AlexaMusic import app
from AlexaMusic.core.call import Alexa
from AlexaMusic.utils.database import is_muted, mute_off
from AlexaMusic.utils.decorators import AdminRightsCheck


@app.on_message(
 filters.command(["unmute", "cunmute", "اتكلم", "/unmute", "/cunmute"],"") & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def unmute_admin(Client, message: Message, _, chat_id):
    if not await is_muted(chat_id):
        return await message.reply_text(_["admin_7"], disable_web_page_preview=True)
    await mute_off(chat_id)
    await Alexa.unmute_stream(chat_id)
    await message.reply_text(
        _["admin_8"].format(message.from_user.mention), disable_web_page_preview=True
    )
