from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from strings import get_command
from AlexaMusic import app
from AlexaMusic.core.call import Alexa
from AlexaMusic.utils.database import set_loop
from AlexaMusic.utils.decorators import AdminRightsCheck
from strings.filters import command
from strings import get_string
#import config

#Nem = config.BOT_NAME + " اسكت"
#Men = config.BOT_NAME + " ايقاف"
@app.on_message(
    filters.command(["end", "stop", "cend", "cstop"]) & filters.group & ~BANNED_USERS
)
@app.on_message(
    command(["اسكت","ايقاف"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    await Alexa.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    user_mention = message.from_user.mention if message.from_user else "المشـرف"
    await message.reply_text(
        _["admin_9"].format(message.from_user.mention), disable_web_page_preview=True
    )
