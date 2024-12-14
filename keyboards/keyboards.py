from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

class CreateKeyboard:

    @staticmethod
    def create_main_menu_btn():

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


