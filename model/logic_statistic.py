import sqlite3
from model.logic_transactions import Transactions



class Statistic:

    def __init__(self):
        self.__transactions = Transactions()


    def get_sum_income(self, value) -> str:
        """
        Используя другой класс отправляет запрос в базу данных для получения транзакций по доходам по полученным датам
        :param value: Принимает дату старта и окончания
        :return: str
        """

        data = self.__transactions.get_sum_transactions_income(value)

        result = data[0][0]

        return result


    def get_sum_expense(self, value) -> str:
        """
        Используя другой класс отправляет запрос в базу данных для получения транзакций по расходам по полученным датам
        :param value: Принимает дату старта и окончания
        :return: str
        """
        data = self.__transactions.get_sum_transactions_expense(value)

        result = data[0][0]

        return result


    def get_balance(self, value) -> int:
        """
        Используя другой класс отправляет запрос в базу данных для получения транзакций по доходам и расходам по полученным датам
        Затем вычисляет чистый баланс
        :param value: Принимает дату старта и окончания
        :return: str
        """
        income = self.get_sum_income(value)

        expense = self.get_sum_expense(value)

        result = int(income) - int(expense)

        return result


    def get_struct_income(self, user_id) -> list:
        """
        Используя другой класс отправляет запрос в базу данных для получения транзакций по доходам по user_id
        :param user_id: Принимает user_id
        :return: list
        """
        data = self.__transactions.get_data_transactions_income(user_id)

        return data

    def get_struct_expense(self, user_id) -> list:
        """
        Используя другой класс отправляет запрос в базу данных для получения транзакций по доходам по user_id
        :param user_id: Принимает user_id
        :return: list
        """
        data = self.__transactions.get_data_transactions_expense(user_id)

        return data