from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from configs import JOBS, CAFES, JOBS_EM
from app.database.bd import Database

db = Database('../data/ays_test_database.db')

"""Клавиатура для работ"""


def create_job_btns(cafe_id):
    """Создаёт кнопки для всех должностей, Менеджер 4"""
    all_jobs = []
    jobs_count = 0
    while jobs_count < len(JOBS):
        if len(JOBS) - jobs_count >= 2:
            all_jobs.append([InlineKeyboardButton(
                text=JOBS[jobs_count][2:] + ' ' + db.get_cnt_of_kd_job_id(JOBS[jobs_count][0], cafe_id),
                callback_data=JOBS[jobs_count]),
                InlineKeyboardButton(
                    text=JOBS[jobs_count + 1][2:] + ' ' + db.get_cnt_of_kd_job_id(JOBS[jobs_count + 1][0],
                                                                                  cafe_id),
                    callback_data=JOBS[jobs_count + 1])])
            jobs_count += 2
        else:
            all_jobs.append([InlineKeyboardButton(
                text=JOBS[jobs_count][2:] + ' ' + db.get_cnt_of_kd_job_id(JOBS[jobs_count][0], cafe_id),
                callback_data=JOBS[jobs_count])])
            jobs_count += 1
    return InlineKeyboardMarkup(inline_keyboard=all_jobs)


def create_job_id_btns_register():
    """Создаёт кнопки должностей для регистрации"""
    all_jobs = []
    jobs_count = 0
    while jobs_count < len(JOBS):
        if len(JOBS) - jobs_count >= 2:
            all_jobs.append([InlineKeyboardButton(text=JOBS[jobs_count][2:], callback_data=JOBS[jobs_count]),
                             InlineKeyboardButton(text=JOBS[jobs_count + 1][2:], callback_data=JOBS[jobs_count + 1])])
            jobs_count += 2
        else:
            all_jobs.append([InlineKeyboardButton(text=JOBS[jobs_count][2:], callback_data=JOBS[jobs_count])])
            jobs_count += 1
    return InlineKeyboardMarkup(inline_keyboard=all_jobs)


"""Клавиатура для заведений"""


def create_cafe_btns():
    """Просмотр, создание БЗ"""
    all_cafes = []
    cafes_count = 0
    while cafes_count < len(CAFES):
        if len(CAFES) - cafes_count >= 2:
            all_cafes.append([InlineKeyboardButton(
                text=CAFES[cafes_count][2:] + ' ' + db.get_cnt_of_kd_cafe_id(CAFES[cafes_count][0]),
                callback_data=CAFES[cafes_count]),
                InlineKeyboardButton(text=CAFES[cafes_count + 1][2:] + ' ' + db.get_cnt_of_kd_cafe_id(
                    CAFES[cafes_count + 1][0]), callback_data=CAFES[cafes_count + 1])])
            cafes_count += 2
        else:
            all_cafes.append([InlineKeyboardButton(
                text=CAFES[cafes_count][2:] + ' ' + db.get_cnt_of_kd_cafe_id(CAFES[cafes_count][0]),
                callback_data=CAFES[cafes_count])])
            cafes_count += 1

    return InlineKeyboardMarkup(inline_keyboard=all_cafes)


def create_cafe_id_btns_register():
    """Создаёт кнопки заведений для регистрации"""
    all_cafes = []
    cafes_count = 0
    while cafes_count < len(CAFES):
        if len(CAFES) - cafes_count >= 2:
            all_cafes.append([InlineKeyboardButton(text=CAFES[cafes_count][2:], callback_data=CAFES[cafes_count]),
                              InlineKeyboardButton(text=CAFES[cafes_count + 1][2:],
                                                   callback_data=CAFES[cafes_count + 1])])
            cafes_count += 2
        else:
            all_cafes.append([InlineKeyboardButton(text=CAFES[cafes_count][2:], callback_data=CAFES[cafes_count])])
            cafes_count += 1

    return InlineKeyboardMarkup(inline_keyboard=all_cafes)


