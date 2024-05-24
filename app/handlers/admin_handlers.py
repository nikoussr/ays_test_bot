import aiogram.exceptions
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaDocument, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram import Router
import app.keyboards as kb
from states.test import admin
from aiogram.fsm.context import FSMContext
from app.database.bd import Database
from main import bot
from configs import JOBS, CAFES

router = Router()
mas = []

db = Database('../data/ays_test_database.db')

"""Обработчик кнопок админ панели"""


@router.callback_query(admin.wait_admin)
async def admin_panel(callback: CallbackQuery, state: FSMContext):
    print("Вошел в админ-панель")
    if callback.data == 'all_message':
        keyboard = kb.create_cafe_id_btns_message()
        keyboard.inline_keyboard.append([InlineKeyboardButton(text='⏪ Выйти', callback_data='exit')])
        await callback.message.edit_text(f"Кому хотете отправить сообщение?",
                                         reply_markup=keyboard)
        await state.set_state(admin.wait_all_message)
    elif callback.data == 'user_data':
        keyboard = kb.create_cafe_id_people_btns()
        keyboard.inline_keyboard.append([InlineKeyboardButton(text='⏪ Выйти', callback_data='exit')])

        await callback.message.edit_text(f"Поиск сотрудника\nВыберите заведение",
                                         reply_markup=keyboard)
        await state.set_state(admin.wait_user_FL)
    elif callback.data == 'make_a_chapter':
        keyboard = kb.create_cafe_btns()
        keyboard.inline_keyboard.append([InlineKeyboardButton(text='⏪ Выйти', callback_data='exit')])
        await callback.message.edit_text(f"Для кого будет БЗ?", reply_markup=keyboard)
        await state.set_state(admin.wait_for_cafe_id)
    elif callback.data == 'list_of_kd':
        keyboard = kb.create_cafe_btns()
        keyboard.inline_keyboard.append([InlineKeyboardButton(text='⏪ Выйти', callback_data='exit')])
        await callback.message.edit_text(f"Для кого хотите посмотреть БЗ?", reply_markup=keyboard)
        await state.set_state(admin.wait_for_job_id_2)
    elif callback.data == "find_admin_kd":
        await callback.message.edit_text(f"Поиск БЗ по ключевому слову\nВведите слово или предложение")
        await state.set_state(admin.wait_for_find_kd)


"""Поиск инфы по сотруднику"""


@router.callback_query(admin.wait_user_FL)
async def choose_user(callback: CallbackQuery, state: FSMContext):
    if callback.data == "exit":
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        user_id = callback.from_user.id
        await callback.message.answer(
            f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.admin_btns)
        await state.set_state(admin.wait_admin)
    else:
        data = callback.data.split('_')
        cafe_id = data[0]
        cafe = data[1]
        await state.update_data(wait_user_FL=(cafe_id, cafe))
        people = db.get_people(cafe_id)
        await callback.message.edit_text(f"Сотрудники в {cafe}", reply_markup=kb.create_job_people_btns(people))
        await state.set_state(admin.wait_user_info)


