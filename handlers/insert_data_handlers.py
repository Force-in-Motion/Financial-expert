from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, types
from aiogram import F

from model.states import States
from model.logic_deposits import Income
from model.logic_deposits import Expense
from keyboards.keyboards import CreateKeyboard as kb

router = Router()
income = Income()
expense = Expense()

@router.message(StateFilter(None), F.text.lower() == 'добавить доход')
@router.message(StateFilter(None), Command('add_income'))
async def input_quantity_income_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :param state: Состояние, находясь в котором бот реагирует на команду пользователя
    :return: None
    """
    await message.answer('Раздел ваших доходов', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Введите сумму своего дохода', reply_markup=kb.create_back_main_menu_kb())
    await state.set_state(States.quantity_income)
    await state.update_data(user_id=message.from_user.id)


@router.message(StateFilter(States.quantity_income), F.text)
async def input_category_income_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :param state: Состояние, находясь в котором бот реагирует на команду пользователя
    :return: None
    """
    if message.text.isdigit():
        await state.update_data(quantity=message.text)
        await message.answer('Введите название категории', reply_markup=kb.create_back_main_menu_kb())
        await state.set_state(States.category_income)
    else:
        await message.reply('Введите число!')


@router.message(StateFilter(States.category_income), F.text)
async def creating_finished_record_income_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и затем извлекает из стейта
    Все данные, полученные входе диалога в состояниях, затем передает в модель для записи в базу данных
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :param state: Состояние, находясь в котором бот реагирует на команду пользователя
    :return: None
    """

    await state.update_data(category=message.text)
    data = await state.get_data()
    income.add_income(data)
    await message.answer('Ваши данные успешно сохранены', reply_markup=kb.create_main_menu_kb())
    await state.clear()



@router.message(StateFilter(None), F.text.lower() == 'добавить расход')
@router.message(StateFilter(None), Command('add_expense'))
async def input_quantity_expense_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :param state: Состояние, находясь в котором бот реагирует на команду пользователя
    :return: None
    """
    await message.answer('Раздел ваших расходов', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Введите сумму своего расхода', reply_markup=kb.create_back_main_menu_kb())
    await state.set_state(States.quantity_expense)
    await state.update_data(user_id=message.from_user.id)


@router.message(StateFilter(States.quantity_expense), F.text)
async def input_category_expense_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :param state: Состояние, находясь в котором бот реагирует на команду пользователя
    :return: None
    """
    if message.text.isdigit():
        await state.update_data(quantity=message.text)
        await message.answer('Введите название категории', reply_markup=kb.create_back_main_menu_kb())
        await state.set_state(States.category_expense)
    else:
        await message.reply('Введите число!')


@router.message(StateFilter(States.category_expense), F.text)
async def creating_finished_record_expense_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и затем извлекает из стейта
    Все данные, полученные входе диалога в состояниях, затем передает в модель для записи в базу данных
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :param state: Состояние, находясь в котором бот реагирует на команду пользователя
    :return: None
    """
    await state.update_data(category=message.text)
    data = await state.get_data()
    expense.add_expense(data)
    await message.answer('Ваши данные успешно сохранены', reply_markup=kb.create_main_menu_kb())
    await state.clear()







