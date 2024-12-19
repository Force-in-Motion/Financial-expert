from aiogram.fsm.state import StatesGroup, State




class States(StatesGroup):
    quantity_income = State()
    category_income = State()

    quantity_expense = State()
    category_expense = State()

    description = State()
    deposit = State()

    one_goal_menu = State()
    add_deposit = State()