def create_cafe_id_btns_message():
    """Создаёт кнопки заведений для рассылки"""
    all_cafes = []
    cafes_count = 0
    while cafes_count < len(CAFES):
        if len(CAFES) - cafes_count >= 2:
            all_cafes.append([InlineKeyboardButton(text=CAFES[cafes_count][2:], callback_data=CAFES[cafes_count]),
                              InlineKeyboardButton(text=CAFES[cafes_count + 1][2:],
                                                   callback_data=CAFES[cafes_count + 1])])
            cafes_count += 2
        else:
            all_cafes.append([InlineKeyboardButton(text=CAFES[cafes_count][2:], callback_data=CAFES[cafes_count])])
            cafes_count += 1
    all_cafes.append([InlineKeyboardButton(text="Всеобщая рассылка", callback_data='0_всех')])

    return InlineKeyboardMarkup(inline_keyboard=all_cafes, )


"""Клавиатура для баз знаний"""


def make_kd_kb(job_id):
    all_bases = []
    kds = []
    all_kds = (db.get_all_kd_j(job_id))
    for kd in all_kds:
        if kd[0] is not None:
            kds.append(str(kd[1]) + kd[0])
            all_bases.append([InlineKeyboardButton(text=kd[0], callback_data=str(kd[1]) + '_' + kd[0])])
    return InlineKeyboardMarkup(inline_keyboard=all_bases), kds


def make_kd_kb1(job_id, cafe_id, folder_id):
    all_bases = []
    all_kds = db.get_all_kd(job_id, cafe_id, folder_id)
    for kd in all_kds:
        if kd[0] is not None:
            all_bases.append([InlineKeyboardButton(text=kd[0], callback_data=str(kd[1]) + '_' + kd[0][:30])])
    return InlineKeyboardMarkup(inline_keyboard=all_bases)


def make_kd_kb_base_ids(base_ids):
    all_bases = []
    kd_names = []
    for base_id in base_ids:
        kd_names.append((db.get_kd_name(base_id), base_id))
    print(kd_names)
    for name, id in kd_names:
        print(name + ' ' + str(id))
        all_bases.append([InlineKeyboardButton(text=name, callback_data=str(id))])
    return InlineKeyboardMarkup(inline_keyboard=all_bases)


"""Клавиатуры для folders"""


def create_folders_btn(all_folders):
    """Создание новой БЗ"""
    folders = []
    folders_count = 0
    if len(all_folders) == 0:
        folders.append([InlineKeyboardButton(text="➕ Создать новую папку", callback_data='new_folder')])

        return InlineKeyboardMarkup(inline_keyboard=folders)
    else:
        while folders_count < len(all_folders):
            if len(all_folders) - folders_count >= 2:
                folders.append([InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count][1]),
                                                     callback_data=str(all_folders[folders_count][0]) + '_' + str(
                                                         all_folders[folders_count][1])),
                                InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count + 1][1]),
                                                     callback_data=str(all_folders[folders_count + 1][0]) + '_' + str(
                                                         all_folders[folders_count + 1][1]))])
                folders_count += 2
            else:
                folders.append([InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count][1]),
                                                     callback_data=str(all_folders[folders_count][0]) + '_' + str(
                                                         all_folders[folders_count][1]))])
                folders_count += 1
        folders.append([InlineKeyboardButton(text="➕ Создать новую папку", callback_data='new_folder')])

        return InlineKeyboardMarkup(inline_keyboard=folders)


def create_folders_btn_look(all_folders):
    """Просмотр БЗ"""
    folders = []
    folders_count = 0
    if len(all_folders) == 0:
        return InlineKeyboardMarkup(inline_keyboard=folders)
    else:
        while folders_count < len(all_folders):
            if len(all_folders) - folders_count >= 2:
                folders.append([InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count][1]),
                                                     callback_data=str(all_folders[folders_count][0]) + '_' + str(
                                                         all_folders[folders_count][1])),
                                InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count + 1][1]),
                                                     callback_data=str(all_folders[folders_count + 1][0]) + '_' + str(
                                                         all_folders[folders_count + 1][1]))])
                folders_count += 2
            else:
                folders.append([InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count][1]),
                                                     callback_data=str(all_folders[folders_count][0]) + '_' + str(
                                                         all_folders[folders_count][1]))])
                folders_count += 1
        return InlineKeyboardMarkup(inline_keyboard=folders)


"""Клавиатура с товарами"""


