from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Router
import app.keyboards as kb
from states.test import user
from aiogram.fsm.context import FSMContext
from app.database.bd import Database

router = Router()
mas = []

db = Database('../data/ays_test_database.db')

"""Юзер-панель"""


@router.callback_query(user.wait_user)
async def user_panel(callback: CallbackQuery, state: FSMContext):
    # Поиск БЗ
    if callback.data == "find_user_kd":
        cafe_id = db.get_cafe_id(callback.from_user.id)
        job_id = db.get_job_id(callback.from_user.id)
        await callback.message.edit_text(f"Поиск БЗ.\nВведите слово или предложение", reply_markup=kb.exit_user_btns)
        await state.update_data(find_user_kd=(cafe_id, job_id))
        await state.set_state(user.wait_for_find_kd)
    # Список БЗ
    elif callback.data == 'open_user_kd':
        cafe_id = db.get_cafe_id(callback.from_user.id)
        job_id = db.get_job_id(callback.from_user.id)
        all_folders = db.get_folders(cafe_id, job_id)
        folders = kb.create_folders_btn_look(all_folders=all_folders)
        await callback.message.edit_text(f"Выберите папку", reply_markup=folders)
        await state.update_data(wait_user=(cafe_id, job_id))
        await state.set_state(user.wait_for_click_folder)
    # Закуп
    elif callback.data == "order":
        await callback.message.edit_text(f"Выберите действие", reply_markup=kb.manager_order_btns)
        await state.set_state(user.wait_for_action)
    # Написать разработчику
    elif callback.data == 'kick_me':
        await callback.message.edit_text(
            "Здравствуйте! Если у вас есть какие-либо вопросы, предложения или Вы нашли баги, пожалуйста, напишите мне.\nЯ всегда готов помочь и выслушать Ваше мнение. Спасибо!", reply_markup=kb.exit_user_btns)
        await state.set_state(user.wait_for_user_message)


"""Поиск БЗ"""


@router.message(user.wait_for_find_kd)
async def find_kd(message: Message, state: FSMContext):
    from main import bot
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
    find_text = str(message.text)
    data = await state.get_data()
    cafe_id = data["find_user_kd"][0]
    job_id = data["find_user_kd"][1]
    all_kd = db.get_all_kd(job_id, cafe_id, 0)
    base_ids = []
    for kd in all_kd:
        text = str(db.get_kd_text(kd[1])).lower()
        if (find_text.lower() in text):
            base_ids.append(kd[1])
    if base_ids:
        await message.answer(f"Выбирай", reply_markup=kb.make_kd_kb_base_ids(base_ids))
        await state.set_state(user.wait_for_click_kd)
    else:
        await message.answer(f"Ничего не найдено", reply_markup=kb.exit_user_btns)
        await state.set_state(user.wait_for_exit_del)


"""Список БЗ"""


@router.callback_query(lambda q: q.data, user.wait_for_click_folder)
async def folders(callback: CallbackQuery, state: FSMContext):
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
async def kd_in_folder(callback: CallbackQuery, state: FSMContext):
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
    await callback.message.answer(f"{text}", reply_markup=kb.exit_user_btns)
    await state.set_state(user.wait_for_exit)


"""Закуп"""


