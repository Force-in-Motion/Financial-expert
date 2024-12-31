import sqlite3
from datetime import datetime
from service.service_data import SaveLoadData as sld



class Income:
    def __init__(self):
        self.__connect = sqlite3.connect(sld.get_db_path())
        self.__cursor = self.__connect.cursor()
        self.__create_table_income()


    def __create_table_income(self) -> None:
        """
        Создает таблицу в базе данных, содержащую депозиты доходов пользователя
        :return: None
        """
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
        """
        Добавляет доходы пользователя в соответствующую таблицу
        :param value: Принимает суммы, категорию и id пользователя
        :return: None
        """
        current_date = datetime.now().strftime('%Y-%m-%d')

        self.__cursor.execute(
        'INSERT INTO Income (quantity, category, user_id, date) VALUES (?, ?, ?, ?)',
        (value.get('quantity'), value.get('category'), value.get('user_id'), current_date)
        )

        self.__connect.commit()



class Expense:

    def __init__(self):
        self.__connect = sqlite3.connect(sld.get_db_path())
        self.__cursor = self.__connect.cursor()
        self.__create_table_expense()


    def __create_table_expense(self) -> None:
        """
        Создает таблицу в базе данных, содержащую депозиты расходов пользователя
        :return: None
        """
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
        """
        Добавляет расходы пользователя в соответствующую таблицу
        :param value: Принимает суммы, категорию и id пользователя
        :return: None
        """
        current_date = datetime.now().strftime('%Y-%m-%d')

        self.__cursor.execute(
        'INSERT INTO Expense (quantity, category, user_id, date) VALUES (?, ?, ?, ?)',
  (value.get('quantity'), value.get('category'), value.get('user_id'), current_date)
        )

        self.__connect.commit()
