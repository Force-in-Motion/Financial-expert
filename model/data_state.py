from aiogram.fsm.state import StatesGroup, State




class States(StatesGroup):
    quantity_income = State()
    category_income = State()

    quantity_expense = State()
    category_expense = State()