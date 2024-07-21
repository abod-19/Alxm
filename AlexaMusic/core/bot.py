import sys

from pyrogram import Client
import config
from ..logging import LOGGER
from pyrogram.enums import ChatMemberStatus


class AlexaBot(Client):
    def __init__(self):
        super().__init__(
            "MusicBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
        )
        LOGGER(__name__).info(f"🥤| يتم تـشغيل الـبوت ...")

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.mention = get_me.mention
        try:
            await self.send_message(
                config.LOG_GROUP_ID, "**🥤| تـم تـشغيل الـبوت بـنجاح، في انـتظار الحساب الـمساعد...**"
            )
        except:
            LOGGER(__name__).error(
                "🥤|  قـم بـرفع الـبوت مشرف في الجروب او القناه."
            )
            sys.exit()
        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error("🥤| قـم بـرفع الـبوت مشرف في الجروب.")
            sys.exit()
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"🥤| تـم تـشغيل {self.name} بـنجاح.")
