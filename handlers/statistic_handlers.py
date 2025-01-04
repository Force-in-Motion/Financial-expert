from IPython.core.inputtransformer2 import MaybeAsyncCompile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, types
from aiogram import F

from model.states import States
from model.logic_statistic import Statistic
from keyboards.keyboards import CreateKeyboard as kb
from utilits.processing_data import ProcessingData as pd

router = Router()
stat = Statistic()


@router.message(F.text.lower() == 'статистика')
@router.message(Command('statistics'))
async def statistics_handler(message: types.Message) -> None:
    """
    Обрабатывает команду пользователя "statistics", вызывает меню данного раздела
    :param message: Принимает команду statistics
    :return: None
    """
    await message.answer('Меню раздела статистики', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Выберите требуемый раздел меню', reply_markup=kb.create_statistic_main_menu_kb())


@router.callback_query(StateFilter(None), F.data == 'all_income')
async def all_income_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке "Общий доход за период"
    :return: None
    """
    await callback.message.answer('Введите начало периода в формате: год-месяц-день\nПример: 2025-01-01', reply_markup=kb.create_back_main_menu_kb())
    await callback.message.delete()
    await state.set_state(States.start_period_income)
    await callback.answer()


@router.message(StateFilter(States.start_period_income), F.text)
async def input_start_period_income_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение пользователя (ввод старта периода), записывает данные в стейт, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    if pd.validate_date_format(message.text):
        await state.update_data(user_id=message.from_user.id, start_date=message.text)
        await message.answer('Введите окончание периода', reply_markup=kb.create_back_main_menu_kb())
        await state.set_state(States.end_period_income)
    else:
        await message.answer('Не корректный ввод даты')


@router.message(StateFilter(States.end_period_income), F.text)
async def input_end_period_income_handler(message: types.Message, state: FSMContext) -> None:
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
        income = stat.get_sum_income(data)

        if income:
            await message.answer(f'Сумма ваших доходов за указанный период: {income}', reply_markup=kb.create_main_menu_kb())
            await state.clear()

        else:
            await message.answer('За указанный период дохода не было', reply_markup=kb.create_main_menu_kb())
            await state.clear()

    else:
        await message.answer('Не корректный ввод даты')


@router.callback_query(StateFilter(None), F.data == 'all_expense')
async def all_expense_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке "Общий расход за период"
    :return: None
    """
    await callback.message.answer('Введите начало периода в формате: год-месяц-день\nПример: 2025-01-01', reply_markup=kb.create_back_main_menu_kb())
    await callback.message.delete()
    await state.set_state(States.start_period_expense)
    await callback.answer()


@router.message(StateFilter(States.start_period_expense), F.text)
async def input_start_period_expense_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение пользователя (ввод старта периода), записывает данные в стейт, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    if pd.validate_date_format(message.text):
        await state.update_data(user_id=message.from_user.id, start_date=message.text)
        await message.answer('Введите окончание периода', reply_markup=kb.create_back_main_menu_kb())
        await state.set_state(States.end_period_expense)
    else:
        await message.answer('Не корректный ввод даты')


@router.message(StateFilter(States.end_period_expense), F.text)
async def input_end_period_expense_handler(message: types.Message, state: FSMContext) -> None:
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
        expense = stat.get_sum_expense(data)

        if expense:
            await message.answer(f'Сумма ваших расходов за указанный период: {expense}', reply_markup=kb.create_main_menu_kb())
            await state.clear()

        else:
            await message.answer('За указанный период расходов не было', reply_markup=kb.create_main_menu_kb())
            await state.clear()

    else:
        await message.answer('Не корректный ввод даты')


@router.callback_query(StateFilter(None), F.data == 'all_balance')
async  def all_balance_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке "Чистый баланс за период"
    :return: None
    """
    await callback.message.answer('Введите начало периода в формате: год-месяц-день\nПример: 2025-01-01', reply_markup=kb.create_back_main_menu_kb())
    await callback.message.delete()
    await state.set_state(States.start_period_balance)
    await callback.answer()


@router.message(StateFilter(States.start_period_balance), F.text)
async def input_start_period_balance_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение пользователя (ввод старта периода), записывает данные в стейт, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    if pd.validate_date_format(message.text):
        await state.update_data(user_id=message.from_user.id, start_date=message.text)
        await message.answer('Введите окончание периода', reply_markup=kb.create_back_main_menu_kb())
        await state.set_state(States.end_period_balance)
    else:
        await message.answer('Не корректный ввод даты')


@router.message(StateFilter(States.end_period_balance), F.text)
async def input_end_period_balance_handler(message: types.Message, state: FSMContext) -> None:
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
        balance = stat.get_balance(data)

        await message.answer(f'Чистый баланс за указанный период: {balance}', reply_markup=kb.create_main_menu_kb())
        await state.clear()

    else:
        await message.answer('Не корректный ввод даты')


@router.callback_query(StateFilter(None), F.data == 'structure_by_categories')
async def struct_by_category_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке "Структура по категориям"
    :return: None
    """
    await callback.message.answer('Введите начало периода в формате: год-месяц-день\nПример: 2025-01-01', reply_markup=kb.create_back_main_menu_kb())
    await callback.message.delete()
    await state.set_state(States.start_period_struct_by_category)
    await callback.answer()


@router.message(StateFilter(States.start_period_struct_by_category), F.text)
async def input_start_period_struct_by_category_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение пользователя (ввод старта периода), записывает данные в стейт, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    if pd.validate_date_format(message.text):
        await state.update_data(user_id=message.from_user.id, start_date=message.text)
        await message.answer('Введите окончание периода', reply_markup=kb.create_back_main_menu_kb())
        await state.set_state(States.end_period_struct_by_category)
    else:
        await message.answer('Не корректный ввод даты')


@router.message(StateFilter(States.end_period_struct_by_category), F.text)
async def input_end_period_struct_by_category_handler(message: types.Message, state: FSMContext) -> None:


    await message.answer('Структура расходов и доходов по категориям')
    await message.answer('Доходы:')

    await state.update_data(end_date=message.text)
    data = await state.get_data()
    income = stat.get_struct_income(message.from_user.id)
    expense = stat.get_struct_expense(message.from_user.id)
    sum_income = stat.get_sum_income(data)
    sum_expense = stat.get_sum_expense(data)

    if income:
        for row in income:
            await message.answer(f'{row[0]}: {row[1] / sum_income * 100:.2f}%  от общих доходов, сумма: {row[1]}')
    else:
        await message.answer('Записи о доходах отсутствуют')

    await message.answer('Расходы:')

    if expense:
        for row in expense:
            await message.answer(f'{row[0]}: {row[1] / sum_expense * 100:.2f}%  от общих расходов, сумма: {row[1]}', reply_markup=kb.create_main_menu_kb())
        await state.clear()

    else:
        await message.answer('Записи о расходах отсутствуют', reply_markup=kb.create_main_menu_kb())
        await state.clear()