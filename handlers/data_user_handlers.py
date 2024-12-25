from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, types
from aiogram import F

from model.states import States
from model.db_operations import Users
from keyboards.keyboards import CreateKeyboard as kb
from utilits.processing_data import ProcessingData as pd

router = Router()
users = Users()

@router.message(F.text.lower() == 'регистрация')
@router.message(StateFilter(None), Command('register'))
async def register_handler(message: types.Message, state: FSMContext) -> None:
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
async def input_user_name_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду регистрации нового пользователяб Запрашивает пароль,
    обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    if not users.get_user_name(message.text, message.from_user.id):
        await state.update_data(username=message.text)
        await message.answer('Введите пароль')
        await state.set_state(States.add_password)
    else:
        await message.answer('Такое имя пользователя уже существует')


@router.message(StateFilter(States.add_password), F.text)
async def input_password_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.update_data(password=message.text)
    data = await state.get_data()
    users.add_user(data)
    await message.answer('Пользователь создан успешно, теперь авторизуйтесь\n', reply_markup=kb.create_main_menu_kb())
    await state.clear()
    await login_handler(message, state)


@router.message(F.text.lower() == 'авторизация')
@router.message(StateFilter(None), Command('login'))
async def login_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду входа нового, запрашивает логин, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await message.answer('Введите имя пользователя', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(States.enter_username)


@router.message(StateFilter(States.enter_username), F.text)
async def enter_user_name_handler(message: types.Message, state: FSMContext) -> None:
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
async def enter_password_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.update_data(password=message.text)
    data = await state.get_data()
    if users.authorization_user(data):
        await message.answer(f'Вы успешно авторизовались\n\n {pd.mess_menu}', reply_markup=kb.create_main_menu_kb())
        await state.clear()
    else:
        await message.answer('Не верный логин или пароль')
        await login_handler(message, state)


@router.message(F.text.lower() == 'редактировать пользователя')
@router.message(Command('edit_user'))
async def user_menu_handler(message: types.Message) -> None:
    """
    Обрабатывает команду входа в меню редактирования пользователя, меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await message.delete()
    await message.answer('Меню пользователя:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Выберите действие:', reply_markup=kb.create_process_user_data())


@router.callback_query(StateFilter(None), F.data == 'username')
async def edit_user_name_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке "Редактировать имя"
    :return: None
    """
    await callback.message.answer('Введите старое имя пользователя')
    await callback.message.delete()
    await state.set_state(States.old_username)
    await callback.answer()


@router.message(StateFilter(States.old_username), F.text)
async def input_old_user_name_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.update_data(user_id=message.from_user.id)
    if users.get_user_name(message.text, message.from_user.id):
        await state.update_data(oldname=message.text)
        await message.answer('Введите новое имя пользователя')
        await state.set_state(States.new_username)
    else:
        await message.answer('Такого имени пользователя нет в базе, введите другое')


@router.message(StateFilter(States.new_username), F.text)
async def input_new_user_name_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    if not users.get_user_name(message.text, message.from_user.id):
        await state.update_data(newname=message.text)
        data = await state.get_data()
        users.edit_user_name(data)
        await message.answer('Имя пользователя успешно изменено', reply_markup=kb.create_main_menu_kb())
        await state.clear()
    else:
        await message.answer('Такое имя пользователя уже занято, выберите другое')


@router.callback_query(StateFilter(None), F.data == 'password')
async def edit_user_password_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке "Редактировать пароль"
    :return: None
    """
    await callback.message.answer('Введите старый пароль')
    await callback.message.delete()
    await state.set_state(States.old_password)
    await callback.answer()


@router.message(StateFilter(States.old_password), F.text)
async def input_old_password_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.update_data(user_id=message.from_user.id)
    if users.get_user_password(message.text, message.from_user.id):
        await state.update_data(oldpassword=message.text)
        await message.answer('Введите новый пароль')
        await state.set_state(States.new_password)
    else:
        await message.answer('Такого пароля нет в базе, введите другой')


@router.message(StateFilter(States.new_password), F.text)
async def input_new_password_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.update_data(newpassword=message.text)
    data = await state.get_data()
    users.edit_user_password(data)
    await message.answer('Пароль пользователя успешно изменен', reply_markup=kb.create_main_menu_kb())
    await state.clear()

@router.callback_query(StateFilter(None), F.data == 'deluser')
async def del_user_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает клик по кнопке "Удалить пользователя"
    :return: None
    """
    await callback.message.answer('Введите имя пользователя для удаления')
    await callback.message.delete()
    await state.set_state(States.del_user)
    await callback.answer()


@router.message(StateFilter(States.del_user), F.text)
async def input_del_user_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает полученное сообщение пользователя, записывает в стейт и меняет стейт на новый
    :param message: Принимает сообщение пользователя
    :param state: Принимает состояние
    :return: None
    """
    await state.update_data(user_id=message.from_user.id)
    if users.get_user_name(message.text, message.from_user.id):
        await state.update_data(username=message.text)
        data = await state.get_data()
        users.del_user(data)
        await message.answer('Пользователь успешно удален')
        await state.clear()
    else:
        await message.answer('Такого пользователя нет в базе, укажите другое имя')