@router.callback_query(admin.wait_user_info)
async def get_user_data(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    user_id = callback.data
    info = db.get_user(user_id)
    await callback.message.answer(f"Порядковый номер: {info[0]}\n"
                                  f"Tелеграм id: {info[1]}\n"
                                  f"ФИ: {info[2]} {info[3]}\n"
                                  f"Дата раждения: {info[4]}\n"
                                  f"Номер телефона: {info[5]}\n"
                                  f"Должность: {info[6]}\n"
                                  f"Заведение: {info[7]}\n"
                                  f"Дата регистрации: {info[8]}", reply_markup=kb.update_user_btns)
    await state.update_data(wait_user_info=info[1])
    await state.set_state(admin.wait_for_user_update)


@router.callback_query(admin.wait_for_user_update)
async def choose_user_update(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=None)
    if callback.data == 'change_job_id':
        keyboard = kb.create_job_id_btns_register()
        # keyboard.inline_keyboard.append([InlineKeyboardButton(text='↩️ Назад', callback_data='back')])
        await callback.message.answer(f"На какую должность перевести сотрудника?", reply_markup=keyboard)
        await state.set_state(admin.wait_for_change_job_id)

        @router.callback_query(admin.wait_for_change_job_id)
        async def change_job_id(callback: CallbackQuery, state: FSMContext):
            if callback.data != 'back':
                await bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                                    message_id=callback.message.message_id,
                                                    reply_markup=None)
                data = await state.get_data()
                user_id = data["wait_user_info"]
                job = callback.data
                db.set_job_id(user_id, job[0])
                await callback.message.edit_text(f"Сотрудник будет переведен на должность {job[2:]}",
                                                 reply_markup=kb.exit_btns)
    elif callback.data == 'change_cafe_id':
        keyboard = kb.create_cafe_id_btns_register()
        # keyboard.inline_keyboard.append([InlineKeyboardButton(text='↩️ Назад', callback_data='back')])
        await callback.message.answer(f"В какое заведение перевести сотрудника?", reply_markup=keyboard)
        await state.set_state(admin.wait_for_change_cafe_id)

        @router.callback_query(admin.wait_for_change_cafe_id)
        async def change_cafe_id(callback: CallbackQuery, state: FSMContext):
            if callback.data != 'back':
                await bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                                    message_id=callback.message.message_id,
                                                    reply_markup=None)
                data = await state.get_data()
                user_id = data["wait_user_info"]
                cafe = callback.data
                db.set_cafe_id(user_id, cafe[0])
                await callback.message.edit_text(f"Сотрудник будет переведен в {cafe[2:]}", reply_markup=kb.exit_btns)
    elif callback.data == 'delete_user':
        await callback.message.answer(
            f"Вы действительно хотите удалить сотрудника?\nПодтвердив, он навсегда исчезнет из базы данных!",
            reply_markup=kb.y_n_btns)
        await state.set_state(admin.wait_for_delete_user)

        @router.callback_query(admin.wait_for_delete_user)
        async def delete_user(callback: CallbackQuery, state: FSMContext):
            if callback.data == "yes":
                db.set_banned_user(callback.from_user.id)
                db.delete_user(callback.from_user.id)
            elif callback.data == "no":
                await bot.delete_message(chat_id=callback.from_user.id,
                                         message_id=callback.message.message_id)
                user_id = callback.from_user.id
                await callback.message.answer(
                    f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
                    reply_markup=kb.admin_btns)
                await state.set_state(admin.wait_admin)
    elif callback.data == 'back':
        data = await state.get_data()
        cafe_id = data["wait_user_FL"][0]
        cafe = data["wait_user_FL"][1]
        await state.update_data(wait_user_FL=(cafe_id, cafe))
        people = db.get_people(cafe_id)
        await callback.message.answer(f"Сотрудники в {cafe}", reply_markup=kb.create_job_people_btns(people))
        await state.set_state(admin.wait_user_info)
    elif callback.data == 'exit':
        user_id = callback.from_user.id
        await callback.message.answer(
            f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.admin_btns)
        await state.set_state(admin.wait_admin)

"""Рассылка"""


@router.callback_query(admin.wait_all_message)
async def get_user_ids(callback: CallbackQuery, state: FSMContext):
    if callback.data == "exit":
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        user_id = callback.from_user.id
        await callback.message.answer(
            f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.admin_btns)
        await state.set_state(admin.wait_admin)
    else:
        print("Делает рассылку")
        data = callback.data.split('_')
        cafe_id = data[0]
        cafe = data[1]
        await state.update_data(wait_all_message=cafe_id)
        await callback.message.edit_text(f"Сообщение будет для: {cafe}")
        await callback.message.answer(f"Введите текст")
        await state.set_state(admin.wait_for_cafe_mes)


