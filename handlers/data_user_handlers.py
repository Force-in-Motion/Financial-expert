from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, types
from aiogram import F
from jinja2.async_utils import auto_await

from model.states import States
from model.db_operations import Users
from keyboards.keyboards import CreateKeyboard as kb

router = Router()
users = Users()

@router.message(F.text.lower() == 'регистрация')
@router.message(StateFilter(None), Command('register'))
async def register_user_name_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду регистрации нового пользователя, запрашивает логин, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await message.answer('Введите имя пользователя', reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(States.add_username)


@router.message(StateFilter(States.add_username), F.text)
async def register_password_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду регистрации нового пользователяб Запрашивает пароль,
    обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.update_data(username=message.text)
    await message.answer('Введите пароль')
    await state.set_state(States.add_password)


@router.message(StateFilter(States.add_password), F.text)
async def creating_finished_register_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.update_data(password=message.text)
    data = await state.get_data()
    users.add_user(data)
    await message.answer('Пользователь создан успешно', reply_markup=kb.create_main_menu_kb())
    await state.clear()


@router.message(F.text.lower() == 'Авторизация')
@router.message(StateFilter(None), Command('login'))
async def enter_user_name_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду входа нового, запрашивает логин, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await message.answer('Введите имя пользователя', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(States.enter_username)


@router.message(StateFilter(States.enter_username), F.text)
async def enter_password_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду входа нового, запрашивает пароль, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.update_data(username=message.text)
    await message.answer('Введите пароль')
    await state.set_state(States.enter_password)


@router.message(StateFilter(States.enter_password), F.text)
async def creating_finished_data_login_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.update_data(password=message.text)
    data = await state.get_data()
    if users.authorization_user(data):
        await message.answer('Вы успешно авторизовались', reply_markup=kb.create_main_menu_kb())
        await message.answer('Меню пользователя', reply_markup=kb.create_process_user_data())
        await state.clear()
    else:
        await message.answer('Не верный логин или пароль')
        await enter_user_name_handler(message, state)


@router.message(F.text.lower() == 'Редактировать пользователя')
@router.message(StateFilter(None), F.text)
async def user_menu_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду входа в меню редактирования пользователя, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    


@router.callback_query(F.data == 'username')
async def edit_username_callback_handler(callback: types.CallbackQuery) -> None:
    """
    Обрабатывает клик по кнопке "Редактировать имя"
    :return: None
    """
    await callback.message.answer('Введите новое имя пользователя')
    await callback.message.delete()