def create_goods_btns(short_name, id):
    pages = len(id) // 10 + 1
    goods = []
    if pages > 1:
        goods.append(
            [InlineKeyboardButton(text="⛔", callback_data='⛔'), InlineKeyboardButton(text='1', callback_data="⛔"),
             InlineKeyboardButton(text=">>", callback_data="next_page")])
        index = 0
        while index < 10:
            text = short_name[index][0]
            cal = str(id[index][0])
            goods.append(
                [InlineKeyboardButton(text=text, callback_data=cal)])
            index += 1
    else:
        index = 0
        while index < len(id):
            text = short_name[index][0]
            cal = str(id[index][0])
            goods.append(
                [InlineKeyboardButton(text=text, callback_data=cal)])
            index += 1
    goods.append([InlineKeyboardButton(text="Сформировать ⏩", callback_data="ready")])
    return InlineKeyboardMarkup(inline_keyboard=goods)


"""Клавиатура с обновлёнными товарами"""


def update_goods_btns(short_name, ids, page):
    goods = []
    if (len(ids) // 10 + 1 - page) == 0 and page > 1:
        goods.append([InlineKeyboardButton(text="<<", callback_data='prev_page'),
                      InlineKeyboardButton(text=str(page), callback_data="⛔"),
                      InlineKeyboardButton(text="⛔", callback_data="⛔")])
        short_name = short_name[(page - 1) * 10:page * 10]
        ids = ids[(page - 1) * 10:page * 10]
        index = 0
        while index < len(ids):
            text = short_name[index][0]
            cal = str(ids[index][0])
            goods.append(
                [InlineKeyboardButton(text=text, callback_data=cal)])
            index += 1
    elif page == 1:
        goods.append(
            [InlineKeyboardButton(text="⛔", callback_data='⛔'), InlineKeyboardButton(text=str(page), callback_data="⛔"),
             InlineKeyboardButton(text=">>", callback_data="next_page")])
        short_name = short_name[:page * 10]
        ids = ids[:page * 10]
        index = 0
        while index < len(ids):
            text = short_name[index][0]
            cal = str(ids[index][0])
            goods.append(
                [InlineKeyboardButton(text=text, callback_data=cal)])
            index += 1
    else:
        goods.append(
            [InlineKeyboardButton(text="<<", callback_data='prev_page'),
             InlineKeyboardButton(text=str(page), callback_data="⛔"),
             InlineKeyboardButton(text=">>", callback_data="next_page")])
        short_name = short_name[(page - 1) * 10:page * 10]
        ids = ids[(page - 1) * 10:page * 10]
        index = 0
        while index < len(ids):
            text = short_name[index][0]
            cal = str(ids[index][0])
            goods.append(
                [InlineKeyboardButton(text=text, callback_data=cal)])
            index += 1
    goods.append([InlineKeyboardButton(text="Сформировать ⏩", callback_data="ready")])
    return InlineKeyboardMarkup(inline_keyboard=goods)


"""def create_find_people(cafe_id):
    all_bases = []
    kds = []
    all_kds = (db.get_all_kd_j(job_id))
    for kd in all_kds:
        if kd[0] is not None:
            kds.append(str(kd[1]) + kd[0])
            all_bases.append([InlineKeyboardButton(text=kd[0], callback_data=str(kd[1]) + '_' + kd[0])])
    return InlineKeyboardMarkup(inline_keyboard=all_bases), kds"""


def create_job_people_btns(people):
    """Просмотр, создание БЗ"""
    all_people = []
    people_count = 0
    while people_count < len(people):
        if len(people) - people_count >= 2:
            all_people.append([InlineKeyboardButton(
                text=JOBS_EM[people[people_count][3]] + ' ' + people[people_count][0] + ' ' + people[people_count][1],
                callback_data=str(people[people_count][2])),
                InlineKeyboardButton(
                    text=JOBS_EM[people[people_count + 1][3]] + ' ' + people[people_count + 1][0] + ' ' +
                         people[people_count + 1][1], callback_data=str(people[people_count + 1][2]))])
            people_count += 2
        else:
            all_people.append([InlineKeyboardButton(
                text=JOBS_EM[people[people_count][3]] + ' ' + people[people_count][0] + ' ' + people[people_count][1],
                callback_data=str(people[people_count][2]))])
            people_count += 1

    return InlineKeyboardMarkup(inline_keyboard=all_people)


def create_cafe_id_people_btns():
    """Просмотр, создание БЗ"""
    all_cafes = []
    cafes_count = 0
    while cafes_count < len(CAFES):
        if len(CAFES) - cafes_count >= 2:
            all_cafes.append([InlineKeyboardButton(
                text=CAFES[cafes_count][2:] + ' ' + db.get_cnt_of_pople_cafe_id(CAFES[cafes_count][0]),
                callback_data=CAFES[cafes_count]),
                InlineKeyboardButton(text=CAFES[cafes_count + 1][2:] + ' ' + db.get_cnt_of_pople_cafe_id(
                    CAFES[cafes_count + 1][0]), callback_data=CAFES[cafes_count + 1])])
            cafes_count += 2
        else:
            all_cafes.append([InlineKeyboardButton(
                text=CAFES[cafes_count][2:] + ' ' + db.get_cnt_of_pople_cafe_id(CAFES[cafes_count][0]),
                callback_data=CAFES[cafes_count])])
            cafes_count += 1

    return InlineKeyboardMarkup(inline_keyboard=all_cafes)


"""Клавиатура регистрации"""
reg_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Регистрация', callback_data='register')]], resize_keyboard=True)

"""Клавиатура для подтверждения"""
y_n_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='yes'),
     InlineKeyboardButton(text='Нет, я ошибся', callback_data='no')]
])

