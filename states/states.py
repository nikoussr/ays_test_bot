from aiogram.filters.state import StatesGroup, State


class register(StatesGroup):
    wait_first_name = State()
    wait_last_name = State()
    wait_phone_number = State()
    wait_date_of_birth = State()
    wait_job_id = State()
    wait_cafe_id = State()
    wait_yes_no = State()
    wait_yes = State()
    wait_no = State()

class admin(StatesGroup):
    wait_admin = State()
    wait_user_FL = State()
    wait_user_info = State()
    wait_for_user_update = State()
    wait_for_change_cafe_id = State()
    wait_for_change_job_id = State()
    wait_for_delete_user = State()



    wait_all_message = State()
    wait_for_find_kd = State()
    wait_for_chapter = State()
    wait_for_job_id_1 = State()
    wait_for_job_id_2 = State()
    wait_for_job_id_3 = State()
    wait_for_folder_name = State()
    wait_for_folder = State()
    wait_for_chapter_name = State()
    wait_for_chapter_text = State()
    wait_yes_no = State()
    wait_for_click_kd_1 = State()
    wait_for_click_kd_2 = State()
    wait_for_click_kd_3= State()
    wait_for_click_kd_4 = State()
    wait_for_click_kd_5 = State()

    wait_for_exit = State()
    wait_for_check_1 = State()
    wait_for_check_2 = State()
    wait_for_check_3 = State()
    wait_for_check_4 = State()
    wait_for_edit_text = State()
    wait_for_edit_name = State()
    wait_for_delete = State()
    wait_for_cafe_id = State()
    wait_for_cafe_mes = State()
    wait_for_edit_file = State()

class user(StatesGroup):
    wait_user = State()
    wait_for_click_folder = State()
    wait_for_click_kd = State()
    wait_for_exit = State()
    wait_for_exit_del = State()
    wait_for_user_message = State()
    wait_for_find_kd = State()
    wait_for_back_exit = State()
    """Закуп"""
    wait_for_action = State()
    wait_for_create_good = State()
    wait_for_delete_good = State()
    wait_for_good_count = State()
    wait_for_confirm_delete = State()
    wait_for_create_order = State()
    wait_for_print_order = State()
    """Хочу.."""
    wait_for_want_to = State()
