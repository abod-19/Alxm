import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from AlexaMusic import app
from config import OWNER_ID
import config

lnk = "https://t.me/EF_19"

@app.on_message(filters.regex(r"^(المطور|مطور|dev)$"))
async def devid(client: Client, message: Message):
    first_owner_id = OWNER_ID[0]
    usr = await client.get_users(first_owner_id)
    #usr = await client.get_users(OWNER_ID)
    name = usr.first_name
    usrnam = usr.username
    photo_path = os.path.join("downloads", "developer.jpg")
    await app.download_media(usr.photo.big_file_id, file_name=photo_path)
    await message.reply_photo(
        photo=photo_path,
        caption=f"""**⌯ 𝙳𝚎𝚟 :** {name}\n\n**⌯ 𝚄𝚂𝙴𝚁 :** @{usrnam}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(name, url=f"tg://user?id={OWNER_ID}"),
                ],
                [
                    InlineKeyboardButton(
                        text="السورس", url=lnk),
                ],
            ]
        ),
    )
        
