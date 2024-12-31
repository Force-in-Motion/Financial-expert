import sqlite3
from service.service_data import SaveLoadData as sld



class Users:
    def __init__(self):
        self.__connect = sqlite3.connect(sld.get_db_path())
        self.__cursor = self.__connect.cursor()
        self.__create_table_users()


    def __create_table_users(self):

        self.__cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
            )
            """)

    def add_user(self, value) -> None:

        self.__cursor.execute(
            'INSERT INTO Users (user_id, username, password) VALUES (?, ?, ?)',
            (value.get('user_id'), value.get('username'), value.get('password'))
        )

        self.__connect.commit()


    def authorization_user(self, value) -> bool:

        self.__cursor.execute(
            'SELECT username, password, user_id FROM Users WHERE username = ? AND password = ? AND user_id = ?',
            (value.get('username'), value.get('password'), value.get('user_id'))
        )

        result = self.__cursor.fetchone()

        if result:

            return True

        return False


    def get_user_name(self, user_name, user_id) -> bool:

        self.__cursor.execute(
            'SELECT username FROM Users WHERE username = ? AND user_id = ?',
            (user_name, user_id)
        )

        result = self.__cursor.fetchone()

        if result:

            return True

        return False


    def get_user_password(self, password, user_id) -> bool:

        self.__cursor.execute(
            'SELECT password FROM Users WHERE password = ? AND user_id = ?',
            (password, user_id)
        )

        result = self.__cursor.fetchone()

        if result:

            return True

        return False


    def edit_user_name(self, value) -> None:

        self.__cursor.execute(
            'UPDATE Users SET username = ? WHERE username = ? AND user_id = ?',
            (value.get('newname'), value.get('oldname'), value.get('user_id'))
        )

        self.__connect.commit()


    def edit_user_password(self, value) -> None:

        self.__cursor.execute(
            'UPDATE Users SET password = ? WHERE password = ? AND user_id = ?',
            (value.get('newpassword'), value.get('oldpassword'), value.get('user_id'))
        )

        self.__connect.commit()


    def del_user(self, value) -> None:

        self.__cursor.execute('DELETE FROM Users WHERE username = ? AND user_id = ?',
                              (value.get('username'), value.get('user_id'),))

        self.__connect.commit()
