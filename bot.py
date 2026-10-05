import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from config import ACCOUNTS

async def update_name(account):
    session_str = account["session"]
    api_id = account["api_id"]
    api_hash = account["api_hash"]
    original_name = account["original_first_name"]
    time_format = account["format"]
    tz = pytz.timezone(account["timezone"])
    
    # Инициализация строго через StringSession БЕЗ файлов базы данных
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    
    print(f"[{account['name']}] Подключение к Telegram...")
    try:
        await client.start()
        print(f"[{account['name']}] Авторизация успешна!")
        
        while True:
            current_time = datetime.now(tz).strftime(time_format)
            new_first_name = f"{original_name}{current_time}"
            
            await client(UpdateProfileRequest(first_name=new_first_name))
            print(f"[{account['name']}] Имя изменено на: {new_first_name}")
            
            await asyncio.sleep(60)
            
    except Exception as e:
        print(f"[{account['name']}] Критическая ошибка: {e}")
    finally:
        await client.disconnect()
        print(f"[{account['name']}] Клиент отключен.")

async def main():
    tasks = []
    for account in ACCOUNTS:
        if account.get("enabled", True):
            tasks.append(update_name(account))
            
    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("В config.py нет активных аккаунтов.")

if __name__ == "__main__":
    asyncio.run(main())
