import asyncio
from pyrogram.enums import ChatType
import config
from AlexaMusic import app
from AlexaMusic.core.call import Alexa, autoend
from datetime import datetime, timedelta
from AlexaMusic.utils.database import get_client, is_active_chat, is_autoend


async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        while not await asyncio.sleep(config.AUTO_LEAVE_ASSISTANT_TIME):
            from AlexaMusic.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                try:
                    async for i in client.get_dialogs():
                        chat_type = i.chat.type
                        if chat_type in [
                            ChatType.SUPERGROUP,
                            ChatType.GROUP,
                            ChatType.CHANNEL,
                        ]:
                            chat_id = i.chat.id
                            if (
                                chat_id != config.LOG_GROUP_ID
                                and chat_id != -1001686672798
                            ):
                                if not await is_active_chat(chat_id):
                                    try:
                                        await client.leave_chat(chat_id)
                                    except:
                                        continue
                except:
                    pass


asyncio.create_task(auto_leave())
