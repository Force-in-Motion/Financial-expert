import matplotlib.pyplot as plt
import numpy as np

from model.logic_transactions import Transactions
from service.service_data import SaveLoadData as sld

class VisualData:

    def __init__(self):
        self.__transaction = Transactions()


    def create_column_diagram_income(self, value):
        """
        Создает столбчатую диаграмму на основе полученных данных из базы данных
        :param value: Принимает стартовую дату, дату окончания, user_id
        :return: файл с диаграммой
        """
        categories = []
        quantity = []

        income = self.__transaction.get_data_transactions_income(value)
        if income:
            for row in income:
                categories.append(row[0])
                quantity.append(row[1])

            plt.figure(figsize=(10, 6))
            plt.style.use('default')
            plt.bar(categories, quantity)
            values = np.linspace(0, max(quantity) + 10, 10)
            plt.yticks(values)
            plt.xticks(rotation=90)
            plt.title('Структура доходов по категориям', loc='left', pad=40)
            plt.xlabel('Категория', ha='right')
            plt.ylabel('Сумма')
            for idx, val in enumerate(quantity):
                plt.text(idx, val + 1, str(val), ha='center')

            plt.ylim(0, max(quantity) + 10)
            plt.savefig(sld.get_graphs_income_column_path(), dpi=100, bbox_inches='tight')
            plt.close()

        return False

    def create_column_diagram_expense(self, value):
        """
        Создает столбчатую диаграмму на основе полученных данных из базы данных
        :param value: Принимает стартовую дату, дату окончания, user_id
        :return: файл с диаграммой
        """
        categories = []
        quantity = []

        expense = self.__transaction.get_data_transactions_expense(value)
        if expense:
            for row in expense:
                categories.append(row[0])
                quantity.append(row[1])

            plt.figure(figsize=(10, 6))
            plt.style.use('default')
            plt.bar(categories, quantity)
            values = np.linspace(0, max(quantity) + 10, 10)
            plt.yticks(values)
            plt.xticks(rotation=90)
            plt.title('Структура расходов по категориям', loc='left', pad=40)
            plt.xlabel('Категория', ha='right')
            plt.ylabel('Сумма')
            for idx, val in enumerate(quantity):
                plt.text(idx, val + 1, str(val), ha='center')

            plt.ylim(0, max(quantity) + 10)
            plt.savefig(sld.get_graphs_expense_column_path(), dpi=100, bbox_inches='tight')
            plt.close()

        return False


    def create_circle_diagram_income(self, value):
        """
        Создает столбчатую диаграмму на основе полученных данных из базы данных
        :param value: Принимает стартовую дату, дату окончания, user_id
        :return: файл с диаграммой
        """
        categories = []
        quantity = []

        expense = self.__transaction.get_data_transactions_income(value)
        if expense:
            for row in expense:
                categories.append(row[0])
                quantity.append(row[1])

            plt.figure(figsize=(10, 8))
            plt.style.use('default')
            plt.pie(quantity, labels=categories, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title('Структура расходов по категориям')
            plt.savefig(sld.get_graphs_income_circle_path(), dpi=100, bbox_inches='tight')
            plt.close()

        return False


    def create_circle_diagram_expense(self, value):
        """
        Создает столбчатую диаграмму на основе полученных данных из базы данных
        :param value: Принимает стартовую дату, дату окончания, user_id
        :return: файл с диаграммой
        """
        categories = []
        quantity = []

        expense = self.__transaction.get_data_transactions_expense(value)
        if expense:
            for row in expense:
                categories.append(row[0])
                quantity.append(row[1])

            plt.figure(figsize=(10, 8))
            plt.style.use('default')
            plt.pie(quantity, labels=categories, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title('Структура расходов по категориям')
            plt.savefig(sld.get_graphs_expense_circle_path(), dpi=100, bbox_inches='tight')
            plt.close()

        return False
