import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    """Регистрация"""

    def add_user(self, user_id):
        """Добавляет в БД только user_id в users"""
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        """Проверяет на наличие в БД полльзователя с данным user_id"""
        with self.connection:
            self.cursor.execute(
                "SELECT first_name, last_name, phone_number, job_name, cafe_name FROM users LEFT JOIN job_titles ON users.job_id = job_titles.job_id FULL JOIN cafes ON users.cafe_id = cafes.cafe_id WHERE user_id = ?",
                (user_id,))
            result = self.cursor.fetchall()
            return bool(len(result))

    def set_first_name(self, user_id, first_name):
        """Добавляет в БД first_name для user_id"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET first_name =? WHERE user_id =?", (first_name, user_id,))
    def get_first_name(self, user_id):
        """Берет из БД first_name у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT first_name FROM users WHERE user_id=?", (user_id,)).fetchall()[0][0]

    def set_last_name(self, user_id, last_name):
        """Добавляет в БД last_name для user_id"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET last_name =? WHERE user_id =?", (last_name, user_id,))

    def get_last_name(self, user_id):
        """Берет из БД last_name у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT last_name FROM users WHERE user_id=?", (user_id,)).fetchall()[0][0]

    def set_phone_number(self, user_id, phone_number):
        """Добавляет в БД phone_number для user_id"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET phone_number =? WHERE user_id =?", (phone_number, user_id,))

    def get_phone_number(self, user_id):
        """Берет из БД phone_number у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT phone_number FROM users WHERE user_id=?", (user_id,)).fetchall()[0][0]

    def set_date_of_birth(self, user_id, date_of_birth):
        """Добавляет в БД date_of_birth для user_id"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET date_of_birth =? WHERE user_id =?", (date_of_birth, user_id,))

    def get_date_of_birth(self, user_id):
        """Добавляет в БД date_of_birth для user_id"""
        with self.connection:
            return self.cursor.execute("SELECT date_of_birth FROM users WHERE user_id=?", (user_id,)).fetchall()[0][0]

    def get_date_of_birth_cafe(self, cafe_id):
        """Добавляет в БД date_of_birth для user_id"""
        with self.connection:
            return self.cursor.execute("SELECT first_name, last_name, date_of_birth FROM users WHERE cafe_id=?", (cafe_id,)).fetchall()

    def set_job_id(self, user_id, job_id):
        """Добавляет в БД job_id для user_id"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET job_id =? WHERE user_id =?", (job_id, user_id,))

    def get_job_id(self, user_id):
        """Берет из БД job_id у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT job_id FROM users WHERE user_id=?", (user_id,)).fetchall()[0][0]

    def set_cafe_id(self, user_id, cafe_id):
        """Добавляет в БД cafe_id для user_id"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET cafe_id =? WHERE user_id =?", (cafe_id, user_id,))

    def get_cafe_id(self, user_id):
        """Берет из БД cafe_id у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT cafe_id FROM users WHERE user_id=?", (user_id,)).fetchall()[0][0]

    def get_people(self, cafe_id):
        """Берет из БД last_name, first_name, user_id, job_id через cafe_id"""
        with self.connection:
            return self.cursor.execute(
                "SELECT last_name, first_name, user_id, job_id FROM users WHERE cafe_id=? ORDER BY job_id, last_name",
                (cafe_id,)).fetchall()

    def get_all_info(self, user_id):
        """Пусть пока будет"""
        with self.connection:
            self.cursor.execute(
                "SELECT first_name, last_name, phone_number, date_of_birth, job_name, cafe_name FROM users LEFT JOIN job_titles ON users.job_id = job_titles.job_id FULL JOIN cafes ON users.cafe_id = cafes.cafe_id WHERE user_id = ?",
                (user_id,))
            result = self.cursor.fetchall()
            return result

    def get_user(self, user_id):
        """Берет из БД всю информацию по ФИ"""
        with self.connection:
            self.cursor.execute(
                "SELECT id, user_id, last_name, first_name, date_of_birth, phone_number, job_name, cafe_name, date_of_reg FROM users LEFT JOIN job_titles ON users.job_id = job_titles.job_id FULL JOIN cafes ON users.cafe_id = cafes.cafe_id WHERE user_id =?",
                (user_id,))
            result = self.cursor.fetchall()[0]
            print(result)
            return result

    """Для БЗ"""

    def set_kd_name(self, base_id, kd_name):
        """Редактирует в БД kd_name в kd"""
        with self.connection:
            return self.cursor.execute("UPDATE kd SET kd_name=? WHERE base_id =? ", (kd_name, base_id,))

    def set_kd_text(self, base_id, kd_text):
        """Редактирует в БД kd_text в kd"""
        with self.connection:
            return self.cursor.execute("UPDATE kd SET KD_text=? WHERE base_id =? ", (kd_text, base_id,))

    def get_kd_text(self, base_id):
        with self.connection:
            self.cursor.execute("SELECT KD_text from kd WHERE  base_id=?", (base_id,))
            result = self.cursor.fetchall()[0][0]
            return result

    def get_kd_name(self, base_id):
        with self.connection:
            self.cursor.execute("SELECT KD_name from kd WHERE  base_id=?", (base_id,))
            result = self.cursor.fetchall()[0][0]
            return result

    def get_base_id(self):
        """Берет из БД максимальный индекс base_id из kd"""
        with self.connection:
            return self.cursor.execute("SELECT MAX(base_id) FROM kd").fetchall()[0][0]

    def get_all_ids(self):
        """Берет из БД все user_id"""
        with self.connection:
            self.cursor.execute("SELECT user_id from users")
            result = self.cursor.fetchall()
            return result

    def get_all_ids_cafe(self, cafe_id):
        """Берет из БД все user_id"""
        with self.connection:
            self.cursor.execute("SELECT user_id from users WHERE cafe_id=?", (cafe_id,))
            result = self.cursor.fetchall()
            return result

    def get_all_kd(self, job_id, cafe_id, folder_id):
        """Берет из БД все БЗ для job_id"""
        with self.connection:
            if folder_id == 0:
                self.cursor.execute("SELECT KD_name, base_id from kd WHERE job_id =? and cafe_id =?",
                                    (job_id, cafe_id))
            else:
                self.cursor.execute("SELECT KD_name, base_id from kd WHERE job_id =? and cafe_id =? AND folder_id = ?",
                                    (job_id, cafe_id, folder_id))
            result = self.cursor.fetchall()
            return result

    def get_all_kd_j(self, job_id):
        """Берет из БД все БЗ для job_id"""
        with self.connection:
            self.cursor.execute("SELECT KD_name, base_id from kd WHERE job_id =?", (job_id,))
            result = self.cursor.fetchall()
            return result

    def get_all_kd_base(self):
        """Берет из БД все БЗ для job_id"""
        with self.connection:
            self.cursor.execute("SELECT KD_name, base_id from kd")
            result = self.cursor.fetchall()
            return result

    def set_kd_file(self, base_id, file):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO kd_files (base_id, file, file_type) VALUES (?, ?, ?)", (base_id, file[0], file[1])
            )

    """Folders"""

    def set_folder_name(self, folder_name):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO folders (folder_name) VALUES (?)", (folder_name,)
            )


    def set_kd(self, cafe_id, job_id, kd_name, folder_id, kd_text):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO kd (cafe_id, job_id, kd_name, kd_text, folder_id) VALUES (?, ?, ?, ?, ?)",
                (cafe_id, job_id, kd_name, kd_text, folder_id,)
            )


    def get_folder_id(self):
        """Берет из БД first_name у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT MAX(folder_id) FROM folders").fetchall()[0][0]

    def get_folders(self, cafe_id, job_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT DISTINCT t1.folder_id, t2.folder_name FROM kd t1 JOIN folders t2 ON t1.folder_id = t2.folder_id WHERE t1.cafe_id = ? AND t1.job_id = ?",
                (cafe_id, job_id,)
            ).fetchall()
            return result

    def get_kd_files(self, base_id):
        with self.connection:
            self.cursor.execute(
                "SELECT file, file_type FROM kd_files WHERE base_id =?", (base_id,)
            )
            result = self.cursor.fetchall()
            return result

    def delete_unkd(self):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM kd_files WHERE base_id NOT IN (SELECT base_id FROM kd)"
            )

    def delete_kd(self, base_id):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM kd WHERE base_id=?", (base_id,)
            )

    def delete_kd_file(self, base_id):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM kd_files WHERE base_id=?", (base_id,)
            )

    def get_cnt_of_kd_job_id(self, job_id, cafe_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT COUNT(*) FROM kd where job_id =? and cafe_id =?", (job_id, cafe_id)
            )
            result = (result.fetchall()[0][0])
            return str(result)

    def get_cnt_of_kd_cafe_id(self, cafe_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT COUNT(*) FROM kd where cafe_id =?", (cafe_id)
            )
            result = (result.fetchall()[0][0])
            return str(result)

    def get_cnt_of_pople_cafe_id(self, cafe_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT COUNT(*) FROM users where cafe_id =?", (cafe_id)
            )
            result = (result.fetchall()[0][0])
            return str(result)

    """goods"""

    def get_good_full_name(self, id):
        with self.connection:
            return self.cursor.execute(
                "SELECT full_name from goods WHERE id=?", (id,)
            ).fetchall()[0][0]

    def get_good_art(self,id):
        with self.connection:
            return self.cursor.execute(
                "SELECT art from goods WHERE  id=?", (id,)
            ).fetchall()[0][0]

    def get_good_short_name(self, id):
        with self.connection:
            return self.cursor.execute(
                "SELECT short_name from goods WHERE  id=?", (id,)
            ).fetchall()[0][0]

    def get_good_unit(self, id):
        with self.connection:
            return self.cursor.execute(
                "SELECT unit from goods WHERE  id=?", (id,)

            ).fetchall()[0][0]

    def get_all_goods_short_name(self, cafe_id):
        with self.connection:
            return self.cursor.execute(
                "SELECT short_name FROM goods WHERE cafe_id =?", (cafe_id,)
            ).fetchall()

    def get_all_goods_art(self, cafe_id):
        with self.connection:
            return self.cursor.execute(
                "SELECT art FROM goods WHERE cafe_id =?", (cafe_id,)
            ).fetchall()

    def insert_good(self, full_name, art, short_name, unit, cafe_id):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO goods (full_name, art, short_name, unit, cafe_id) VALUES (?, ?, ?, ?, ?)", (full_name, art, short_name, unit, cafe_id, )
            )

    def delete_good(self, id):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM goods WHERE id=?", (id,)
            )

    def get_all_goods_ids(self, cafe_id):
        with self.connection:
            return self.cursor.execute(
                "SELECT id FROM goods WHERE cafe_id =?", (cafe_id,)
            ).fetchall()
    """Бан лист"""

    def delete_user(self, user_id):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM users WHERE user_id=?", (user_id,))
    def set_banned_user(self, user_id):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO banned (user_id) VALUES (?)", (user_id,))
    def get_banned_users(self):
        with self.connection:
            return self.cursor.execute(
                "SELECT user_id FROM banned").fetchall()


    """Хочу.."""
    def set_want(self, cafe_id, want_text, user_id):
        with self.connection:
            return self.connection.execute(
                "INSERT INTO wants (cafe_id, want_text, user_id) VALUES (?,?, ?)", (cafe_id, want_text, user_id)
            )

    def get_all_wants(self):
        with self.connection:
            return self.cursor.execute(
                "SELECT id, cafe_name, want_text, date, is_answered, user_id FROM wants LEFT JOIN cafes ON wants.cafe_id = cafes.cafe_id WHERE is_answered = ?", (0,)
            ).fetchall()
    def get_want_id(self):
        with self.connection:
            return self.cursor.execute(
                "SELECT MAX(id) FROM wants"
            ).fetchall()[0][0]

    def get_want_user_id(self, want_id):
        with self.connection:
            return self.cursor.execute(
                "SELECT user_id FROM wants WHERE id = ?", (want_id,)).fetchall()[0][0]

    def get_want_text(self, want_id):
        with self.connection:
            return self.cursor.execute(
                "SELECT want_text FROM wants WHERE id = ?", (want_id,)).fetchall()[0][0]

    def set_wants_is_answered(self, want_id):
        with self.connection:
            return self.cursor.execute(
                "UPDATE wants SET is_answered = ? WHERE id = ?", (1, want_id,)
            )
    def get_want_date(self, want_id):
        with self.connection:
            return self.cursor.execute(
                "SELECT date FROM wants WHERE id = ?", (want_id,)).fetchall()[0][0]

