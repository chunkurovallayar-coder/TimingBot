import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest

# Импортируем настройки из вашего config.py
from config import ACCOUNTS 

async def update_name(account):
    session_str = account["session"]
    api_id = account["api_id"]
    api_hash = account["api_hash"]
    original_name = account["original_first_name"]
    time_format = account["format"]
    tz = pytz.timezone(account["timezone"])
    
    # Подключаемся БЕЗ файлов, строго используя StringSession
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    
    print(f"[{account['name']}] Подключение к Telegram...")
    await client.start()
    print(f"[{account['name']}] Авторизация успешна!")
    
    try:
        while True:
            # Форматируем время и обновляем имя
            current_time = datetime.now(tz).strftime(time_format)
            new_first_name = f"{original_name}{current_time}"
            
            await client(UpdateProfileRequest(first_name=new_first_name))
            print(f"[{account['name']}] Имя изменено на: {new_first_name}")
            
            # Ждем 60 секунд до следующего обновления
            await asyncio.sleep(60)
    except Exception as e:
        print(f"[{account['name']}] Ошибка в цикле: {e}")
    finally:
        await client.disconnect()

async def main():
    tasks = []
    for account in ACCOUNTS:
        if account.get("enabled", True):
            tasks.append(update_name(account))
            
    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("Нет активных аккаунтов в config.py")

if __name__ == "__main__":
    asyncio.run(main())
