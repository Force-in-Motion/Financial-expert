import aiogram
import asyncio
from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram import F

from keyboards.keyboards import CreateKeyboard as cb



router = Router()



@router.message(Command('start'))
async def start_handler(message: types.Message) -> None:
    mess = ('Привет!\n Я помогу тебе управлять личными финансами,'
            ' отслеживать расходы и доходы, определять категории'
            ' фин. операций и анализировать личный бюджет.\n\n'
            'Основные команды:\n'
            '/start - Запуск приложения.\n\n'
            '/register - Регистрация нового пользователя в системе.\n\n'
            '/login - Авторизация пользователя для доступа к его данным.\n\n'
            '/add_income [сумма] [категория] - Добавление дохода с указанием суммы и категории.\n\n'
            '/add_expense [сумма] [категория] - Добавление расхода с указанием суммы и категории.\n\n'
            '/set_goal [сумма] [описание] - Установка финансовой цели с указанием суммы и описания.\n\n'
            '/view_transactions [период] - Просмотр истории транзакций за указанный период.\n\n'
            '/view_categories - Просмотр доступных категорий, список категорий можно расширить\n\n'
            '/statistics - Просмотр статистики по расходам и доходам, а также прогрессу в достижении финансовых целей.\n\n'
            '/help - Список доступных команд и описание их использования.')

    await message.answer(mess, reply_markup=cb.create_main_menu_kb())

