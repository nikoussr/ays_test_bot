from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from configs import JOBS, CAFES
from app.database.bd import Database

db = Database('../data/ays_test_database.db')

"""Клавиатура для работ"""


def create_job_btns(cafe_id):
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


def create_job_id_btns():
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


def create_cafe_id_btns():
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


def create_cafe_id_btns_mes():
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

    return InlineKeyboardMarkup(inline_keyboard=all_cafes)


"""Клавиатура для баз знаний"""


def make_kd_kb(job_id):
    all_bases = []
    kds = []
    all_kds = (db.get_all_kd_j(job_id))
    for kd in all_kds:
        if kd[0] is not None:
            kds.append(str(kd[1]) + kd[0])
            all_bases.append([InlineKeyboardButton(text=kd[0], callback_data=str(kd[1]) + '_' + kd[0])])
    # all_bases.append([InlineKeyboardButton(text='↩️', callback_data='back')])
    return InlineKeyboardMarkup(inline_keyboard=all_bases), kds


def make_kd_kb1(job_id, cafe_id, folder_id):
    all_bases = []
    kds = []
    all_kds = db.get_all_kd(job_id, cafe_id,folder_id)
    print(all_kds)
    for kd in all_kds:
        if kd[0] is not None:
            kds.append(str(kd[1]) + kd[0][:30])
            all_bases.append([InlineKeyboardButton(text=kd[0], callback_data=str(kd[1]) + '_' + kd[0][:30])])
    # all_bases.append([InlineKeyboardButton(text='↩️', callback_data='back')])
    return InlineKeyboardMarkup(inline_keyboard=all_bases), kds


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
     InlineKeyboardButton(text='💬 Рассылка', callback_data='all_message')], [InlineKeyboardButton(text='✍ Создать БЗ', callback_data='make_a_chapter'),
                                                                           InlineKeyboardButton(text='📄 Список БЗ', callback_data='list_of_kd')]])

"""Клавиатура для выхода"""
exit_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выйти', callback_data='exit')]
])
"""Клавиатура для выхода"""
edit_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🖊 Изменить текст', callback_data='edit_text'),
     InlineKeyboardButton(text='🖊 Изменить название', callback_data='edit_name')],
    [InlineKeyboardButton(text='🖊 Добавить фотографии', callback_data='edit_photo'),
     InlineKeyboardButton(text='❌ Удалить БЗ', callback_data='delete_kd')],
    [InlineKeyboardButton(text='⏪ Выйти', callback_data='exit')]
])

"""Клавиатура для назад"""
back_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад ↩️', callback_data='back')]
])

"""Клавиатура для БЗ"""
user_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='БЗ ️', callback_data='open_user_kd'),
     InlineKeyboardButton(text='Пнуть разработчика', callback_data='kick_me')]
])

"""Клавиатура для БЗ"""
user_manager_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='БЗ ️', callback_data='open_user_kd'),
     InlineKeyboardButton(text="Закуп", callback_data="order")],
    [InlineKeyboardButton(text='Написать разработчику', callback_data='kick_me')]
])

manager_order_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сделать закуп", callback_data="create_order"),
     InlineKeyboardButton(text="Редактировать позиции", callback_data="make_new_good")]
])

update_chapter_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Всё верно', callback_data='okey'),
     InlineKeyboardButton(text='Отменить', callback_data='not_okey')]
])


def create_folders_btn(all_folders):
    folders = []
    folders_count = 0
    if len(all_folders) == 0:
        folders.append([InlineKeyboardButton(text="➕ Создать новую папку", callback_data='new_folder')])

        return InlineKeyboardMarkup(inline_keyboard=folders)
    else:
        while folders_count < len(all_folders):
            if len(all_folders) - folders_count >= 2:
                folders.append([InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count][1]), callback_data=str(all_folders[folders_count][0]) + '_' + str(all_folders[folders_count][1])),
                                InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count + 1][1]),
                                                     callback_data=str(all_folders[folders_count + 1][0]) +'_' + str(all_folders[folders_count + 1][1]))])
                folders_count += 2
            else:
                folders.append([InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count][1]), callback_data=str(all_folders[folders_count][0]) + '_' + str(all_folders[folders_count][1]))])
                folders_count += 1
        folders.append([InlineKeyboardButton(text="➕ Создать новую папку", callback_data='new_folder')])

        return InlineKeyboardMarkup(inline_keyboard=folders)

