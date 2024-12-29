
from aiogram import F
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import CreateKeyboard as kb
from utilits.processing_data import ProcessingData as pd

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


@router.message(F.text.lower() == 'главное меню')
@router.message(Command('menu'))
async def main_menu_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду возврата в главное меню, сбрасывает все стейты
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.clear()
    await message.answer(f'Вы возвращены в главное меню, выберите команду\n\n {pd.mess_menu}', reply_markup=kb.create_main_menu_kb())


@router.callback_query(F.data == 'menu')
async def main_menu_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке "Главное меню"
    :return: None
    """
    await state.clear()
    await callback.message.answer(f'Вы возвращены в главное меню, выберите команду\n\n {pd.mess_menu}', reply_markup=kb.create_main_menu_kb())
    await callback.answer()
