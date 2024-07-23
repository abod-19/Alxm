import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from AlexaMusic import LOGGER, app, userbot
from AlexaMusic.core.call import Alexa
from AlexaMusic.plugins import ALL_MODULES
from AlexaMusic.utils.database import get_banned_users, get_gbanned

loop = asyncio.get_event_loop_policy().get_event_loop()


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("AlexaMusic").error("اضف جلسه الحساب المساعد ثم حاول مره اخرى...")
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("AlexaMusic.plugins" + all_module)
    LOGGER("AlexaMusic.plugins").info("تم تحديث معلومات السورس بنجاح.")
    await userbot.start()
    await Alexa.start()
    try:
        await Alexa.stream_call("https://telegra.ph/file/b60b80ccb06f7a48f68b5.mp4")
    except NoActiveGroupCall:
        LOGGER("AlexaMusic").error(
            "[ERROR] - \n\nقم بفتح المكالمه ولا تقم بايقافها والا سيتوقف البوت عن العمل."
        )
        sys.exit()
    except:
        pass
    await Alexa.decorators()
    LOGGER("AlexaMusic").info("تم التنصيب على سورس الملك بنجاح\nقناة السورس https://t.me/EF_19")
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("AlexaMusic").info("Stopping Music Bot")
