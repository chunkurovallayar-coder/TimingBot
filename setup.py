from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import asyncio

API_ID = 2040
API_HASH = 'b18441a1ff607e10a989891a5462e627'

async def main():
    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        print(client.session.save())

await main()