def create_folders_btn_look(all_folders):
    folders = []
    folders_count = 0
    if len(all_folders) == 0:
        return InlineKeyboardMarkup(inline_keyboard=folders)
    else:
        while folders_count < len(all_folders):
            if len(all_folders) - folders_count >= 2:
                folders.append([InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count][1]), callback_data=str(all_folders[folders_count][0]) + '_' + str(all_folders[folders_count][1])),
                                InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count + 1][1]),
                                                     callback_data=str(all_folders[folders_count + 1][0]) +'_' + str(all_folders[folders_count + 1][1]))])
                folders_count += 2
            else:
                folders.append([InlineKeyboardButton(text="🗂 " + str(all_folders[folders_count][1]), callback_data=str(all_folders[folders_count][0]) + '_' + str(all_folders[folders_count][1]))])
                folders_count += 1
        return InlineKeyboardMarkup(inline_keyboard=folders)
def create_goods_btns(short_name, art, cafe_id):
    pages = len(art) // 10 + 1
    goods = []
    if pages > 1:
        goods.append(
            [InlineKeyboardButton(text="⛔", callback_data='⛔'), InlineKeyboardButton(text='1', callback_data="⛔"),
             InlineKeyboardButton(text=">>", callback_data="next_page")])
        index = 0
        while index < 10:
            goods.append(
                [InlineKeyboardButton(text=short_name[index][0], callback_data=str(cafe_id) + str(art[index][0]))])
            index += 1
    else:
        index = 0
        while index < len(art):
            goods.append(
                [InlineKeyboardButton(text=short_name[index][0], callback_data=str(cafe_id) + str(art[index][0]))])
            index += 1
    goods.append([InlineKeyboardButton(text="Готово", callback_data="ready")])
    return InlineKeyboardMarkup(inline_keyboard=goods)


def update_goods_btns(short_name, art, cafe_id, page):
    goods = []
    if (len(art) // 10 + 1 - page) == 0 and page > 1:
        goods.append([InlineKeyboardButton(text="<<", callback_data='prev_page'), InlineKeyboardButton(text=str(page), callback_data="⛔"),
             InlineKeyboardButton(text="⛔", callback_data="⛔")])
        short_name = short_name[(page - 1) * 9 + 1:page * 10]
        art = art[(page - 1) * 9 + 1:page * 10]
        index = 0
        while index < len(art):
            goods.append(
                [InlineKeyboardButton(text=short_name[index][0], callback_data=str(cafe_id) + str(art[index][0]))])
            index += 1
    elif page == 1:
        goods.append(
            [InlineKeyboardButton(text="⛔", callback_data='⛔'), InlineKeyboardButton(text=str(page), callback_data="⛔"),
             InlineKeyboardButton(text=">>", callback_data="next_page")])
        short_name = short_name[:page * 10]
        art = art[:page * 10]
        index = 0
        while index < len(art):
            goods.append(
                [InlineKeyboardButton(text=short_name[index][0], callback_data=str(cafe_id) + str(art[index][0]))])
            index += 1
    else:
        print("тут")
        goods.append(
            [InlineKeyboardButton(text="<<", callback_data='prev_page'), InlineKeyboardButton(text=str(page), callback_data="⛔"),
             InlineKeyboardButton(text=">>", callback_data="next_page")])
        short_name = short_name[(page - 1) * 9 + 1:page * 10]
        art = art[(page - 1) * 9 + 1:page * 10]
        index = 0
        while index < len(art):
            goods.append(
                [InlineKeyboardButton(text=short_name[index][0], callback_data=str(cafe_id) + str(art[index][0]))])
            index += 1
        print('Здесь')
    print('тутааа')
    goods.append([InlineKeyboardButton(text="Готово", callback_data="ready")])
    return InlineKeyboardMarkup(inline_keyboard=goods)


