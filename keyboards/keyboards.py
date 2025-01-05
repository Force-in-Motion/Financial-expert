from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from model.logic_goals import Goal


class CreateKeyboard:

    @staticmethod
    def create_enter_menu_kb():
        """
        Создает начальную клавиатуру для регистрации или авторизации пользователя
        :return: Клавиатуру
        """
        builder = ReplyKeyboardBuilder()

        builder.button(text='Регистрация')
        builder.button(text='Авторизация')

        builder.adjust(2, 1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_main_menu_kb():
        """
        Создает клавиатуру главного меню бота
        :return: Клавиатуру
        """
        builder = ReplyKeyboardBuilder()

        builder.button(text='Меню целей')
        builder.button(text='Добавить доход')
        builder.button(text='Добавить расход')
        builder.button(text='История транзакций')
        builder.button(text='Статистика')
        builder.button(text='Меню пользователя')
        builder.button(text='Главное меню')

        builder.adjust(1, 2, 2, 1, 1, )

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_process_user_data():
        """
        Создает клавиатуру для работы с меню пользователя
        :return: Клавиатуру
        """
        builder = InlineKeyboardBuilder()

        builder.button(text='Редактировать имя ', callback_data='username')
        builder.button(text='Редактировать пароль', callback_data='password')
        builder.button(text='Удалить пользователя', callback_data='deluser')
        builder.button(text='Главное меню', callback_data='menu')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_menu_transactions():
        """
        Создает клавиатуру для работы с транзакциями пользователя
        :return: Клавиатуру
        """
        builder = InlineKeyboardBuilder()

        builder.button(text='Транзакции за период', callback_data='period')
        builder.button(text='Транзакции по категории', callback_data='category')
        builder.button(text='Итоги за период', callback_data='results')
        builder.button(text='Главное меню', callback_data='menu')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_menu_goal_kb():
        """
        Создает клавиатуру для работы с целями пользователя
        :return: Клавиатуру
        """
        builder = InlineKeyboardBuilder()

        builder.button(text='Добавить цель', callback_data='add_goal')
        builder.button(text='Мои цели', callback_data='my_goal')
        builder.button(text='Главное меню', callback_data='menu')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_menu_my_goals_kb():
        """
        Создает клавиатуру для работы с целями пользователя
        :return: Клавиатуру
        """
        builder = InlineKeyboardBuilder()

        builder.button(text='Список целей', callback_data='list_goal')
        builder.button(text='Показать статистику', callback_data='statistic_goal')
        builder.button(text='Главное меню', callback_data='menu')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_list_goals_kb(user_id):
        """
        Создает клавиатуру для работы с целями пользователя,
         которая выводит на экран все цели пользователя в виде инлайн кнопок
        :return: Клавиатуру
        """
        goal = Goal()

        builder = InlineKeyboardBuilder()

        for elem in goal.get_all_description_goal(user_id):

            builder.button(text=elem, callback_data=elem)

        builder.adjust(1)

        del goal

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_menu_one_goal():
        """
        Создает клавиатуру для работы с целями пользователя
        :return: Клавиатуру
        """
        builder = InlineKeyboardBuilder()

        builder.button(text='Удалить цель', callback_data='del_goal')
        builder.button(text='Добавить депозит', callback_data='add_deposit')
        builder.button(text='Главное меню', callback_data='menu')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_main_menu_statistic_goals():
        """
        Создает клавиатуру для работы со статистикой целей пользователя
        :return: Клавиатуру
        """
        builder = InlineKeyboardBuilder()

        builder.button(text='Активные цели', callback_data='active')
        builder.button(text='Завершенные цели', callback_data='finished')
        builder.button(text='Главное меню', callback_data='menu')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_back_main_menu_kb():
        """
        Создает клавиатуру, которая возвращает пользователя в главное меню бота очищая все состояния
        :return: Клавиатуру
        """
        builder = InlineKeyboardBuilder()

        builder.button(text='Главное меню', callback_data='menu')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_statistic_main_menu_kb():
        """
        Создает клавиатуру, которая определяет меню возможностей разделе статистики
        :return: Клавиатуру
        """
        builder = InlineKeyboardBuilder()

        builder.button(text='Общий доход за период', callback_data='all_income')
        builder.button(text='Общий расход за период', callback_data='all_expense')
        builder.button(text='Чистый баланс за период', callback_data='all_balance')
        builder.button(text='Структура по категориям', callback_data='structure_by_categories')
        builder.button(text='ТОП затратных категорий', callback_data='cost_categories')
        builder.button(text='Прогресс целей', callback_data='statistic_goal')
        builder.button(text='Главное меню', callback_data='menu')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_options_struct_output_kb():

        builder = InlineKeyboardBuilder()

        builder.button(text='Текстовое представление', callback_data='text_content')
        builder.button(text='Графическое представление', callback_data='visual_content')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod
    def create_diagram_kb():

        builder = InlineKeyboardBuilder()

        builder.button(text='Столбчатая диаграмма', callback_data='column')
        builder.button(text='Круговая диаграмма', callback_data='circular')

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)