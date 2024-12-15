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
    def get_samples_path() -> str:
        """
        Создает относительный путь к файлу common_areas
        :return: Путь в виде строки
        """
        current_dir = os.path.dirname(__file__)
        path_sample = os.path.join(current_dir, '..', 'settings', 'samples.json')

        return os.path.abspath(path_sample)


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
        with open(SaveLoadData.get_token_path(), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['token']


    @staticmethod
    def get_sample() -> str:
        with open(SaveLoadData.get_samples_path(), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['categories']