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
    def get_token() -> str:
        """
        Получает токен по указанному пути
        :return: Токен в виде строки
        """
        with open(SaveLoadData.get_token_path(), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['token']

