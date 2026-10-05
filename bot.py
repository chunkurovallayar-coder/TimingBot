import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from datetime import datetime
import pytz
from config import ACCOUNTS


async def update_name(account):
    api_id = account["api_id"]
    api_hash = account["api_hash"]
    name = account["original_first_name"]
    fmt = account["format"]
    tz = pytz.timezone(account["timezone"])
    session = account["session"]

    async with TelegramClient(
    StringSession(session),
    api_id,
    api_hash
) as client:

        while True:
            now = datetime.now(tz).strftime(fmt)
            new_name = f"{name}{now}"

            await client.edit_profile(first_name=new_name)

            # Ждём до следующей минуты
            await asyncio.sleep(60)


async def main():
    tasks = [
        update_name(acc)
        for acc in ACCOUNTS
        if acc["enabled"]
    ]

    await asyncio.gather(*tasks)


asyncio.run(main())
