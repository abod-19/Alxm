# This code is written by (C) TheTeamAlexa bot will send message to log group when someone add
# this bot to new group make sure to star all projects
# Copyright (C) 2021-2024 by Alexa_Help@ Github, < TheTeamAlexa >.
# A Powerful Music Bot Property Of Rocks Indian Largest Chatting Group
# All rights reserved. © Alisha © Alexa © Yukki

from pyrogram import Client, filters
from pyrogram.types import Message
from AlexaMusic import app
from AlexaMusic.utils.database import get_served_chats
from config import LOG_GROUP_ID


async def lul_message(chat_id: int, message: str):
    await app.send_message(chat_id=chat_id, text=message)


@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    if (await client.get_me()).id in [user.id for user in message.new_chat_members]:
        added_by = message.from_user.first_name if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        matlabi_jhanto = message.chat.title
        served_chats = len(await get_served_chats())
        chat_id = message.chat.id
        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "ᴩʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
        lemda_text = f"🌹 تمت اضافه البوت الى مجموعه جديدة .\n\n┏━━━━━━━━━━━━━━━━━┓\n┣★ <b>𝙲𝙷𝙰𝚃</b> › : {matlabi_jhanto}\n┣★ <b>𝙲𝙷𝙰𝚃 𝙸𝙳</b> › : {chat_id}\n┣★ <b>𝙲𝙷𝙰𝚃 𝚄𝙽𝙰𝙼𝙴</b> › : {chatusername}\n┣★ <b>𝙲𝙾𝚄𝙽𝚃</b> › : {cont}\n┣★ <b>𝚃𝙾𝚃𝙰𝙻 𝙲𝙷𝙰𝚃</b> › : {served_chats}\n┣★ <b>𝙰𝙳𝙳𝙴𝙳 𝙱𝚈</b> › :\n┗━━━ꪜ {added_by}"
        await lul_message(LOG_GROUP_ID, lemda_text)
