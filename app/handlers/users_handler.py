from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Router
import app.keyboards as kb
from states.test import  user
from aiogram.fsm.context import FSMContext
from app.database.bd import Database

router = Router()
mas = []

db = Database('../data/ays_test_database.db')


@router.callback_query(user.wait_user)
async def user_panel(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'open_user_kd':
        cafe_id = db.get_cafe_id(callback.from_user.id)
        job_id = db.get_job_id(callback.from_user.id)
        all_folders = db.get_folders(cafe_id, job_id)
        folders = kb.create_folders_btn_look(all_folders=all_folders)
        await callback.message.edit_text(f"Выберите папку", reply_markup=folders)
        await state.update_data(wait_user=(cafe_id, job_id))
        await state.set_state(user.wait_for_click_folder)
    elif callback.data == "find_user_kd":
        cafe_id = db.get_cafe_id(callback.from_user.id)
        job_id = db.get_job_id(callback.from_user.id)
        await callback.message.answer(f"Поиск БЗ по ключевому слову\nВведите слово или предложение")
        await state.update_data(find_user_kd=(cafe_id, job_id))
        await state.set_state(user.wait_for_find_kd)


    elif callback.data == "order":
        await callback.message.answer(f"Выберите действие", reply_markup=kb.manager_order_btns)
        await state.set_state(user.wait_for_order)
    elif callback.data == 'kick_me':
        await callback.message.answer("Здравствуйте! Если у вас есть какие-либо вопросы, предложения или Вы нашли баги, пожалуйста, напишите мне.\nЯ всегда готов помочь и выслушать Ваше мнение. Спасибо!")
        await state.set_state(user.wait_for_user_message)


"""Закуп"""


@router.callback_query(user.wait_for_order)
async def wait_for_order(callback: CallbackQuery, state: FSMContext):
    if callback.data == "make_new_good":
        pass
    else:
        from main import bot
        await bot.edit_message_text(f"Закупка..", chat_id=callback.from_user.id, message_id=callback.message.message_id)
        cafe_id = db.get_cafe_id(callback.from_user.id)
        art = db.get_all_goods_art(cafe_id)
        short_name = db.get_all_goods_short_name(cafe_id)
        keyboard = kb.create_goods_btns(short_name, art, cafe_id)
        await callback.message.answer(f"Выберите позицию", reply_markup=keyboard)  # клава с товарами
        await state.update_data(wait_for_order=(art, short_name, cafe_id, 1))
        await state.set_state(user.wait_for_create_order)


@router.callback_query(user.wait_for_create_order)
async def wait_for_create_orr(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cafe_id = data["wait_for_order"][2]
    short_name = data["wait_for_order"][1]
    art = data["wait_for_order"][0]
    if callback.data == "next_page":
        page = data["wait_for_order"][3] + 1
        keyboard = kb.update_goods_btns(short_name, art, cafe_id, page)
        from main import bot
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            reply_markup=keyboard)
        await state.update_data(wait_for_order=(art, short_name, cafe_id, page))
        await state.set_state(user.wait_for_create_order)
    if callback.data == "prev_page":
        page = data["wait_for_order"][3] - 1
        keyboard = kb.update_goods_btns(short_name, art, cafe_id, page)
        from main import bot
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            reply_markup=keyboard)
        await state.update_data(wait_for_order=(art, short_name, cafe_id, page))
        await state.set_state(user.wait_for_create_order)
    elif callback.data not in ["⛔", "prev_page", "next_page", "ready"]:
        from main import bot
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        c_data = callback.data
        await state.update_data(wait_for_create_order=(c_data[0], c_data[1:]))
        await callback.message.answer(f"Сколько штук?")
        await state.set_state(user.wait_for_good_count)
    elif callback.data == "ready":
        data = await state.get_data()
        info = data["wait_for_good_count"]
        data_str = '\n'.join([sublist[0] + ', арт. ' + sublist[1] + ', ' + sublist[2] + ' ед.' for sublist in info])
        print(data_str)
        await callback.message.answer(data_str)

