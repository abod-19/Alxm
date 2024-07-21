import asyncio

from pyrogram.types import InlineKeyboardMarkup

from strings import get_string
from AlexaMusic.misc import db
from AlexaMusic.utils.database import (get_active_chats, get_lang,
                                       is_music_playing)
from AlexaMusic.utils.formatters import seconds_to_min
from AlexaMusic.utils.inline import (stream_markup_timer)

from ..admins.callback import wrong

checker = {}


async def timer():
    while not await asyncio.sleep(1):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            if not await is_music_playing(chat_id):
                continue
            playing = db.get(chat_id)
            if not playing:
                continue
            file_path = playing[0]["file"]
            if "index_" in file_path or "live_" in file_path:
                continue
            duration = int(playing[0]["seconds"])
            if duration == 0:
                continue
            db[chat_id][0]["played"] += 1


asyncio.create_task(timer())


