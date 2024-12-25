from aiogram.fsm.state import StatesGroup, State




class States(StatesGroup):
    add_username = State()
    add_password = State()

    enter_username = State()
    enter_password = State()

    old_username = State()
    new_username = State()

    old_password = State()
    new_password = State()

    del_username = State()

    quantity_income = State()
    category_income = State()

    quantity_expense = State()
    category_expense = State()

    description = State()
    required = State()

    one_goal_menu = State()
    add_deposit = State()

