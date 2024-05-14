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

    def set_last_name(self, user_id, last_name):
        """Добавляет в БД last_name для user_id"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET last_name =? WHERE user_id =?", (last_name, user_id,))

    def set_phone_number(self, user_id, phone_number):
        """Добавляет в БД phone_number для user_id"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET phone_number =? WHERE user_id =?", (phone_number, user_id,))

    def set_job_id(self, user_id, job_id):
        """Добавляет в БД job_id для user_id"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET job_id =? WHERE user_id =?", (job_id, user_id,))

    def set_cafe_id(self, user_id, cafe_id):
        """Добавляет в БД cafe_id для user_id"""
        with self.connection:
            return self.cursor.execute("UPDATE users SET cafe_id =? WHERE user_id =?", (cafe_id, user_id,))

    def set_kd_name(self, base_id, kd_name):
        """Добавляет в БД kd_name в kd"""
        with self.connection:
            return self.cursor.execute("UPDATE kd SET kd_name=? WHERE base_id =? ", (kd_name, base_id,))

    def set_kd_job_id(self, job_id, base_id):
        """Добавляет в БД job_id в kd"""
        with self.connection:
            return self.cursor.execute("UPDATE kd SET job_id=? WHERE base_id =?", (job_id,base_id,))

    def set_kd_cafe_id(self, cafe_id):
        """Добавляет в БД job_id в kd"""
        with self.connection:
            return self.cursor.execute("INSERT INTO kd (cafe_id) VALUES (?)", (cafe_id,))

    def set_kd_text(self, base_id, kd_text):
        """Добавляет в БД kd_name в kd"""
        with self.connection:
            return self.cursor.execute("UPDATE kd SET KD_text=? WHERE base_id =? ", (kd_text, base_id,))

    def get_base_id(self):
        """Берет из БД first_name у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT MAX(base_id) FROM kd").fetchall()[0][0]

    def get_first_name(self, user_id):
        """Берет из БД first_name у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT first_name FROM users WHERE user_id=?", (user_id,)).fetchall()[0][0]

    def get_last_name(self, user_id):
        """Берет из БД last_name у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT last_name FROM users WHERE user_id=?", (user_id,)).fetchall()[0][0]

    def get_phone_number(self, user_id):
        """Берет из БД phone_number у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT phone_number FROM users WHERE user_id=?", (user_id,)).fetchall()[0][0]

    def get_job_id(self, user_id):
        """Берет из БД job_id у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT job_id FROM users WHERE user_id=?", (user_id,)).fetchall()[0][0]

    def get_cafe_id(self, user_id):
        """Берет из БД cafe_id у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT cafe_id FROM users WHERE user_id=?", (user_id,)).fetchall()[0][0]

    def get_all_ids(self):
        """Берет из БД все user_id"""
        with self.connection:
            self.cursor.execute("SELECT user_id from users")
            result = self.cursor.fetchall()
            print(result)
            return result

    def get_all_ids_cafe(self, cafe_id):
        """Берет из БД все user_id"""
        with self.connection:
            self.cursor.execute("SELECT user_id from users WHERE cafe_id=?", (cafe_id,))
            result = self.cursor.fetchall()
            print(result)
            return result

    def get_all_kd(self, job_id, cafe_id):
        """Берет из БД все БЗ для job_id"""
        with self.connection:
            self.cursor.execute("SELECT KD_name, base_id from kd WHERE job_id =? and cafe_id =?", (job_id, cafe_id))
            result = self.cursor.fetchall()
            return result

    def get_all_kd_j(self, job_id):
        """Берет из БД все БЗ для job_id"""
        with self.connection:
            self.cursor.execute("SELECT KD_name, base_id from kd WHERE job_id =?", (job_id,))
            result = self.cursor.fetchall()
            return result

    def get_text_of_kd(self, base_id):
        with self.connection:
            self.cursor.execute("SELECT KD_text from kd WHERE  base_id=?", (base_id,))
            result = self.cursor.fetchall()[0][0]
            return result

    def get_all_info(self, user_id):
        """Пусть пока будет"""
        with self.connection:
            self.cursor.execute(
                "SELECT first_name, last_name, phone_number, job_name, cafe_name FROM users LEFT JOIN job_titles ON users.job_id = job_titles.job_id FULL JOIN cafes ON users.cafe_id = cafes.cafe_id WHERE user_id = ?",
                (user_id,))
            result = self.cursor.fetchall()
            print(result)
            return result

    def get_user(self, first_name, last_name):
        """Берет из БД всю информацию по ФИ"""
        with self.connection:
            self.cursor.execute(
                "SELECT id, user_id, first_name, last_name, phone_number, job_name, cafe_name FROM users LEFT JOIN job_titles ON users.job_id = job_titles.job_id FULL JOIN cafes ON users.cafe_id = cafes.cafe_id WHERE first_name =? AND last_name =?",
                (first_name, last_name,))
            result = self.cursor.fetchall()[0]
            print(result)
            return result

    def set_kd_photo(self, base_id, photo):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO kd_photos (base_id, photo) VALUES (?, ?)", (base_id, photo)
            )


    """Folders"""

    def set_folder_name(self, folder_name):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO folders (folder_name) VALUES (?)", (folder_name,)
            )

    def kd_create(self):
        with self.connection:
            return self.connection.execute(
                "INSERT INTO kd DEFAULT VALUES"
            )
    def set_kd(self, cafe_id, job_id, kd_name, folder_id, kd_text):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO kd (cafe_id, job_id, kd_name, kd_text, folder_id) VALUES (?, ?, ?, ?, ?)", (cafe_id, job_id, kd_name, kd_text, folder_id,)
            )
    def set_kd_folder_id(self, base_id):
        with self.connection:
            return self.cursor.execute(
                "UPDATE kd SET folder_id=? WHERE base_id =?", (base_id, )
            )

    def get_folder_name(self, folder_id):
        return self.cursor.execute(
            "SELECT folder_name FROM folders WHERE folders_id =?", (folder_id,)
        ).fetchall()[0]


    def get_kd_folder_id(self, cafe_id, job_id):
        with self.connection:
            result =  self.cursor.execute(
                "SELECT folder_id FROM kd WHERE job_id =? AND cafe_id =?", (job_id, cafe_id, )
            ).fetchall()
            print(result)
            return result

    def get_folder_id(self):
        """Берет из БД first_name у user_id"""
        with self.connection:
            return self.cursor.execute("SELECT MAX(folder_id) FROM folders").fetchall()[0][0]

    def get_folders(self, cafe_id, job_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT DISTINCT t1.folder_id, t2.folder_name FROM kd t1 JOIN folders t2 ON t1.folder_id = t2.folder_id WHERE t1.cafe_id = ? AND t1.job_id = ?", (cafe_id, job_id,)
            ).fetchall()
            print(result)
            return result

    def get_kd_photos(self, base_id):
        with self.connection:
            self.cursor.execute(
                "SELECT photo FROM kd_photos WHERE base_id =?", (base_id, )
            )
            result = self.cursor.fetchall()
            print(result)
            return result
    def delete_unkd(self):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM kd_photos WHERE base_id NOT IN (SELECT base_id FROM kd)"
            )

    def delete_kd(self, base_id):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM kd WHERE base_id=?", (base_id,)
            )

    def delete_kd_photo(self, base_id):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM kd_photos WHERE base_id=?", (base_id,)
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



    """goods"""


    def set_good_art(self, art):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO goods (art) VALUES (?)", (art,)
            )

    def set_good_cafe_id(self, art, cafe_id):
        with self.connection:
            return self.cursor.execute(
                "UPDATE goods SET cafe_id=? WHERE art =?", (cafe_id, art)
            )

    def set_good_full_name(self, art, full_name):
        with self.connection:
            return self.cursor.execute(
                "UPDATE goods SET full_name=? WHERE art =?", (full_name, art)
            )

    def set_good_short_name(self, art, short_name):
        with self.connection:
            return self.cursor.execute(
                "UPDATE goods SET short_name=? WHERE art =?", (short_name, art)
            )

    def set_good_unit(self, art, unit):
        with self.connection:
            return self.cursor.execute(
                "UPDATE goods SET unit=? WHERE art =?", (unit, art)
            )

    def get_good_art(self, art):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO goods (art) VALUES (?)", (art,)
            ).fetchall()



    def get_good_full_name(self, art, cafe_id):
        with self.connection:
            return self.cursor.execute(
                "SELECT full_name from goods WHERE  art=? and cafe_id=?" , (art, cafe_id,)
            ).fetchall()[0][0]

    def get_good_short_name(self, art, cafe_id):
        with self.connection:
            return self.cursor.execute(
                "SELECT short_name from goods WHERE  art=? and cafe_id=?" , (art, cafe_id,)
            ).fetchall()

    def get_good_unit(self, art, cafe_id):
        with self.connection:
            return self.cursor.execute(
                "SELECT unit from goods WHERE  art=? and cafe_id=?" ,(art, cafe_id,)

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