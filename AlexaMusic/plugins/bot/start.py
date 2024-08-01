import asyncio, redis, requests, datetime, random

from pyrogram import filters
from pyrogram import enums, filters
from youtubesearchpython.__future__ import VideosSearch

import config
from config import BANNED_USERS
from config.config import OWNER_ID
from strings import get_command, get_string
from AlexaMusic import Telegram, YouTube, app
from AlexaMusic.misc import SUDOERS
from AlexaMusic.plugins.play.playlist import del_plist_msg
from AlexaMusic.plugins.sudo.sudoers import sudoers_list
from AlexaMusic.plugins.Managed.Deev import devid
from AlexaMusic.utils.database import (
    add_served_chat,
    is_served_user,
    add_served_user,
    blacklisted_chats,
    get_assistant,
    get_lang,
    get_userss,
    is_on_off,
    is_served_private_chat,
)
from AlexaMusic.utils.decorators.language import LanguageStart
from AlexaMusic.utils.inline import help_pannel, private_panel, start_pannel
from AlexaMusic.utils.command import commandpro
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InputMediaPhoto,
    Message,
)

loop = asyncio.get_running_loop()


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_comm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_photo(
                       photo=config.START_IMG_URL,
                       caption=_["help_1"], reply_markup=keyboard)
        if name[0:4] == "song":
            return await message.reply_text(_["song_2"])
        if name[0:3] == "sta":
            m = await message.reply_text(
                "جلب الإحصائيات الشخصية الخاصة بك من {app.name} ."
            )
            stats = await get_userss(message.from_user.id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    top_list = stats[i]["spot"]
                    results[str(i)] = top_list
                    list_arranged = dict(
                        sorted(
                            results.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                    )
                if not results:
                    return m.edit(_["ustats_1"])
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += f"🔗[ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ](https://t.me/jsbcjdbfn) ** ᴩʟᴀʏᴇᴅ {count} ᴛɪᴍᴇs**\n\n"
                    else:
                        msg += f"🔗 [{title}](https://www.youtube.com/watch?v={vidid}) ** played {count} times**\n\n"
                msg = _["ustats_2"].format(tot, tota, limit) + msg
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(None, get_stats)
            except Exception as e:
                print(e)
                return
            thumbnail = await YouTube.thumbnail(videoid, True)
            await m.delete()
            await message.reply_photo(photo=thumbnail, caption=msg)
            return
        if name[0:3] == "dev":
            await devid(client=client, message=message)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                usrnam = message.from_user.username
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"⟡ تم تشغيل البوت للتحقق من **المطورين\n\n**⟡ 𝐈𝐃 :** {sender_id}\n**⟡ 𝐍𝐀𝐌𝐄 :** {message.from_user.mention}\n**⟡ 𝐔𝐒𝐄𝐑 :** @{usrnam}",
                )
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                return await Telegram.send_split_text(message, lyrics)
            else:
                return await message.reply_text("فشل الحصول على كلمات الاغنيه.")
        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
📌**العنوان :** {title}

⏳**المدة :** {duration} ᴍɪɴᴜᴛᴇs
👀**المشاهدات :** `{views}`
🎥**القناة :** [{channel}]({channellink})
🔗**الرابط:** [{title}]({link})
⏰**بواسطة :** {published}

💖 **{app.name}**"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ʏᴏᴜᴛᴜʙᴇ •", url=f"{link}"),
                        InlineKeyboardButton(text="• ᴄʟᴏsᴇ •", callback_data="close"),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=key,
            )
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <code>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</code>\n\n**ᴜsᴇʀ ɪᴅ:** {sender_id}\n**ᴜsᴇʀɴᴀᴍᴇ:** {sender_name}",
                )
    else:
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        out = private_panel(_, app.username, OWNER)
        if config.START_IMG_URL:
            try:
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_2"].format(config.MUSIC_BOT_NAME),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            except:
                await message.reply_text(
                    _["start_2"].format(config.MUSIC_BOT_NAME),
                    reply_markup=InlineKeyboardMarkup(out),
                )
        else:
            await message.reply_text(
                _["start_2"].format(config.MUSIC_BOT_NAME),
                reply_markup=InlineKeyboardMarkup(out),
            )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"{message.from_user.mention} تم تشغيل البوت.\n\n**ᴜsᴇʀ ɪᴅ:** {sender_id}\n**ᴜsᴇʀɴᴀᴍᴇ:** {sender_name}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def testbot(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )

welcome_group = 2


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                "**ᴩʀɪᴠᴀᴛᴇ ᴍᴜsɪᴄ ʙᴏᴛ**\n\nᴏɴʟʏ ғᴏʀ ᴛʜᴇ ᴄʜᴀᴛs ᴀᴜᴛʜᴏʀɪsᴇᴅ ʙʏ ᴍʏ ᴏᴡɴᴇʀ, ʀᴇǫᴜᴇsᴛ ɪɴ ᴍʏ ᴏᴡɴᴇʀ's ᴩᴍ ᴛᴏ ᴀᴜᴛʜᴏʀɪsᴇ ʏᴏᴜʀ ᴄʜᴀᴛ ᴀɴᴅ ɪғ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴡᴀɴᴛ ᴛᴏ ᴅᴏ sᴏ ᴛʜᴇɴ ғᴜ*ᴋ ᴏғғ ʙᴇᴄᴀᴜsᴇ ɪ'ᴍ ʟᴇᴀᴠɪɴɢ."
            )
            return await app.leave_chat(message.chat.id)
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.id == app.id:
                chat_type = message.chat.type
                #if chat_type != enums.ChatType.SUPERGROUP:
                    #await message.reply_text(_["start_6"])
                    #return await app.leave_chat(message.chat.id)
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_7"].format(
                            f"https://t.me/{app.username}?start=dev"
                        )
                    )
                    return await app.leave_chat(chat_id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(_)
                await message.reply_text(
                    _["start_3"].format(
                        config.MUSIC_BOT_NAME,
                        userbot.username,
                        userbot.id,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    _["start_4"].format(config.MUSIC_BOT_NAME, member.mention)
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_5"].format(config.MUSIC_BOT_NAME, member.mention)
                )
            return
        except:
            return