@router.message(admin.wait_for_cafe_mes)
async def get_user_ids(message: Message, state: FSMContext):
    data = await state.get_data()
    cafe_id = data["wait_all_message"]
    text = message.caption  # берем от пользователя текст
    document = message.document
    if not text:
        text = message.text
    photo = message.photo  # берем все фото от пользователя
    group_elements = []  # создаем массив групповых элементов (видева, фотоб аудио...)
    if photo is not None:  # если есть хоть одно фото, то
        photo = photo[-1].file_id  # берем самое лучше качество через [-1]
        input_media = InputMediaPhoto(media=photo)
        group_elements.append(input_media)
    if document is not None:  # если есть хоть один документ, то
        print(document)
        document = document.file_id  # берем id файла
        input_media = InputMediaDocument(media=document)
        group_elements.append(input_media)
    if cafe_id == "0":
        all_ids = db.get_all_ids()  # берёт из БД все id

    else:
        all_ids = db.get_all_ids_cafe(cafe_id)

    cnt = 0
    if group_elements and text:
        for id in all_ids:
            try:
                await bot.send_media_group(id[0], group_elements)
                await bot.send_message(id[0], text)
                print(f"Сообщение дошло до {id[0]}")
                cnt += 1
            except:
                print(f"Сообщение не дошло до {id[0]}")
    elif group_elements:
        for id in all_ids:
            try:
                await bot.send_media_group(id[0], group_elements)
                print(f"Сообщение дошло до {id[0]}")
                cnt += 1
            except:
                print(f"Сообщение не дошло до {id[0]}")
    elif text:
        for id in all_ids:
            try:
                await bot.send_message(id[0], text)
                print(f"Сообщение дошло до {id[0]}")
                cnt += 1
            except:
                print(f"Сообщение не дошло до {id[0]}")

    await message.answer(
        f"Сообщение отправлено {cnt}/{len(all_ids)} пользователям.\nЕсли сообщение не отправлено, значит пользователь удалил или заблокировал бота",
        reply_markup=kb.exit_btns)


"""Создание БЗ"""


@router.callback_query(
    lambda q: q.data in CAFES or q.data == "exit", admin.wait_for_cafe_id)
async def set_cafe_id(callback: CallbackQuery, state: FSMContext):
    if callback.data == "exit":
        user_id = callback.from_user.id
        await callback.message.answer(
            f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.admin_btns)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await state.set_state(admin.wait_admin)
    else:
        print("Создаёт БЗ, выбор заведения")
        cafe_id = callback.data.split('_')  # приходит в формате "1_Бугель Вугель"
        await state.update_data(wait_for_cafe_id=cafe_id)
        await callback.message.edit_text(f'БЗ будет для заведения: {cafe_id[1]}')
        await callback.message.answer(f"Для кого будет БЗ?", reply_markup=kb.create_job_btns(cafe_id[0]))
        await state.set_state(admin.wait_for_job_id_1)


@router.callback_query(
    lambda q: q.data in JOBS, admin.wait_for_job_id_1)
async def set_job_id(callback: CallbackQuery, state: FSMContext):
    print("Создаёт БЗ, выбор должности")

    job_id = callback.data.split('_')  # приходит в формате "1_Менеджер"
    data = await state.get_data()
    cafe_id = data["wait_for_cafe_id"]
    await state.update_data(wait_for_job_id_1=job_id)  # сразу добавляет в БД
    await callback.message.edit_text(f'БЗ будет для должности: {job_id[1]}')
    all_folders = db.get_folders(cafe_id=cafe_id[0], job_id=job_id[0])
    await callback.message.answer(f"Выберите папку или создайте новую",
                                  reply_markup=kb.create_folders_btn(all_folders=all_folders))
    await state.set_state(admin.wait_for_folder)


