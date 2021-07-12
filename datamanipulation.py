import sqlite3


class DataBase:
    def __init__(self):
        self.db = sqlite3.connect('famcs.db', check_same_thread=False)
        self.sql = self.db.cursor()
        self.sql.execute("""CREATE TABLE IF NOT EXISTS users (
                                                        id TEXT,
                                                        nickname TEXT,
                                                        score TEXT
                                                        )""")
        self.db.commit()

    def delete_user(self, user_id):
        self.sql.execute(f"DELETE FROM users WHERE id = '{user_id}'")
        self.db.commit()

    def add_user(self, user_id, nickname, score):
        self.sql.execute(f"SELECT id FROM users WHERE id = {user_id}")
        if self.sql.fetchone() is None:
            self.sql.execute(f"INSERT INTO users VALUES ('{user_id}', '{nickname}', '{score}')")
            self.db.commit()

    def get_user_score(self, user_id):
        self.sql.execute(f"SELECT id FROM users WHERE id = {user_id}")
        if self.sql.fetchone() is None:
            return None
        temps = self.sql.execute(f"SELECT score FROM users WHERE id = '{user_id}'").fetchone()
        self.db.commit()
        return temps[0]
