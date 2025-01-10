from aiogram.fsm.state import StatesGroup, State




class States(StatesGroup):
    """
    Содержит состояния
    """
    add_username = State()
    add_password = State()

    enter_username = State()
    enter_password = State()

    old_username = State()
    new_username = State()

    old_password = State()
    new_password = State()

    del_user = State()

    quantity_income = State()
    category_income = State()

    quantity_expense = State()
    category_expense = State()

    add_description_goal = State()
    add_required_goal = State()

    one_goal_menu = State()
    add_deposit = State()

    start_period_transactions = State()
    end_period_transactions = State()

    search_transaction_by_category = State()

    start_period_result = State()
    end_period_result = State()

    start_period_income = State()
    end_period_income = State()

    start_period_expense = State()
    end_period_expense = State()

    start_period_balance = State()
    end_period_balance = State()

    start_period_struct_by_category_text = State()
    end_period_struct_by_category_text = State()

    start_period_struct_by_category_view_column = State()
    end_period_struct_by_category_view_column = State()

    start_period_visual_circle = State()
    end_period_visual_circle = State()

    start_period_cost_category = State()
    end_period_cost_category = State()


