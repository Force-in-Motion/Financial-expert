from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from service.service_data import SaveLoadData as sld

class CreateKeyboard:



    @staticmethod
    def create_main_menu_kb():

        builder = ReplyKeyboardBuilder()

        builder.button(text='Добавить доход')
        builder.button(text='Добавить расход')
        builder.button(text='Определить цель')
        builder.button(text='История транзакций')
        builder.button(text='Статистика')

        builder.adjust(2, 1, 2)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def help_btn():
        builder = ReplyKeyboardBuilder()

        builder.button(text='Помощь')

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_category_kb():

        builder = InlineKeyboardBuilder()

        categories = sld.get_sample()

        for elem in categories:

            builder.button(text=elem, callback_data=elem)

            builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


CreateKeyboard.create_category_kb()