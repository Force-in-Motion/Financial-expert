
import os
import json



class SaveLoadData:

    @staticmethod
    def get_token_path() -> str:
        """
        Создает относительный путь к файлу common_areas
        :return: Путь в виде строки
        """
        current_dir = os.path.dirname(__file__)
        path_token = os.path.join(current_dir, '..', 'settings', 'token.json')

        return os.path.abspath(path_token)



    @staticmethod
    def get_db_path() -> str:
        """
        Создает относительный путь к файлу common_areas
        :return: Путь в виде строки
        """
        current_dir = os.path.dirname(__file__)
        path_db = os.path.join(current_dir, '..', 'storage', 'database.db')

        return os.path.abspath(path_db)


    @staticmethod
    def get_graphs_income_column_path() -> str:
        """
        Создает относительный путь к файлу с заданным именем
        :return: Путь в виде строки
        """
        current_dir = os.path.dirname(__file__)
        path_file = os.path.join(current_dir, '..', 'media', 'column_income.png')

        return os.path.abspath(path_file)


    @staticmethod
    def get_graphs_expense_column_path() -> str:
        """
        Создает относительный путь к файлу с заданным именем
        :return: Путь в виде строки
        """
        current_dir = os.path.dirname(__file__)
        path_file = os.path.join(current_dir, '..', 'media', 'column_expense.png')

        return os.path.abspath(path_file)


    @staticmethod
    def get_graphs_income_circle_path() -> str:
        """
        Создает относительный путь к файлу с заданным именем
        :return: Путь в виде строки
        """
        current_dir = os.path.dirname(__file__)
        path_file = os.path.join(current_dir, '..', 'media', 'circle_income.png')

        return os.path.abspath(path_file)


    @staticmethod
    def get_graphs_expense_circle_path() -> str:
        """
        Создает относительный путь к файлу с заданным именем
        :return: Путь в виде строки
        """
        current_dir = os.path.dirname(__file__)
        path_file = os.path.join(current_dir, '..', 'media', 'circle_expense.png')

        return os.path.abspath(path_file)


    @staticmethod
    def del_file(path) -> None:
        """
        Удаляет файл по полученному пути
        :param path: Принимает путь
        :return: None
        """
        if os.path.exists(path):
            os.remove(path)


    @staticmethod
    def get_token() -> str:
        """
        Получает токен по указанному пути
        :return: Токен в виде строки
        """
        with open(SaveLoadData.get_token_path(), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['token']

