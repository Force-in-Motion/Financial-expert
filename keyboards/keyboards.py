from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from model.db_operations import Goal


class CreateKeyboard:


    @staticmethod
    def create_main_menu_kb():

        builder = ReplyKeyboardBuilder()

        builder.button(text='Регистрация')
        builder.button(text='Авторизация')
        builder.button(text='Меню целей')
        builder.button(text='Добавить доход')
        builder.button(text='Добавить расход')
        builder.button(text='История транзакций')
        builder.button(text='Редактировать пользователя')
        builder.button(text='Статистика')
        builder.button(text='Помощь')

        builder.adjust(2, 1, 2, 2, 1, 1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_process_user_data():
        builder = InlineKeyboardBuilder()

        builder.button(text='Редактировать имя ', callback_data='username')
        builder.button(text='Редактировать пароль', callback_data='username')
        builder.button(text='Удалить пользователя', callback_data='username')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_menu_goal_kb():

        builder = InlineKeyboardBuilder()

        builder.button(text='Добавить цель', callback_data='add_goal')
        builder.button(text='Мои цели', callback_data='my_goal')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_menu_my_goals_kb():

        builder = InlineKeyboardBuilder()

        builder.button(text='Список целей', callback_data='list_goal')
        builder.button(text='Показать статистику', callback_data='statistic')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_list_goals_kb():
        goal = Goal()

        builder = InlineKeyboardBuilder()

        for elem in goal.get_all_description_goal():

            builder.button(text=elem, callback_data=elem)

        builder.adjust(1)

        del goal

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_menu_one_goal():
        builder = InlineKeyboardBuilder()

        builder.button(text='Удалить цель', callback_data='del_goal')
        builder.button(text='Добавить депозит', callback_data='add_deposit')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_main_menu_statistic_goals():
        builder = InlineKeyboardBuilder()

        builder.button(text='Активные цели', callback_data='active')
        builder.button(text='Завершенные цели', callback_data='finished')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)