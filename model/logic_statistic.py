import sqlite3
from model.logic_transactions import Transactions



class Statistic:

    def __init__(self):
        self.__transactions = Transactions()


    def get_sum_income(self, value) -> str:
        """
        Используя другой класс отправляет запрос в базу данных для получения транзакций по доходам по полученным датам
        :param value: Принимает дату старта, окончания, user_id
        :return: str
        """

        data = self.__transactions.get_sum_transactions_income(value)

        result = data[0][0]

        return result


    def get_sum_expense(self, value) -> str:
        """
        Используя другой класс отправляет запрос в базу данных для получения транзакций по расходам по полученным датам
        :param value: Принимает дату старта, окончания, user_id
        :return: str
        """
        data = self.__transactions.get_sum_transactions_expense(value)

        result = data[0][0]

        return result


    def get_balance(self, value) -> int or bool:
        """
        Используя другой класс отправляет запрос в базу данных для получения транзакций по доходам и расходам по полученным датам
        Затем вычисляет чистый баланс
        :param value: Принимает дату старта, окончания, user_id
        :return: str
        """
        income = self.get_sum_income(value)
        expense = self.get_sum_expense(value)

        if income and expense:
            result = int(income) - int(expense)
            return result

        return False


    def get_struct_income(self, value) -> list:
        """
        Используя другой класс отправляет запрос в базу данных для получения транзакций по доходам по user_id
        :param value: Принимает дату старта, окончания, user_id
        :return: list
        """
        data = self.__transactions.get_data_transactions_income(value)

        return data

    def get_struct_expense(self, value) -> list:
        """
        Используя другой класс отправляет запрос в базу данных для получения транзакций по доходам по user_id
        :param value: Принимает дату старта, окончания, user_id
        :return: list
        """
        data = self.__transactions.get_data_transactions_expense(value)

        return data


    def top_cost_categories(self, user_id):
        pass