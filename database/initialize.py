import sqlite3
import logging

def create_db():
    with sqlite3.connect("sqlite3.db") as con:
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                group_id INTEGER
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        ''')

        """
            TODO:
            Добавить запросы на INSERT групп, если таковых нет, чтобы пробрасывать все группы ещё перед стартом работы бота
        """

class User:
    async def add(id: int):
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(f'''
                INSERT INTO users (account_id) VALUES ({id});
            ''')

    async def get(id: int):
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(f'''
                SELECT `id`, `account_id`, `group_id` from `users` where `account_id` = {id};
            ''')
    
    async def update(id: int, gr_id: int):
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(f'''
                UPDATE `users` SET `group_id` = {gr_id} WHERE `account_id` = {id} LIMIT 1;
            ''')

    async def delete(id: int):
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(f'''
                DELETE FROM `users` WHERE `account_id` = {id} LIMIT 1;
            ''')

    async def exists(id: int):
        # Пытаемся найти пользователя
        exists = await User.get(id)

        # Debug лог
        logging.debug(f'UserExists: User={id}, Exists={bool(exists)}')

        # Если не существует - добавляем
        if not bool(exists):
            await User.add(id)

        # Возврат ответа
        return exists

class Group:
    async def add(name: str):
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(f'''
                INSERT INTO groups (name) VALUES ({name});
            ''')

    async def get(name: str):
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(f'''
                SELECT `id` FROM `groups` WHERE name = {name};
            ''')
    
    async def update(name: str):
        pass # Парсинг всех групп со сайта novsu.ru
    

    async def delete(name: str):
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(f'''
                DELETE FROM `groups` WHERE `name` = {name} LIMIT 1;
            ''')
