from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, types
from aiogram import F

from model.states import States
from model.db_operations import Income
from model.db_operations import Expense

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
    await message.answer('Введите сумму своего дохода')
    await state.set_state(States.quantity_income)


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
        await message.answer('Введите название категории')
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
    if message.text.isdigit():
        await state.update_data(category=message.text)
    else:
        await state.update_data(category=message.text.upper())

    data = await state.get_data()
    income.add_income(data)
    await message.answer('Ваши данные успешно сохранены')
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
    await message.answer('Введите сумму своего расхода')
    await state.set_state(States.quantity_expense)


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
        await message.answer('Введите название категории')
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
    if message.text.isdigit():
        await state.update_data(category=message.text)
    else:
        await state.update_data(category=message.text.upper())

    data = await state.get_data()
    expense.add_expense(data)
    await message.answer('Ваши данные успешно сохранены')
    await state.clear()


@router.message(StateFilter(States.category_income, States.category_expense, States.quantity_income,
                            States.quantity_expense, States.description, States.required, States.one_goal_menu,
                            States.add_deposit))
async def input_error_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя и сообщает об ошибке ввода если получен не текст
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :param state: Состояние, находясь в котором бот реагирует на команду пользователя
    :return: None
    """
    await message.answer('Введите данные из предложенных!')






