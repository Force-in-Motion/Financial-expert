import sqlite3
from datetime import datetime
from service.service_data import SaveLoadData as sld



class Income:
    def __init__(self):
        self.__connect = sqlite3.connect(sld.get_db_path())
        self.__cursor = self.__connect.cursor()
        self.__create_table()


    def __create_table(self) -> None:

        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS Income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quantity INTEGER  NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
        )
        """)

        self.__connect.commit()


    def add_income(self, value) -> None:

        current_date = datetime.now().strftime('%Y-%m-%d')

        self.__cursor.execute(
        'INSERT INTO Income (quantity, category, date)'
        ' VALUES (?, ?, ?)', (value['quantity'], value['category'], current_date)
        )

        self.__connect.commit()
        self.__connect.close()
