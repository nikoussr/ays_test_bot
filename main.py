import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import registration_handler, start_handler, users_handler, admin_handlers
from configs import TOKEN
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from app.database.bd import Database

db = Database('../data/ays_test_database.db')

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


"""  user_id = message.from_user.id
dobs = db.get_date_of_birth_cafe(db.get_cafe_id(user_id))
now = datetime.datetime.today().date()
year = datetime.datetime.today().year
for first_name, last_name, dob in dobs:
    if dob != '-':
        dob = list(str(dob).split('.'))
        dob = datetime.date(year, int(dob[1]), int(dob[0]))
        print(dob)
        days = (dob - now).days
        print(days)
        if 0 < days <= 82:
            await message.answer(f"У сотрудника {last_name} {first_name} скоро день рождения! {dob}")"""