@router.callback_query(user.wait_for_action)
async def wait_for_action(callback: CallbackQuery, state: FSMContext):
    # Сделать закуп
    if callback.data == "create_order":
        from main import bot
        await bot.edit_message_text(f"Закупка..", chat_id=callback.from_user.id, message_id=callback.message.message_id)
        cafe_id = db.get_cafe_id(callback.from_user.id)
        art = db.get_all_goods_art(cafe_id)
        short_name = db.get_all_goods_short_name(cafe_id)
        keyboard = kb.create_goods_btns(short_name, art, cafe_id)
        await callback.message.answer(f"Выберите позицию", reply_markup=keyboard)  # клава с товарами
        await state.update_data(wait_for_order=(art, short_name, cafe_id, 1))
        await state.set_state(user.wait_for_create_order)
    # Добавить позицию
    elif callback.data == "make_new_good":
        from main import bot
        await bot.edit_message_text(
            f"Введите позицию в виде (через перенос строки):\nПолное название\nАртикул\nКороткое название\nМера измерения (шт, л, уп, ед...)\nЕсли нет артикула, то впишите туда короткое название",
            chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await state.set_state(user.wait_for_create_good)
    # Удалить позицию
    elif callback.data == "delete_good":
        from main import bot
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        cafe_id = db.get_cafe_id(callback.from_user.id)
        art = db.get_all_goods_art(cafe_id)
        short_name = db.get_all_goods_short_name(cafe_id)
        await state.update_data(delete_good=(art, short_name, cafe_id, 1))
        keyboard = kb.create_goods_btns(short_name, art, cafe_id)
        await callback.message.answer(f"Что удалить?", reply_markup=keyboard)  # клава с товарами
        await state.set_state(user.wait_for_delete_good)
    # Выйти
    else:
        await state.clear()
        await state.set_state(user.wait_user)
        await callback.message.delete(inline_message_id=callback.inline_message_id)
        user_id = callback.from_user.id
        await callback.message.answer(
            f"Добро пожаловать в юзер-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.user_manager_btns if db.get_job_id(user_id) == 1 else kb.user_btns)

@router.callback_query(user.wait_for_delete_good)
async def wait_for_delete_good(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cafe_id = data["delete_good"][2]
    short_name = data["delete_good"][1]
    art = data["delete_good"][0]
    if callback.data == "next_page":
        page = data["delete_good"][3] + 1
        keyboard = kb.update_goods_btns(short_name, art, cafe_id, page)
        from main import bot
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            reply_markup=keyboard)
        await state.update_data(wait_for_delete_good=(art, short_name, cafe_id, page))
        await state.set_state(user.wait_for_delete_good)
    if callback.data == "prev_page":
        page = data["wait_for_delete_good"][3] - 1
        keyboard = kb.update_goods_btns(short_name, art, cafe_id, page)
        from main import bot
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            reply_markup=keyboard)
        await state.update_data(wait_for_delete_good=(art, short_name, cafe_id, page))
        await state.set_state(user.wait_for_delete_good)
    elif callback.data not in ["⛔", "prev_page", "next_page", "ready"]:
        from main import bot
        c_data = callback.data
        await bot.edit_message_text(text=f"Удалить {db.get_good_short_name(cafe_id= c_data[0], art = c_data[1:])[0][0]}, арт. {c_data[1:]}?", chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id, reply_markup=kb.y_n_btns)
        await state.update_data(wait_for_delete=c_data)
        await state.set_state(user.wait_for_confirm_delete)
    elif callback.data == "ready":
        from main import bot
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await state.set_state(user.wait_for_exit)
        await state.clear()
        await state.set_state(user.wait_user)
        user_id = callback.from_user.id
        await callback.message.answer(
            f"Добро пожаловать в юзер-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.user_manager_btns if db.get_job_id(user_id) == 1 else kb.user_btns)


@router.callback_query(user.wait_for_confirm_delete)
async def wait_for_create_order(callback: CallbackQuery, state: FSMContext):
    if callback.data == "yes":
        data = await state.get_data()
        c_data = data["wait_for_delete"]
        db.delete_good(c_data[0], c_data[1:])
        await callback.message.edit_text(f"Удалено", reply_markup=None)
        cafe_id = db.get_cafe_id(callback.from_user.id)
        art = db.get_all_goods_art(cafe_id)
        short_name = db.get_all_goods_short_name(cafe_id)
        await state.update_data(delete_good=(art, short_name, cafe_id, 1))
        keyboard = kb.create_goods_btns(short_name, art, cafe_id)
        await callback.message.answer(f"Что удалить?", reply_markup=keyboard)  # клава с товарами
        await state.set_state(user.wait_for_delete_good)
    else:
        await callback.message.edit_text(f"Не удалось удалить", reply_markup=None)
        cafe_id = db.get_cafe_id(callback.from_user.id)
        art = db.get_all_goods_art(cafe_id)
        short_name = db.get_all_goods_short_name(cafe_id)
        await state.update_data(delete_good=(art, short_name, cafe_id, 1))
        keyboard = kb.create_goods_btns(short_name, art, cafe_id)
        await callback.message.answer(f"Что удалить?", reply_markup=keyboard)  # клава с товарами
        await state.set_state(user.wait_for_delete_good)
@router.message(user.wait_for_create_good)
async def wait_for_create_good(message: Message, state: FSMContext):
    await message.answer(f"Позиция(-и) добавлена(-ы)", reply_markup=kb.exit_user_btns)
    cafe_id = db.get_cafe_id(message.from_user.id)
    param = message.text.splitlines()
    data = []
    for i in range(0, len(param), 4):
        data.append(param[i:i + 4])
    for i in range(len(data)):
        db.insert_good(data[i][0], data[i][1], data[i][2], data[i][3].lower().replace('.', ''), cafe_id)


@router.callback_query(user.wait_for_create_order)
async def wait_for_create_order(callback: CallbackQuery, state: FSMContext):
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
        from main import bot
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        try:
            data = await state.get_data()
            info = data["wait_for_good_count"]
            data_str = '\n'.join(
                [str(index + 1) + '. ' + sublist[0] + ', арт. ' + sublist[1] + ', ' + sublist[2] + ' ' + sublist[3] + '.'
                 for
                 index, sublist in enumerate(info)])
            await callback.message.answer(data_str, reply_markup=kb.exit_user_btns)
            await state.set_state(user.wait_for_exit)
        except KeyError:
            await state.clear()
            await state.set_state(user.wait_user)
            user_id = callback.from_user.id
            await callback.message.answer(
                f"Добро пожаловать в юзер-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
                reply_markup=kb.user_manager_btns if db.get_job_id(user_id) == 1 else kb.user_btns)


@router.message(user.wait_for_good_count)
async def wait_for_good_count(message: Message, state: FSMContext):
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

"""Написать разработчику"""
@router.message(user.wait_for_user_message)
async def send(message: Message, state: FSMContext):
    from main import bot
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id-1)
    await message.answer(f"Cообщение доставлено", reply_markup=kb.exit_user_btns)
    from main import bot
    await bot.send_message(695088267, f"Сообщение от {message.from_user.full_name}:\n{message.text}")
    await state.set_state(user.wait_for_exit)


@router.callback_query(user.wait_for_exit)
async def user_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(user.wait_user)
    from main import bot
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=None)
    user_id = callback.from_user.id
    await callback.message.answer(
        f"Добро пожаловать в юзер-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
        reply_markup=kb.user_manager_btns if db.get_job_id(user_id) == 1 else kb.user_btns)

@router.callback_query(lambda q: q.data == 'exit_user')
async def user_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(user.wait_user)
    await callback.message.delete(inline_message_id=callback.inline_message_id)
    user_id = callback.from_user.id
    await callback.message.answer(
        f"Добро пожаловать в юзер-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
        reply_markup=kb.user_manager_btns if db.get_job_id(user_id) == 1 else kb.user_btns)