@router.callback_query(admin.wait_for_folder)
async def create_new_folder(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'new_folder':
        await callback.message.answer(f"Введите название для папки")
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

        @router.message()
        async def new_folder_name(message: Message):
            folder_name = message.text
            await state.update_data(wait_for_folder=folder_name)
            await bot.edit_message_text(text=f"Папка: {folder_name}", chat_id=message.chat.id,
                                        message_id=message.message_id - 1)
            await callback.message.answer(f"Введите название для БЗ")
            await state.set_state(admin.wait_for_chapter_name)
    else:
        data = callback.data
        data = data.split('_')
        folder_name = data[1]
        await state.update_data(wait_for_folder=data)
        await bot.edit_message_text(text=f"Папка: {folder_name}", chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id)
        await callback.message.answer(f"Введите название для БЗ")
        await state.set_state(admin.wait_for_chapter_name)


@router.message(admin.wait_for_chapter_name)
async def set_chapter_name(message: Message, state: FSMContext):
    print("Создаёт БЗ, выбирает имя")
    schapter_name = message.text
    await state.update_data(wait_for_chapter_name=schapter_name)
    await message.answer(f"Введите текст для БЗ. Можно добавить фотографии")
    await state.set_state(admin.wait_for_chapter_text)


@router.message(admin.wait_for_chapter_text)
async def set_chapter_text_photo(message: Message, state: FSMContext):
    print("Создаёт БЗ, вставляет текст + фото")

    data = await state.get_data()
    photos = data.get('photos', [])
    captions = data.get('captions', {})
    texts = data.get('texts', [])

    text = ''
    if message.text:
        # Если пришло только текстовое сообщение
        for x in range(0, len(message.text), 4000):
            text = message.text[x:x + 4000]
            texts.append(text)
        await state.update_data(texts=texts)

    elif message.photo:
        # Если пришла только фотография
        photo_id = message.photo[-1].file_id
        photos.append(photo_id)

        if len(photos) == 1:
            caption = message.caption
            captions[photo_id] = caption

        await state.update_data(photos=photos, captions=captions)
    try:
        await bot.edit_message_text(text=f"Правильно ли введён текст?", chat_id=message.chat.id,
                                    message_id=message.message_id - 1, reply_markup=kb.y_n_btns)
    except aiogram.exceptions.TelegramBadRequest:
        pass
    await state.set_state(admin.wait_yes_no)

    @router.callback_query(lambda q: q.data == 'yes', admin.wait_yes_no)
    async def yes(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        cafe_id = data["wait_for_cafe_id"][0]
        job_id = data["wait_for_job_id_1"][0]
        kd_name = data["wait_for_chapter_name"]
        kd_text = data.get('texts', [])
        text = ''
        for x in kd_text:
            text += x
            print(len(text))
        photos = data.get('photos', [])
        captions = data.get('captions', {})
        print(f"Длина текста - {kd_text}")
        if isinstance(data["wait_for_folder"], list):
            folder_id = data["wait_for_folder"][0]
            db.set_kd(cafe_id, job_id, kd_name, folder_id, (text if kd_text else captions.get(photos[0])))
            base_id = db.get_base_id()
            for photo in photos:
                db.set_kd_photo(base_id, photo)
        else:
            folder_name = data["wait_for_folder"]
            db.set_folder_name(folder_name=folder_name)
            folder_id = db.get_folder_id()
            db.set_kd(cafe_id, job_id, kd_name, folder_id, (text if kd_text else captions.get(photos[0])))
            base_id = db.get_base_id()
            for photo in photos:
                db.set_kd_photo(base_id, photo)
        await callback.message.edit_text(f'БЗ успешно сохранена', reply_markup=kb.exit_btns)
        await state.clear()

    @router.callback_query(lambda q: q.data == 'no', admin.wait_yes_no)
    async def no(callback: CallbackQuery, state: FSMContext):
        db.delete_unkd()
        await state.clear()
        await state.set_state(admin.wait_admin)
        await callback.message.edit_text('Повторное создание БЗ...', reply_markup=None)
        await callback.message.answer(f"Для кого будет БЗ?", reply_markup=kb.create_cafe_btns())
        await state.set_state(admin.wait_for_cafe_id)


"""Просмотр БЗ"""


@router.callback_query(lambda q: q.data in CAFES or q.data == "exit", admin.wait_for_job_id_2)
async def list_of_cafes(callback: CallbackQuery, state: FSMContext):
    if callback.data == "exit":
        user_id = callback.from_user.id
        await callback.message.answer(
            f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.admin_btns)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await state.set_state(admin.wait_admin)
    else:
        print("Смотрит БЗ, выбирает заведение")
        cafe_id = callback.data.split('_')
        await state.update_data(wait_for_job_2=cafe_id[0])
        await callback.message.edit_text(f"Просмотр БЗ для {cafe_id[1]}")
        await callback.message.answer(f"Для кого вы хотите посмотреть БЗ?", reply_markup=kb.create_job_btns(cafe_id[0]))
        await state.set_state(admin.wait_for_click_kd_3)


@router.callback_query(lambda q: q.data in JOBS, admin.wait_for_click_kd_3)
async def list_of_jobs(callback: CallbackQuery, state: FSMContext):
    print("Смотрит БЗ, выбирает должность")
    data = await state.get_data()
    cafe_id = data["wait_for_job_2"]
    job = callback.data.split('_')
    await state.update_data(wait_for_click_kd_3=job)
    all_folders = db.get_folders(cafe_id=cafe_id[0], job_id=job[0])
    all_folders = kb.create_folders_btn_look(all_folders=all_folders)
    await callback.message.answer(f"Выберите папку",
                                  reply_markup=all_folders)
    await callback.message.edit_text(f"Вот все папки для должности {job[1]}", reply_markup=None)
    await state.set_state(admin.wait_for_click_kd_4)


@router.callback_query(admin.wait_for_click_kd_4)
async def create_new_folder(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cafe_id = data["wait_for_job_2"]
    job = data["wait_for_click_kd_3"]
    folder_id = callback.data
    folder_id = folder_id.split('_')
    kd_btns = kb.make_kd_kb1(job[0], cafe_id, folder_id[0])
    await callback.message.edit_text(f"Вот все БЗ в папке {folder_id[1]}", reply_markup=kd_btns)
    await state.set_state(admin.wait_for_click_kd_5)


@router.callback_query(lambda q: q.data, admin.wait_for_click_kd_5)
async def text_of_chapter(callback: CallbackQuery, state: FSMContext):
    global text
    data = callback.data.split('_')
    base_id = data[0]
    KD_text = db.get_kd_text(base_id)
    for x in range(0, len(KD_text), 4096):
        if len(KD_text) - x <= 4096:
            text = KD_text[x:x + 4096]
            break
        text = KD_text[x:x + 4096]
        await callback.message.answer(f"{text}")
    await callback.message.answer(f"{text}", reply_markup=kb.edit_btns)

    await state.update_data(wait_for_click_kd_1=base_id)
    group_elements = []  # создаем массив групповых элементов (видева, фотоб аудио...)
    photos = db.get_kd_photos(base_id)
    if photos is not None:
        for photo in photos:  # если есть хоть одно фото, то
            element = photo[0]
            input_media = InputMediaPhoto(media=element)
            group_elements.append(input_media)  # добавляем элементы
    try:
        await callback.message.answer_media_group(group_elements)  # вывод группы
    except:
        pass
    await state.set_state(admin.wait_for_click_kd_2)


"""Редактирование БЗ"""


@router.callback_query(lambda q: q.data, admin.wait_for_click_kd_2)
async def text_of_chapterh(callback: CallbackQuery, state: FSMContext):
    print("Редактирует БЗ, выбирает что")
    if callback.data == 'exit':
        await state.set_state(admin.wait_admin)
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            reply_markup=None)
        user_id = callback.from_user.id
        await callback.message.answer(
            f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.admin_btns)
    elif callback.data == 'edit_text':
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            reply_markup=None)
        await state.set_state(admin.wait_for_edit_text)
        await callback.message.answer(f"Введите новый текст")
    elif callback.data == 'edit_name':
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            reply_markup=None)
        await state.set_state(admin.wait_for_edit_name)
        await callback.message.answer(f"Введите новое название для БЗ")
    elif callback.data == 'edit_photo':
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            reply_markup=None)
        await state.set_state(admin.wait_for_edit_photo)
        await callback.message.answer(f"Отправьте новые фото. Если хотите удалить все фото, то отправьте 0")
    elif callback.data == 'delete_kd':
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            reply_markup=None)
        await state.set_state(admin.wait_for_check_3)
        await callback.message.answer(f"Удалить БЗ?", reply_markup=kb.y_n_btns)

        @router.callback_query(lambda q: q.data == 'yes', admin.wait_for_check_3)
        async def yes(callback: CallbackQuery, state: FSMContext):
            data = await state.get_data()
            db.delete_kd(data["wait_for_click_kd_1"])
            db.delete_unkd()
            await callback.message.answer(f'БЗ успешно удалена', reply_markup=kb.exit_btns)
            await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                                reply_markup=None)

        @router.callback_query(lambda q: q.data == 'no', admin.wait_for_check_3)
        async def no(callback: CallbackQuery, state: FSMContext):
            await state.set_state(admin.wait_admin)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            user_id = callback.from_user.id
            await callback.message.answer(
                f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
                reply_markup=kb.admin_btns)


