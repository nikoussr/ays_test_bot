import aiogram.exceptions
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaDocument
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
        await callback.message.edit_text(f"Кому хотете отправить сообщение?", reply_markup=kb.create_cafe_id_btns_message())
        await state.set_state(admin.wait_all_message)
    elif callback.data == 'user_data':
        await callback.message.edit_text(f"Поиск сотрудника\nВведите ФИ\nНапример: Иванов Иван", reply_markup=None)
        await state.set_state(admin.wait_user_FL)
    elif callback.data == 'make_a_chapter':
        await callback.message.edit_text(f"Для кого будет БЗ?", reply_markup=kb.create_cafe_btns())
        await state.set_state(admin.wait_for_cafe_id)
    elif callback.data == 'list_of_kd':
        await callback.message.edit_text(f"Для кого хотите посмотреть БЗ?", reply_markup=kb.create_cafe_btns())
        await state.set_state(admin.wait_for_job_id_2)


"""Поиск инфы по сотруднику"""


@router.message(admin.wait_user_FL)
async def get_user_data(message: Message, state: FSMContext):
    print("Ищет инфу по сотруднику")
    data = (message.text.split())
    info = db.get_user(data[1], data[0])
    await message.answer(f"Порядковый номер: {info[0]}\n"
                         f"Tелеграм id: {info[1]}\n"
                         f"ФИ: {info[3]} {info[2]}\n"
                         f"Номер телефона: {info[4]}\n"
                         f"Должность: {info[5]}\n"
                         f"Заведение: {info[6]}\n")
    await state.set_state(admin.wait_user_FL)
    await message.answer(f"Введите ФИ сотрудника", reply_markup=kb.exit_btns)
    await state.set_state(admin.wait_for_exit)


"""Рассылка"""


@router.callback_query(admin.wait_all_message)
async def get_user_ids(callback: CallbackQuery, state: FSMContext):
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
    await state.set_state(admin.wait_for_exit)


"""Создание БЗ"""


@router.callback_query(
    lambda q: q.data in CAFES, admin.wait_for_cafe_id)
async def set_cafe_id(callback: CallbackQuery, state: FSMContext):
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
                                  reply_markup=kb.create_folders_btn(all_folders = all_folders))
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
        data= data.split('_')
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

    if message.text:
        # Если пришло только текстовое сообщение
        await state.update_data(text=message.text)

    elif message.photo:
        # Если пришла только фотография
        photo_id = message.photo[-1].file_id
        photos.append(photo_id)

        if len(photos) == 1:
            caption = message.caption
            captions[photo_id] = caption

        await state.update_data(photos=photos, captions=captions)
    try:
        await bot.edit_message_text(text=f"Текст для БЗ: \n{message.text if message.text else message.caption}", chat_id=message.chat.id,
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
        kd_text = data.get('text')
        photos = data.get('photos', [])
        captions = data.get('captions', {})
        if isinstance(data["wait_for_folder"], list):
            folder_id = data["wait_for_folder"][0]
            db.set_kd(cafe_id, job_id, kd_name, folder_id, (kd_text if kd_text else captions.get(photos[0])))
            base_id = db.get_base_id()
            for photo in photos:
                db.set_kd_photo(base_id, photo)
        else:
            folder_name = data["wait_for_folder"]
            db.set_folder_name(folder_name=folder_name)
            folder_id = db.get_folder_id()
            db.set_kd(cafe_id, job_id, kd_name, folder_id, (kd_text if kd_text else captions.get(photos[0])))
            base_id = db.get_base_id()
            for photo in photos:
                db.set_kd_photo(base_id, photo)
        await callback.message.edit_text(f'БЗ успешно сохранена', reply_markup=kb.exit_btns)
        await state.clear()
        await state.set_state(admin.wait_for_exit)


    @router.callback_query(lambda q: q.data == 'no', admin.wait_yes_no)
    async def no(callback: CallbackQuery, state: FSMContext):
        db.delete_unkd()
        await state.clear()
        await state.set_state(admin.wait_admin)
        await callback.message.edit_text('Повторное создание БЗ...', reply_markup=None)
        await callback.message.answer(f"Для кого будет БЗ?", reply_markup=kb.create_cafe_btns())
        await state.set_state(admin.wait_for_job_id_1)


"""Просмотр БЗ"""


@router.callback_query(lambda q: q.data in CAFES, admin.wait_for_job_id_2)
async def list_of_cafes(callback: CallbackQuery, state: FSMContext):
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
    kd_btns, kds = kb.make_kd_kb1(job[0], cafe_id, folder_id[0])
    await callback.message.edit_text(f"Вот все БЗ в папке {folder_id[1]}", reply_markup=kd_btns)
    await state.set_state(admin.wait_for_click_kd_5)



@router.callback_query(lambda q: q.data, admin.wait_for_click_kd_5)
async def text_of_chapter(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    base_id = data[0]
    KD_name = data[1]
    KD_text = db.get_text_of_kd(base_id)
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
    await callback.message.answer(f"{KD_text}", reply_markup=kb.edit_btns)
    await state.set_state(admin.wait_for_click_kd_2)


"""Редактирование БЗ"""


@router.callback_query(lambda q: q.data, admin.wait_for_click_kd_2)
async def text_of_chapterh(callback: CallbackQuery, state: FSMContext):
    print("Редактирует БЗ, выбирает что")
    if callback.data == 'exit':
        await state.set_state(admin.wait_admin)
        # await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
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
            await state.set_state(admin.wait_for_exit)

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
        await state.set_state(admin.wait_for_exit)

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
    await state.set_state(admin.wait_for_exit)


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
        await state.set_state(admin.wait_for_exit)

    @router.callback_query(lambda q: q.data == 'not_okey', admin.wait_for_check_2)
    async def no(callback: CallbackQuery, state: FSMContext):
        await state.set_state(admin.wait_admin)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        user_id = callback.from_user.id
        await callback.message.answer(
            f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
            reply_markup=kb.admin_btns)


"""Выход"""


@router.callback_query(lambda q: q.data == 'exit', admin.wait_for_exit)
async def user_data(callback: CallbackQuery, state: FSMContext):
    await state.set_state(admin.wait_admin)
    # await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=None)
    user_id = callback.from_user.id
    await callback.message.answer(
        f"Добро пожаловать в админ-панель, {db.get_first_name(user_id)} {db.get_last_name(user_id)}!",
        reply_markup=kb.admin_btns)
