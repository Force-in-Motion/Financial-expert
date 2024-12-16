from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from model.db_operations import Goal


class CreateKeyboard:


    @staticmethod
    def create_main_menu_kb():

        builder = ReplyKeyboardBuilder()

        builder.button(text='Добавить доход')
        builder.button(text='Добавить расход')
        builder.button(text='Меню целей')
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
    def create_menu_goal_kb():

        builder = InlineKeyboardBuilder()

        builder.button(text='Добавить цель', callback_data='add_goal')
        builder.button(text='Мои цели', callback_data='my_goal')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_menu_my_goal_kb():

        builder = InlineKeyboardBuilder()

        builder.button(text='Список целей', callback_data='list_goal')
        builder.button(text='Показать статистику', callback_data='add_deposit')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_list_goals_kb():
        goal = Goal()

        builder = InlineKeyboardBuilder()

        for elem in goal.get_description_goal():

            builder.button(text=elem, callback_data=elem)

        builder.adjust(1)

        del goal

        return builder.as_markup(resize_keyboard=True)