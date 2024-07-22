from pyrogram import filters
from pyrogram.types import Message

from strings import get_command
from AlexaMusic import app
from AlexaMusic.misc import SUDOERS
from AlexaMusic.utils.database.memorydatabase import (
    get_active_chats,
    get_active_video_chats,
)

# Commands
ACTIVEVC_COMMAND = get_command("ACTIVEVC_COMMAND")
ACTIVEVIDEO_COMMAND = get_command("ACTIVEVIDEO_COMMAND")


@app.on_message(filters.command(["activevc", "activevoice", "المكالمات"]) & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text("⟡ جاري البحث عن مكالمات ...")
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "دردشه خاصه"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await mystic.edit_text("⟡ لاتوجد مكالمات حالياً.")
    else:
        await mystic.edit_text(
            f"**⟡ المكالمات النشطة حاليا :**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["activev", "activevideo", "الفيديوهات"]) & SUDOERS)
async def activevi_(_, message: Message):
    mystic = await message.reply_text("⟡ جاري البحث عن فيديوهات متوفرة ...")
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "دردشه خاصه"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await mystic.edit_text("⟡ لاتوجد فيديوهات حالياً.")
    else:
        await mystic.edit_text(
            f"**⟡ الفيديوهات النشطة حاليا :**\n\n{text}",
            disable_web_page_preview=True,
        )
