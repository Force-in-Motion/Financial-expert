
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, types
from aiogram import F

from model.states import States
from model.logic_transactions import Transactions
from utilits.processing_data import ProcessingData as pd
from keyboards.keyboards import CreateKeyboard as kb


router = Router()
ta = Transactions()


@router.message(F.text.lower() == 'история транзакций')
@router.message(Command('view_transactions'))
async def transactions_menu_handler(message: types.Message) -> None:
    """
    Обрабатывает команду пользователя входа в меню транзакций
    :param message: Принимает команду пользователя
    :return: None
    """
    await message.answer('Меню раздела транзакций', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Выберите действие', reply_markup=kb.create_menu_transactions())


@router.callback_query(StateFilter(None), F.data == 'period')
async def transactions_by_period_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке "Транзакции за период"
    :return: None
    """
    await callback.message.answer('Введите начало периода в формате: год-месяц-день\nПример: 2025-01-01', reply_markup=kb.create_back_main_menu_kb())
    await state.set_state(States.start_period_transactions)
    await callback.message.delete()
    await callback.answer()


@router.message(StateFilter(States.start_period_transactions), F.text)
async def input_start_period_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение пользователя (ввод старта периода), записывает данные в стейт, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    if pd.validate_date_format(message.text):
        await state.update_data(user_id=message.from_user.id, start_date=message.text)
        await message.answer('Введите окончание периода', reply_markup=kb.create_back_main_menu_kb())
        await state.set_state(States.end_period_transactions)
    else:
        await message.answer('Не корректный ввод даты', reply_markup=kb.create_back_main_menu_kb())


@router.message(StateFilter(States.end_period_transactions), F.text)
async def input_end_period_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение пользователя (ввод окончания периода), записывает данные в стейт, меняет стейт на новый
    Отправляет запросы в базу данных, обрабатывает их выводит ответ пользователю
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    if pd.validate_date_format(message.text):

        await state.update_data(end_date=message.text)
        data = await state.get_data()
        income = ta.get_transactions_income_by_date(data)
        expense = ta.get_transactions_expense_by_date(data)

        if income:
            await message.answer('Ваши доходы за указанный период')
            for row in income:
                await message.answer(f'Категория: {row[0]}\n Сумма: {row[1]}\n Дата: {row[2]}')
        else:
            await message.answer('За указанный период дохода не было')

        if expense:
            await message.answer('Ваши расходы за указанный период')
            for row in expense:
                await message.answer(f'Категория: {row[0]}\n Сумма: {row[1]}\n Дата: {row[2]}', reply_markup=kb.create_main_menu_kb())
                await state.clear()
        else:
            await message.answer('За указанный период расхода не было', reply_markup=kb.create_main_menu_kb())
            await state.clear()
    else:
        await message.answer('Не корректный ввод даты', reply_markup=kb.create_back_main_menu_kb())

@router.callback_query(StateFilter(None), F.data == 'category')
async def transactions_by_category_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке "Транзакции по категории"
    :return: None
    """
    await callback.message.answer('Введите категорию для поиска транзакций', reply_markup=kb.create_back_main_menu_kb())
    await callback.message.delete()
    await state.set_state(States.search_transaction_by_category)
    await callback.answer()


@router.message(StateFilter(States.search_transaction_by_category), F.text)
async def input_category_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение пользователя (ввод категории), записывает данные в стейт, меняет стейт на новый
    Отправляет запросы в базу данных, обрабатывает их выводит ответ пользователю
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.update_data(category=message.text, user_id=message.from_user.id)
    data = await state.get_data()
    income = ta.get_transactions_income_by_category(data)
    expense = ta.get_transactions_expense_by_category(data)

    if income:
        await message.answer('Ваши доходы по указанной категории')
        for row in income:
            await message.answer(f'Категория: {row[0]}\n Сумма: {row[1]}\n Дата: {row[2]}')
    else:
        await message.answer('По указанной категории дохода не было')

    if expense:
        await message.answer('Ваши расходы по указанной категории')
        for row in expense:
            await message.answer(f'Категория: {row[0]}\n Сумма: {row[1]}\n Дата: {row[2]}', reply_markup=kb.create_main_menu_kb())
            await state.clear()
    else:
        await message.answer('По указанной категории расхода не было', reply_markup=kb.create_main_menu_kb())
        await state.clear()


@router.callback_query(StateFilter(None), F.data == 'results')
async def results_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке "Итоги за период"
    :return: None
    """
    await callback.message.answer('Введите начало периода в формате: год-месяц-день\nПример: 2025-01-01', reply_markup=kb.create_back_main_menu_kb())
    await state.set_state(States.start_period_result)
    await callback.message.delete()
    await callback.answer()


@router.message(StateFilter(States.start_period_result), F.text)
async def input_start_period_result_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение пользователя (ввод старта периода итогов), записывает данные в стейт, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    if pd.validate_date_format(message.text):
        await state.update_data(start_date=message.text, user_id=message.from_user.id)
        await message.answer('Введите окончание периода', reply_markup=kb.create_back_main_menu_kb())
        await state.set_state(States.end_period_result)
    else:
        await message.answer('Не корректный ввод даты', reply_markup=kb.create_back_main_menu_kb())


@router.message(StateFilter(States.end_period_result), F.text)
async def input_start_period_result_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение пользователя (ввод окончания периода итогов), записывает данные в стейт, сбрасывает состояния
    Отправляет запросы в базу данных, обрабатывает их выводит ответ пользователю
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    if pd.validate_date_format(message.text):

        await state.update_data(end_date=message.text)
        data = await state.get_data()
        sum_income = ta.get_sum_transactions_income(data)
        sum_expense = ta.get_sum_transactions_expense(data)

        if sum_income:
            await message.answer(f'Ваши доходы за указанный период: {sum_income[0][0]}')
        else:
            await message.answer('За указанный период дохода не было')

        if sum_expense:
            await message.answer(f'Ваши расходы за указанный период: {sum_expense[0][0]}', reply_markup=kb.create_main_menu_kb())
            await state.clear()
        else:
            await message.answer('За указанный период расхода не было', reply_markup=kb.create_main_menu_kb())
            await state.clear()
    else:
        await message.answer('Не корректный ввод даты', reply_markup=kb.create_back_main_menu_kb())





















