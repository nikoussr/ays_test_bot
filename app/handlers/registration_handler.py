from aiogram.types import Message, CallbackQuery
from aiogram import Router
import app.keyboards as kb
from states.states import register, user, admin
from aiogram.fsm.context import FSMContext
from app.database.bd import Database
from configs import JOBS, CAFES, ADMIN

router = Router()
mas = []

db = Database('../data/ays_test_database.db')


@router.callback_query(lambda q: q.data == 'register')
async def reg(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=None)
    user_id = callback.from_user.id
    if db.user_exists(user_id):
        await callback.message.answer(f"Вы уже зарегистрированы")
    else:
        await state.set_state(register.wait_first_name)
        db.add_user(callback.from_user.id)
        await callback.message.answer(f'Введите имя')


@router.message(register.wait_first_name)
async def first(message: Message, state: FSMContext):
    if message.text != "/start":
        await state.update_data(wait_first_name=message.text)
        await state.set_state(register.wait_last_name)
        data = await state.get_data()
        db.set_first_name(message.from_user.id, data["wait_first_name"])
        await message.answer(f'Введите фамилию')


@router.message(register.wait_last_name)
async def second(message: Message, state: FSMContext):
    if message.text != "/start":
        await state.update_data(wait_last_name=message.text)
        data = await state.get_data()
        db.set_last_name(message.from_user.id, data["wait_last_name"])
        await message.answer(f'Введите номер телефрна в формате "89..."')
        await state.set_state(register.wait_phone_number)


@router.message(register.wait_phone_number)
async def third(message: Message, state: FSMContext):
    if message.text != "/start":
        await state.update_data(wait_phone_number=message.text)
        data = await state.get_data()
        db.set_phone_number(message.from_user.id, data["wait_phone_number"])
        await message.answer(f"Когда вы родились?\nФормат ввода - 01.02.2003")
        await state.set_state(register.wait_date_of_birth)


@router.message(register.wait_date_of_birth)
async def third(message: Message, state: FSMContext):
    if message.text != "/start":
        await state.update_data(wait_for_date_of_birth=message.text)
        data = await state.get_data()
        db.set_date_of_birth(message.from_user.id, data["wait_for_date_of_birth"])
        await message.answer(f"Где вы работаете?", reply_markup=kb.create_cafe_id_btns_register())
        await state.set_state(register.wait_cafe_id)


@router.callback_query(
    lambda q: q.data in CAFES,
    register.wait_cafe_id)
async def cafes(callback: CallbackQuery, state: FSMContext):
    if callback.message.text != "/start":
        db.set_cafe_id(callback.from_user.id, callback.data[0])
        await callback.message.edit_text("Место работы выбрано", reply_markup=None)
        await callback.message.answer(f"Кем вы работаете?", reply_markup=kb.create_job_id_btns_register(callback.data[0]))
        await state.set_state(register.wait_job_id)


@router.callback_query(register.wait_job_id)
async def jobs(callback: CallbackQuery, state: FSMContext):
    db.set_job_id(callback.from_user.id, callback.data[0])
    await callback.message.edit_text("Должность выбрана", reply_markup=None)
    user_info = db.get_all_info(callback.from_user.id)[0]
    await callback.message.answer(
        f"Вас зовут - {user_info[0]} {user_info[1]}\nномер телефона - {user_info[2]}\nдата раждения - {user_info[3]}\nдолжность - {user_info[4]}\nместо работы - {user_info[5]}\nВсё верно?",
        reply_markup=kb.y_n_btns)
    await state.set_state(register.wait_yes_no)


@router.callback_query(lambda q: q.data == 'yes', register.wait_yes_no)
async def yes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f'Регистрация прошла успешно', reply_markup=None)
    user_id = str(callback.from_user.id)
    print(f"Зарегестрировался {user_id}")
    if user_id not in ADMIN:
        await callback.message.answer(
            f"Добро пожаловать в юзер-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.user_manager_btns if db.get_job_id(user_id) == 1 else kb.user_btns)
        await state.set_state(user.wait_user)
    else:
        await callback.message.answer(
            f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.admin_btns)
        await state.set_state(admin.wait_admin)


@router.callback_query(lambda q: q.data == 'no', register.wait_yes_no)
async def no(callback: CallbackQuery, state: FSMContext):
    await state.set_state(register.wait_first_name)
    await callback.message.edit_text('Повторная регистрация...', reply_markup=None)
    await callback.message.answer(f'Введите имя')
