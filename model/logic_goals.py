import sqlite3
from datetime import datetime
from service.service_data import SaveLoadData as sld



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
            'INSERT INTO Goal (description, required, user_id, date) VALUES (?, ?, ?, ?)',
            (value.get('description'), value.get('required'), value.get('user_id'), current_date)
        )

        self.__connect.commit()


    def add_deposit(self, value) -> None:

        self.__cursor.execute('SELECT deposit FROM Goal WHERE description = ? AND user_id = ?',
                              (value.get('description'), value.get('user_id')))
        result = self.__cursor.fetchone()

        new_deposit = result[0] + int(value.get('deposit'))

        self.__cursor.execute(
            'UPDATE Goal SET deposit = ? WHERE description = ? AND user_id = ?',
            (new_deposit, value.get('description'), value.get('user_id')))

        self.__connect.commit()


    def del_goal(self, value) -> None:

        self.__cursor.execute('DELETE FROM Goal WHERE description = ? AND user_id = ?',
                              (value.get('description'), value.get('user_id')))

        self.__connect.commit()


    def get_all_description_goal(self, user_id: int) -> list[str]:

        self.__cursor.execute('SELECT description FROM Goal WHERE user_id = ?', (user_id,))

        result = self.__cursor.fetchall()

        descriptions = [elem[0] for elem in result]

        return descriptions


    def check_accumulation(self, value) -> bool:

        self.__cursor.execute('SELECT deposit, required FROM Goal WHERE description = ? AND user_id = ?',
                              (value.get('description'), value.get('user_id')))

        result = self.__cursor.fetchone()

        if result[0] >= result[1]:

            return True

        return False


    def get_data_goal_from_description(self, value):

        self.__cursor.execute('SELECT * FROM Goal WHERE description = ? AND user_id = ?',
                              (value.get('description'), value.get('user_id')))

        result = self.__cursor.fetchone()

        return result


    def get_all_data_goal(self, user_id: int):

        self.__cursor.execute('SELECT * FROM Goal WHERE user_id = ?', (user_id,))

        result = self.__cursor.fetchall()

        return result


    def get_all_data_completed_goal(self, user_id: int):
        self.__cursor.execute('SELECT * FROM Completed_Goal WHERE user_id = ?', (user_id,))

        result = self.__cursor.fetchall()

        return result


    def transfers_in_completed_goals(self, value) -> None:

        data_goal = self.get_data_goal_from_description(value)

        self.__cursor.execute(
            'INSERT INTO Completed_Goal (user_id, description, required, deposit, date) VALUES (?, ?, ?, ?, ?)',
            (data_goal[1], data_goal[2], data_goal[3], data_goal[4], data_goal[5])
        )

        self.__connect.commit()
