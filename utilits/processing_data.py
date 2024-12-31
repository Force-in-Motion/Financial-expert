import re




class ProcessingData:

    mess_menu = ('/menu_user - Редактирование данных пользователя.\n\n'
            '/add_income [сумма] [категория] - Добавление дохода с указанием суммы и категории.\n\n'
            '/add_expense [сумма] [категория] - Добавление расхода с указанием суммы и категории.\n\n'
            '/goal - Открывает меню установки и контроля целей.\n\n'
            '/view_transactions [период] - Просмотр истории транзакций за указанный период.\n\n'
            '/statistics - Просмотр статистики по расходам и доходам, а также прогрессу в достижении финансовых целей.\n\n'
            '/menu - Возврат в главное меню и список доступных команд.')


    @staticmethod
    def validate_date_format(value):
        """
        Проверяет является ли строка валидной датой для запроса в базу данных
        :param value: Принимает строку
        :return: bool
        """
        date = r'^\d{4}-\d{2}-\d{2}$'

        if not re.match(date, value):
                return False

        year, month, day = map(int, value.split('-'))
        if month < 1 or month > 12 or day < 1 or day > 31:
                return False

        if month in [4, 6, 9, 11] and day > 30:
                return False
        if month == 2:
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                        if day > 29:
                                return False
                else:
                        if day > 28:
                                return False

        return True