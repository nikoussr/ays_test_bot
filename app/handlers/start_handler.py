from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F, Router
import app.keyboards as kb
from states.test import admin, user
from aiogram.fsm.context import FSMContext
from app.database.bd import Database
from configs import ADMIN
from aiogram.exceptions import  TelegramBadRequest


router = Router()
db = Database('../data/ays_test_database.db')


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        from main import bot
        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=message.message_id,
                                            reply_markup=None)
    except TelegramBadRequest:
        pass
    if str(user_id) not in str(db.get_banned_users()):
        if (str(user_id) in (ADMIN) and db.user_exists(user_id)):
            await message.answer(
                f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
                reply_markup=kb.admin_btns)
            await state.set_state(admin.wait_admin)
            print('START')
        elif (str(user_id) in (ADMIN) and not db.user_exists(user_id)):
            await message.answer(
                f"Добро пожаловать в админ-панель, {message.from_user.first_name}!\nВам нужно пройти регистрацию", reply_markup=kb.reg_btns)

        elif (not (db.user_exists(message.from_user.id))):
            await message.answer("Привет друг!\nЧтобы начать пользоваться этим ботом, нужно пройти регистрацию", reply_markup=kb.reg_btns)
        else:
            await message.answer(
                f"Добро пожаловать в юзер-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
                reply_markup=kb.user_manager_btns if db.get_job_id(message.from_user.id) == 1 else kb.user_btns)
            await state.set_state(user.wait_user)
            print("Вошел в юзер-панель")
    else:
        await message.answer(f"Вы заблокированы. Пока!")

