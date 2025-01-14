from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, types
from aiogram import F

from model.states import States
from model.logic_goals import Goal
from keyboards.keyboards import CreateKeyboard as kb

router = Router()
goal = Goal()



@router.message( F.text.lower() == 'меню целей')
@router.message(Command('goal'))
async def goals_menu_handler(message: types.Message) -> None:
    """
    Обрабатывает команду пользователя- переход в меню работы с целями
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :return: None
    """
    await message.answer('Меню целей', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Выберите требуемый раздел меню', reply_markup=kb.create_menu_goal_kb())


@router.callback_query(StateFilter(None), F.data == 'add_goal')
async def add_goal_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке 'Добавить цель'
    :return: None
    """
    await callback.message.answer('Введите короткое описание цели, например: На отпуск', reply_markup=kb.create_back_main_menu_kb())
    await state.set_state(States.add_description_goal)
    await callback.message.delete()
    await callback.answer()


@router.message(StateFilter(States.add_description_goal), F.text)
async def input_description_goal_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :param state: Состояние, находясь в котором бот реагирует на команду пользователя
    :return: None
    """
    await state.update_data(description=message.text, user_id=message.from_user.id)
    await message.answer('Введите сумму для депозита', reply_markup=kb.create_back_main_menu_kb())
    await state.set_state(States.add_required_goal)


@router.message(StateFilter(States.add_required_goal), F.text)
async def input_deposit_goal_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и затем извлекает из стейта
    :param message: Принимает текст сообщения, которое пользователь пишет в чат
    :param state: Состояние, находясь в котором бот реагирует на команду пользователя
    :return: None
    """
    if message.text.isdigit():
        await state.update_data(required=message.text)
        data = await state.get_data()
        goal.add_goal(data)
        await message.answer('Цель успешно создана', reply_markup=kb.create_main_menu_kb())
        await state.clear()
    else:
        await message.reply('Введите число!', reply_markup=kb.create_back_main_menu_kb())


@router.callback_query(F.data == 'my_goal')
async def my_goals_callback_handler(callback: types.CallbackQuery) -> None:
    """
    Обрабатывает клик по кнопке 'Мои цели'
    :return: None
    """
    await callback.message.answer('Войдите в требуемое меню', reply_markup=kb.create_menu_my_goals_kb())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(StateFilter(None), F.data == 'list_goal')
async def list_goals_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке 'Список целей'
    :return: None
    """
    user_id = callback.from_user.id
    if goal.get_all_description_goal(user_id):
        await callback.message.answer('Список активных целей', reply_markup=kb.create_list_goals_kb(user_id))
        await state.set_state(States.one_goal_menu)
    else:
        await callback.message.answer('Вы пока не добавили ни одну цель!', reply_markup=kb.create_back_main_menu_kb())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(StateFilter(States.one_goal_menu), F.data == 'del_goal')
async def del_goal_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке выбора цели для ее удаления
    :return: None
    """
    data = await state.get_data()
    goal.del_goal(data)
    await callback.message.answer('Цель успешно удалена', reply_markup=kb.create_main_menu_kb())
    await callback.message.delete()
    await state.clear()
    await callback.answer()


@router.callback_query(StateFilter(States.one_goal_menu), F.data == 'add_deposit')
async def add_deposit_goal_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке 'Добавить депозит'
    :return: None
    """
    await callback.message.answer('Введите сумму депозита', reply_markup=kb.create_back_main_menu_kb())
    await state.set_state(States.add_deposit)
    await callback.message.delete()
    await callback.answer()


@router.callback_query(StateFilter(States.one_goal_menu))
async def menu_one_goal_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке названия цели
    :return: None
    """
    await state.update_data(description=callback.data, user_id=callback.from_user.id)
    await callback.message.answer('Меню вашей цели', reply_markup=kb.create_menu_one_goal())
    await callback.message.delete()
    await callback.answer()


@router.message(StateFilter(States.add_deposit), F.text)
async def get_value_deposit_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение пользователя для добавления размера депозита
    :param state: Принимает состояние добавления депозита
    :param message: Ожидается число
    :return: None
    """
    if message.text.isdigit():
        await state.update_data(deposit=message.text, user_id=message.from_user.id)
        data = await state.get_data()
        goal.add_deposit(data)
        await message.answer('Депозит успешно добавлен', reply_markup=kb.create_main_menu_kb())
        if goal.check_accumulation(data):
            await message.answer('Вы успешно завершили накопление\n\n Цель достигнута и перенесена в раздел завершенных!')
            goal.transfers_in_completed_goals(data)
            goal.del_goal(data)
        await state.clear()
    else:
        await message.reply('Введите числовое значение', reply_markup=kb.create_back_main_menu_kb())


@router.callback_query(F.data == 'statistic_goal')
async def statistic_menu_callback_handler(callback: types.CallbackQuery) -> None:
    """
    Обрабатывает клик по кнопке "Показать статистику"
    :return: None
    """
    await callback.message.answer(text='Выберите интересующую вас статистику', reply_markup=kb.create_main_menu_statistic_goals())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == 'active')
async def active_goals_callback_handler(callback: types.CallbackQuery) -> None:
    """
    Обрабатывает клик по кнопке "Активные цели"
    :return: None
    """
    user_id = callback.from_user.id
    await callback.message.answer(text='Статистика активных целей')
    await callback.message.delete()
    data = goal.get_all_data_goal(user_id)
    if data:
        for row in data:
            if row[4] != 0:
                await callback.message.answer(text=f'Цель накопления: {row[2]}\n Требуемая сумма: {row[3]}\n '
                f'Накопления: {row[4]}\n Процент накопления: {row[4] / row[3] * 100:.2f}\n Остаток: {row[3] - row[4]}\n',
                reply_markup=kb.create_main_menu_kb())
                await callback.answer()
            else:
                await callback.message.answer('Вы пока не добавили ни одного взноса, процент посчитать невозможно', reply_markup=kb.create_main_menu_kb())
                await callback.answer()
    else:
        await callback.message.answer('Активные цели отсутствуют, для начала добавьте их', reply_markup=kb.create_main_menu_kb())
        await callback.answer()


@router.callback_query(F.data == 'finished')
async def finished_goals_callback_handler(callback: types.CallbackQuery) -> None:
    """
    Обрабатывает клик по кнопке "Завершенные цели"
    :return: None
    """
    user_id = callback.from_user.id
    await callback.message.answer(text='Статистика завершенных целей')
    await callback.message.delete()
    data = goal.get_all_data_completed_goal(user_id)

    if data:
        for row in data:
            await callback.message.answer(text=f'Цель накопления: {row[2]}\n Требуемая сумма: {row[3]}\n '
            f'Накопления: {row[4]}\n Процент накопления: {row[4] / row[3] * 100}\n Остаток: {row[3] - row[4]}\n',
            reply_markup=kb.create_main_menu_kb())
            await callback.answer()
    else:
        await callback.message.answer('Вы пока не завершили ни одной цели', reply_markup=kb.create_main_menu_kb())
        await callback.answer()