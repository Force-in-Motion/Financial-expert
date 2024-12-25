
from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F

from keyboards.keyboards import CreateKeyboard as kb



router = Router()



@router.message(Command('start'))
async def start_handler(message: types.Message) -> None:
    mess = ('Привет!\n Я помогу тебе управлять личными финансами,'
            ' отслеживать расходы и доходы, определять категории'
            ' фин. операций, анализировать личный бюджет,\n'
            ' ставить цели и многое другое.\n\n'
            'Основные команды:\n'
            '/start - Запуск приложения.\n\n'
            '/login - Авторизация пользователя.\n\n'
            '/register - Регистрация нового пользователя в системе.\n\n'
            )

    await message.answer(mess, reply_markup=kb.create_enter_menu_kb())

