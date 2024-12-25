import sqlite3
from datetime import datetime
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
            'SELECT username, password FROM Users WHERE username = ? AND password = ?',
            (value.get('username'), value.get('password'))
        )

        result = self.__cursor.fetchone()

        if result:
            return True
        return False


    def edit_user_name(self, value) -> None:

        self.__cursor.execute(
            'UPDATE Users SET username = ? WHERE user_id = ?',
            (value.get('username'), value.get('user_id'))
        )

        self.__connect.commit()


    def edit_user_password(self, value) -> None:

        self.__cursor.execute(
            'UPDATE Users SET password = ? WHERE user_id = ?',
            (value.get('password'), value.get('user_id'))
        )

        self.__connect.commit()


    def del_user(self, value) -> None:

        self.__cursor.execute('DELETE FROM Users WHERE user_id = ?', (value.get('user_id'),))

        self.__connect.commit()




class Income:
    def __init__(self):
        self.__connect = sqlite3.connect(sld.get_db_path())
        self.__cursor = self.__connect.cursor()
        self.__create_table_income()


    def __create_table_income(self) -> None:

        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS Income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        quantity INTEGER  NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)

        self.__connect.commit()


    def add_income(self, value) -> None:

        current_date = datetime.now().strftime('%Y-%m-%d')

        self.__cursor.execute(
        'INSERT INTO Income (quantity, category, date) VALUES (?, ?, ?)',
        (value.get('quantity'), value.get('category'), current_date)
        )

        self.__connect.commit()



class Expense:
    def __init__(self):
        self.__connect = sqlite3.connect(sld.get_db_path())
        self.__cursor = self.__connect.cursor()
        self.__create_table_expense()


    def __create_table_expense(self) -> None:

        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS Expense (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        quantity INTEGER  NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
        )
        """)

        self.__connect.commit()


    def add_expense(self, value) -> None:

        current_date = datetime.now().strftime('%Y-%m-%d')

        self.__cursor.execute(
        'INSERT INTO Expense (quantity, category, date) VALUES (?, ?, ?)',
  (value.get('quantity'), value.get('category'), current_date)
        )

        self.__connect.commit()




class Goal:
    def __init__(self):
        self.__connect = sqlite3.connect(sld.get_db_path())
        self.__cursor = self.__connect.cursor()
        self.__create_table_goal()
        self.__create_table_completed_goal()

    def __create_table_completed_goal(self) -> None:

        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS Completed_Goal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        required INTEGER NOT NULL,
        deposit INTEGER,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
        )
        """)


    def __create_table_goal(self) -> None:

        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS Goal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        required INTEGER NOT NULL,
        deposit INTEGER DEFAULT 0,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
        )
        """)

    def add_goal(self, value) -> None:

        current_date = datetime.now().strftime('%Y-%m-%d')

        self.__cursor.execute(
            'INSERT INTO Goal (description, required, date) VALUES (?, ?, ?)',
            (value.get('description'), value.get('required'), current_date)
        )

        self.__connect.commit()


    def add_deposit(self, value) -> None:

        self.__cursor.execute('SELECT deposit FROM Goal WHERE description = ?',
                              (value.get('description'),))
        result = self.__cursor.fetchone()

        new_deposit = result[0] + int(value.get('deposit'))

        self.__cursor.execute(
            'UPDATE Goal SET deposit = ? WHERE description = ?',
            (new_deposit, value.get('description')))

        self.__connect.commit()


    def del_goal(self, value) -> None:

        self.__cursor.execute('DELETE FROM Goal WHERE description = ?', (value.get('description'),))

        self.__connect.commit()


    def get_all_description_goal(self) -> list[str]:

        self.__cursor.execute('SELECT description FROM Goal')

        result = self.__cursor.fetchall()

        descriptions = [elem[0] for elem in result]

        return descriptions


    def check_accumulation(self, value) -> bool:

        self.__cursor.execute('SELECT deposit, required FROM Goal WHERE description = ?', (value.get('description'),))

        result = self.__cursor.fetchone()

        if result[0] >= result[1]:

            return True

        return False


    def get_data_goal_from_description(self, value):

        self.__cursor.execute('SELECT * FROM Goal WHERE description = ?', (value.get('description'),))

        result = self.__cursor.fetchone()

        return result


    def get_all_data_goal(self):

        self.__cursor.execute('SELECT * FROM Goal')

        result = self.__cursor.fetchall()

        return result


    def get_all_data_completed_goal(self):

        self.__cursor.execute('SELECT * FROM Completed_Goal')

        result = self.__cursor.fetchall()

        return result


    def transfers_in_completed_goals(self, value) -> None:

        data_goal = self.get_data_goal_from_description(value)

        self.__cursor.execute(
            'INSERT INTO Completed_Goal (description, required, deposit, date) VALUES (?, ?, ?, ?)',
            (data_goal[1], data_goal[2], data_goal[3], data_goal[4])
        )

        self.__connect.commit()


