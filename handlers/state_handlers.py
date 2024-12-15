import asyncio
import aiogram
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Router, types
from aiogram import F

from model.data_state import States
from keyboards.keyboards import CreateKeyboard as cb
from service.service_data import SaveLoadData as sld
from model.db_operations import Income

router = Router()
income = Income()

@router.message(StateFilter(None), F.text.lower() == 'добавить доход')
@router.message(StateFilter(None), Command('add_income'))
async def input_quantity_income_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer('Введите сумму своего дохода')
    await state.set_state(States.quantity)


@router.message(StateFilter(States.quantity), F.text)
async def input_category_income_handler(message: types.Message, state: FSMContext) -> None:
    await state.update_data(quantity=message.text)
    await message.answer('Выберите категорию', reply_markup=cb.create_category_kb())
    await state.set_state(States.category)


@router.callback_query(StateFilter(States.category), F.data.in_(sld.get_sample()))
async def push_category_income_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(category=callback.data)
    get_data = await state.get_data()
    income.add_income(get_data)
    await callback.message.answer('Ваши данные успешно сохранены')
    await callback.answer()