"""Клавиатура для админ-панели"""
admin_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👤 Данные сотрудника', callback_data='user_data'),
     InlineKeyboardButton(text='💬 Рассылка', callback_data='all_message')],
    [InlineKeyboardButton(text='✍ Создать БЗ', callback_data='make_a_chapter'),
     InlineKeyboardButton(text='📄 Список БЗ', callback_data='list_of_kd')],
    [InlineKeyboardButton(text='🔎 Поиск БЗ ️', callback_data='find_admin_kd')]])

"""Клавиатура для редактирования"""
edit_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🖊 Изменить текст', callback_data='edit_text'),
     InlineKeyboardButton(text='🖊 Изменить название', callback_data='edit_name')],
    [InlineKeyboardButton(text='🖊 Добавить файлы', callback_data='edit_file'),
     InlineKeyboardButton(text='❌ Удалить БЗ', callback_data='delete_kd')],
    [InlineKeyboardButton(text='⏪ Выйти', callback_data='exit')]
])

"""Клавиатура для выхода"""
exit_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⏪ Выйти', callback_data='exit')]
])
exit_user_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⏪ Выйти', callback_data='exit_user')]
])

"""Клавиатура для сотрудника"""
user_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔎 Поиск БЗ ️', callback_data='find_user_kd'),
     InlineKeyboardButton(text='📄 Список БЗ ️', callback_data='open_user_kd')],
    [InlineKeyboardButton(text='👨‍💻 Написать разработчику', callback_data='kick_me')]
])

"""Клавиатура для менеджера"""
user_manager_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔎 Поиск БЗ ️', callback_data='find_user_kd'),
     InlineKeyboardButton(text='📄 Список БЗ ️', callback_data='open_user_kd')],
    [InlineKeyboardButton(text="🛒 Закуп", callback_data="order"),
     InlineKeyboardButton(text='👨‍💻 Написать разработчику', callback_data='kick_me')]
])

"""Клавиатура для закупа"""
manager_order_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛒 Сделать закуп", callback_data="create_order"),
     InlineKeyboardButton(text="➕ Добавить позицию", callback_data="make_new_good")],
    [InlineKeyboardButton(text="❌ Удалить позицию", callback_data="delete_good")],
    [InlineKeyboardButton(text="⏪ Выйти", callback_data="exit_user")]

])
"""Клавиатура подтверждения редактирования"""
update_chapter_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Всё верно', callback_data='okey'),
     InlineKeyboardButton(text='Отменить', callback_data='not_okey')]
])

"""Клавиатура для данных пользователя"""
update_user_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🖊 Сменить должность', callback_data='change_job_id'),
     InlineKeyboardButton(text='🖊 Сменить заведение', callback_data='change_cafe_id')],
    [InlineKeyboardButton(text='❌ Удалить сотрудника', callback_data='delete_user')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='back')
        , InlineKeyboardButton(text='⏪ Выйти', callback_data='exit'),
     ]
])