@router.message(admin.wait_for_edit_text)
async def edit_text(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(wait_for_che=message.text)
    await bot.edit_message_text(f"Новый текст:\n{message.text}\nВсё верно?", chat_id=message.chat.id,
                                message_id=message.message_id - 1, reply_markup=kb.update_chapter_btns)
    await state.set_state(admin.wait_for_check_1)

    @router.callback_query(lambda q: q.data == 'okey', admin.wait_for_check_1)
    async def yes(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        db.set_kd_text(data["wait_for_click_kd_1"], data["wait_for_che"])
        await callback.message.answer(f'БЗ успешно отредактирована', reply_markup=kb.exit_btns)
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            reply_markup=None)

    @router.callback_query(lambda q: q.data == 'not_okey', admin.wait_for_check_1)
    async def no(callback: CallbackQuery, state: FSMContext):
        await state.set_state(admin.wait_admin)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        user_id = callback.from_user.id
        await callback.message.answer(
            f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.admin_btns)


@router.message(admin.wait_for_edit_photo)
async def edit_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    base_id = data["wait_for_click_kd_1"]
    if message.text == "0":
        db.delete_kd_photo(base_id)
    else:
        photo = message.photo  # берем все фото от пользователя
        photo = photo[-1].file_id  # берем самое лучше качество через [-1]
        db.set_kd_photo(base_id, photo)
    try:
        await bot.edit_message_text(text=f'БЗ успешно отредактирована', chat_id=message.chat.id,
                                    message_id=message.message_id - 1, reply_markup=kb.exit_btns)
    except aiogram.exceptions.TelegramBadRequest:
        pass



@router.message(admin.wait_for_edit_name)
async def edit_name(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(wait_for_edit_name=message.text)
    await bot.edit_message_text(f"Новое название:\n{message.text}\nВсё верно?", chat_id=message.chat.id,
                                message_id=message.message_id - 1, reply_markup=kb.update_chapter_btns)
    await state.set_state(admin.wait_for_check_2)

    @router.callback_query(lambda q: q.data == 'okey', admin.wait_for_check_2)
    async def yes(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        db.set_kd_name(data["wait_for_click_kd_1"], data["wait_for_edit_name"])
        await callback.message.answer(f'БЗ успешно отредактирована', reply_markup=kb.exit_btns)
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            reply_markup=None)

    @router.callback_query(lambda q: q.data == 'not_okey', admin.wait_for_check_2)
    async def no(callback: CallbackQuery, state: FSMContext):
        await state.set_state(admin.wait_admin)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        user_id = callback.from_user.id
        await callback.message.answer(
            f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.admin_btns)


@router.message(admin.wait_for_find_kd)
async def find_kd(message: Message, state: FSMContext):
    find_text = str(message.text)
    all_kd = db.get_all_kd_base()
    base_ids = []
    for kd in all_kd:
        text = str(db.get_kd_text(kd[1]))
        if (find_text in text) or (find_text.lower() in text) or (find_text.upper() in text) or (
                find_text[0].upper() in text):
            base_ids.append(kd[1])
    if base_ids:
        await message.answer(f"Выбирай", reply_markup=kb.make_kd_kb_base_ids(base_ids))
        await state.set_state(admin.wait_for_click_kd_5)
    else:
        await message.answer(f"Ничего не найдено", reply_markup=kb.exit_btns)


"""Выход"""


@router.callback_query(lambda q: q.data == 'exit')
async def user_data(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.message.answer(
        f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
        reply_markup=kb.admin_btns)
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=None)
    await state.set_state(admin.wait_admin)
