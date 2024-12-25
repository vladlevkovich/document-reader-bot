from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import start_handler, document_handler
import asyncio
import logging
import os

load_dotenv()

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(os.getenv('TOKEN_BOT'))
    dp = Dispatcher()
    dp.include_router(start_handler.router)
    dp.include_router(document_handler.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