@router.message(user.wait_for_good_count)
async def wait_for_create_orde(message: Message, state: FSMContext):
    count = message.text
    data = await state.get_data()
    cafe_id, art = data["wait_for_create_order"][0], data["wait_for_create_order"][1]
    full_name = db.get_good_full_name(art, cafe_id)
    unit = db.get_good_unit(art, cafe_id)
    try:
        spisok = data["wait_for_good_count"]
        spisok.append([full_name, art, count, unit])
        print(spisok)
        await state.update_data(wait_for_good_count=spisok)
    except:
        spisok = []
        spisok.append([full_name, art, count, unit])
        print(spisok)
        await state.update_data(wait_for_good_count=spisok)

    cafe_id = db.get_cafe_id(message.from_user.id)
    art = db.get_all_goods_art(cafe_id)
    short_name = db.get_all_goods_short_name(cafe_id)
    keyboard = kb.create_goods_btns(short_name, art, cafe_id)
    await message.answer(f"Выберите позицию", reply_markup=keyboard)  # клава с товарами
    await state.update_data(wait_for_order=(art, short_name, cafe_id, 1))
    await state.set_state(user.wait_for_create_order)

@router.message(user.wait_for_user_message)
async def send(message: Message, state: FSMContext):
    await message.answer(f"Cообщение доставлено", reply_markup=kb.exit_btns)
    from main import bot
    await bot.send_message(695088267, f"Сообщение от {message.from_user.full_name}:\n{message.text}")
    await state.set_state(user.wait_for_exit)


@router.callback_query(lambda q: q.data, user.wait_for_click_folder)
async def text_of_chapter(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    folder_id = data[0]
    folder_name = data[1]
    data = await state.get_data()
    cafe_id = data["wait_user"][0]
    job_id = data["wait_user"][1]
    kd_btns = kb.make_kd_kb1(job_id, cafe_id, folder_id)
    await callback.message.edit_text(f"Вот все БЗ в папке {folder_name}", reply_markup=kd_btns)
    await state.set_state(user.wait_for_click_kd)


@router.callback_query(lambda q: q.data, user.wait_for_click_kd)
async def text_of_chapter(callback: CallbackQuery, state: FSMContext):
    global text
    data = callback.data.split('_')
    base_id = data[0]
    group_elements = []  # создаем массив групповых элементов (видева, фотоб аудио...)
    photos = db.get_kd_photos(base_id)
    if photos is not None:
        for photo in photos:  # если есть хоть одно фото, то
            element = photo[0]
            input_media = InputMediaPhoto(media=element)
            group_elements.append(input_media)  # добавляем элементы
    if group_elements:
        await callback.message.answer_media_group(group_elements)  # вывод группы
    KD_text = db.get_kd_text(base_id)
    for x in range(0, len(KD_text), 4096):
        if len(KD_text) - x <= 4096:
            text = KD_text[x:x + 4096]
            break
        text = KD_text[x:x + 4096]
        await callback.message.answer(f"{text}")
    await callback.message.answer(f"{text}", reply_markup=kb.exit_btns)
    await state.set_state(user.wait_for_exit)


@router.message(user.wait_for_find_kd)
async def find_kd(message: Message, state: FSMContext):
    find_text = str(message.text)
    data = await state.get_data()
    cafe_id = data["find_user_kd"][0]
    job_id = data["find_user_kd"][1]
    all_kd = db.get_all_kd(job_id, cafe_id, 0)
    base_ids = []
    for kd in all_kd:
        text = str(db.get_kd_text(kd[1]))
        if (find_text in text) or (find_text.lower() in text) or (find_text.upper() in text) or (find_text[0].upper() in text):
            base_ids.append(kd[1])
    if base_ids:
        await message.answer(f"Выбирай", reply_markup= kb.make_kd_kb_base_ids(base_ids))
        await state.set_state(user.wait_for_click_kd)
    else:
        await message.answer(f"Ничего не найдено", reply_markup= kb.exit_btns)
        await state.set_state(user.wait_for_exit)

@router.callback_query(lambda q: q.data == 'exit', user.wait_for_exit)
async def user_data(callback: CallbackQuery, state: FSMContext):
    await state.set_state(user.wait_user)
    await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=None)
    # await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    user_id = callback.from_user.id
    await callback.message.answer(
        f"Добро пожаловать в юзер-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
        reply_markup=kb.user_btns)
