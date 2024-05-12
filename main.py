import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import registration_handler, start_handler, admin_handlers,users_handler
from configs import TOKEN
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from app.database.bd import Database

db = Database('ays_test_database.db')

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot)


async def main():
    await  bot.delete_webhook()
    dp.include_router(registration_handler.router)
    dp.include_router(start_handler.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(users_handler.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
