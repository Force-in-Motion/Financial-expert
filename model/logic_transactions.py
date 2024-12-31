import sqlite3
from service.service_data import SaveLoadData as sld



class Transactions:

    def __init__(self):
        self.__connect = sqlite3.connect(sld.get_db_path())
        self.__cursor =  self.__connect.cursor()


    def get_transactions_income_by_date(self, value) -> list:
        """
        Отправляет запрос в базу данных для получения транзакций по доходам по полученным датам
        :param value: Принимает дату старта и окончания
        :return: Результат запроса
        """
        self.__cursor.execute(
            'SELECT category, quantity, date FROM Income WHERE date BETWEEN ? AND ? AND user_id = ?',
            (value.get('start_date'), value.get('end_date'), value.get('user_id'))
        )

        result = self.__cursor.fetchall()

        return result


    def get_transactions_expense_by_date(self, value) -> list:
        """
        Отправляет запрос в базу данных для получения транзакций по расходам по полученным датам
        :param value: Принимает дату старта и окончания
        :return: Результат запроса
        """
        self.__cursor.execute(
            'SELECT category, quantity, date FROM Expense WHERE date BETWEEN ? AND ? AND user_id = ?',
            (value.get('start_date'), value.get('end_date'), value.get('user_id'))
        )

        result = self.__cursor.fetchall()

        return result


    def get_sum_transactions_income(self, value) -> list:
        """
        Отправляет запрос в базу данных для получения суммы транзакций по доходам по полученным датам
        :param value: Принимает дату старта и окончания
        :return: Результат запроса
        """
        self.__cursor.execute(
            'SELECT SUM(quantity) FROM Income WHERE date BETWEEN ? AND ? AND  user_id = ?',
            (value.get('start_date'), value.get('end_date'), value.get('user_id'))
        )

        result = self.__cursor.fetchall()

        return result


    def get_sum_transactions_expense(self, value) -> list:
        """
        Отправляет запрос в базу данных для получения суммы транзакций по расходам по полученным датам
        :param value: Принимает дату старта и окончания
        :return: Результат запроса
        """
        self.__cursor.execute(
            'SELECT SUM(quantity) FROM Expense WHERE date BETWEEN ? AND ? AND   user_id = ?',
            (value.get('start_date'), value.get('end_date'), value.get('user_id'))
        )

        result = self.__cursor.fetchall()

        return result


    def get_transactions_income_by_category(self, value) -> list:
        """
        Отправляет запрос в базу данных для получения транзакций по доходам по полученной категории
        :param value: Принимает дату старта и окончания
        :return: Результат запроса
        """
        self.__cursor.execute(
            'SELECT category, quantity, date FROM Income WHERE category = ? AND user_id = ?',
            (value.get('category'), value.get('user_id'))
        )

        result = self.__cursor.fetchall()

        return result


    def get_transactions_expense_by_category(self, value) -> list:
        """
        Отправляет запрос в базу данных для получения транзакций по расходам по полученной категории
        :param value: Принимает дату старта и окончания
        :return: Результат запроса
        """
        self.__cursor.execute(
            'SELECT category, quantity, date FROM Expense WHERE category = ? AND user_id = ?',
            (value.get('category'), value.get('user_id'))
        )

        result = self.__cursor.fetchall()

        return result