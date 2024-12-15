from aiogram.fsm.state import StatesGroup, State




class States(StatesGroup):
    quantity = State()
    category = State()
    date = State
