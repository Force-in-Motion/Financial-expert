from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, types
from aiogram import F
from jinja2.async_utils import auto_await

from model.states import States
from model.db_operations import Goal
from keyboards.keyboards import CreateKeyboard as kb

router = Router()
goal = Goal()


@router.message( F.text.lower() == 'меню целей')
@router.message(Command('goal'))
async def goal_menu_handler(message: types.Message) -> None:
    """
    Обрабатывает команду пользователя- переход в меню работы с целями
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :return: None
    """
    await message.answer('Войдите в требуемое меню', reply_markup=kb.create_menu_goal_kb())


@router.callback_query(StateFilter(None), F.data == 'add_goal')
async def add_goal_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке 'Добавить цель'
    :return: None
    """
    await callback.message.answer('Введите короткое описание цели, например: На отпуск')
    await state.set_state(States.description)
    await callback.answer()


@router.message(StateFilter(States.description), F.text)
async def description_goal_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :param state: Состояние, находясь в котором бот реагирует на команду пользователя
    :return: None
    """
    await state.update_data(description=message.text)
    await message.answer('Введите сумму для депозита')
    await state.set_state(States.deposit)


@router.message(StateFilter(States.deposit), F.text)
async def deposit_goal_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и затем извлекает из стейта
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :param state: Состояние, находясь в котором бот реагирует на команду пользователя
    :return: None
    """
    if message.text.isdigit():
        await state.update_data(deposit=message.text)
        data = await state.get_data()
        goal.add_goal(data)
        await message.answer('Цель успешно создана')
        await state.clear()
    else:
        await message.reply('Введите число!')


@router.callback_query(F.data == 'my_goal')
async def my_goal_callback_handler(callback: types.CallbackQuery) -> None:
    """
    Обрабатывает клик по кнопке 'Мои цели'
    :return: None
    """
    await callback.message.answer('Войдите в требуемое меню', reply_markup=kb.create_menu_my_goal_kb())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == 'list_goal')
async def list_goal_callback_handler(callback: types.CallbackQuery) -> None:
    """
    Обрабатывает клик по кнопке 'Список целей'
    :return: None
    """
    await callback.message.answer('Список активных целей', reply_markup=kb.create_list_goals_kb())
    await callback.message.delete()
    await callback.answer()