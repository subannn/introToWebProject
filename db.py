import sqlite3
import os

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    short TEXT UNIQUE,
                    original TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT UNIQUE,
                    password TEXT NOT NULL
                )
            ''')

    def save_short_long_urls(self, short, original):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO urls (short, original) VALUES (?, ?)',
                (short, original)
            )
            conn.commit()

    def get_long_url(self, short):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'select urls.original from urls where short = ?',
                (short,)
            )
            result = cursor.fetchone()
            return result[0] if result else None

    def user_exists(self, user_name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT user_name FROM users WHERE user_name = ?',
                (user_name,)
            )
            result = cursor.fetchone()

            if result is None:
                return False
            return True

    def save_user(self, user_name, password):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (user_name, password) VALUES (?, ?)',
                (user_name, password)
            )
            conn.commit()

    def check_user_and_password(self, user_name, password):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'select * from users where user_name = ? and password = ?',
                (user_name, password)
            )
            result = cursor.fetchone()
            return True if result else False

    # def get_user_id(self, user_name):
    #     with sqlite3.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(
    #             'select * from users where user_name = ?,
    #             (user_name)
    #         )
    #         result = cursor.fetchone()
    #         return True if result else False

