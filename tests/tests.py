import pytest
import sqlite3


@pytest.fixture
def db():
    """
    Создает фикстуры для тестирования
    :return:
    """
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Expense (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Goal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        required INTEGER NOT NULL,
        deposit INTEGER DEFAULT 0,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
    )
    """)

    yield cursor, connection

    connection.close()


def test_registration_with_existing_user_id(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (1, 'testuser', 'password123')")
    connection.commit()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (1, 'anotheruser', 'newpassword')")
        connection.commit()


def test_successful_registration(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (2, 'newuser', 'newpassword')")
    connection.commit()

    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()

    assert len(users) == 1
    assert users[0][1] == 2
    assert users[0][2] == 'newuser'


def test_authorization_with_correct_credentials(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (3, 'testuser', 'password123')")
    connection.commit()

    cursor.execute("SELECT * FROM Users WHERE username = 'testuser' AND password = 'password123'")
    user = cursor.fetchone()

    assert user is not None
    assert user[1] == 3


def test_authorization_with_incorrect_credentials(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (4, 'testuser', 'password123')")
    connection.commit()

    cursor.execute("SELECT * FROM Users WHERE username = 'testuser' AND password = 'wrongpassword'")
    user = cursor.fetchone()

    assert user is None


def test_add_expense(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (5, 'expenseuser', 'password123')")
    connection.commit()

    cursor.execute("INSERT INTO Expense (user_id, quantity, category, date) VALUES (5, 100, 'Food', '2023-10-10')")
    connection.commit()

    cursor.execute("SELECT * FROM Expense WHERE user_id = 5")
    expense = cursor.fetchone()

    assert expense is not None
    assert expense[1] == 5
    assert expense[2] == 100
    assert expense[3] == 'Food'


def test_add_income_without_category(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (6, 'incomeuser', 'password123')")
    connection.commit()

    cursor.execute("INSERT INTO Income (user_id, quantity, category, date) VALUES (6, 200, '', '2023-10-10')")
    connection.commit()

    cursor.execute("SELECT * FROM Income WHERE user_id = 6")
    income = cursor.fetchone()

    assert income is not None
    assert income[1] == 6
    assert income[2] == 200
    assert income[3] == ''


def test_view_transaction_history(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (7, 'historyuser', 'password123')")
    cursor.execute("INSERT INTO Expense (user_id, quantity, category, date) VALUES (7, 100, 'Travel', '2023-10-10')")
    connection.commit()

    cursor.execute("SELECT * FROM Expense WHERE category = 'NonExistentCategory'")
    history = cursor.fetchall()

    assert len(history) == 0


def test_set_goal(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (8, 'goaluser', 'password123')")
    connection.commit()

    cursor.execute("INSERT INTO Goal (user_id, description, required, date) VALUES (8, 'Save for vacation', 2000, '2023-12-31')")
    connection.commit()

    cursor.execute("SELECT * FROM Goal WHERE user_id = 8")
    goal = cursor.fetchone()

    assert goal is not None
    assert goal[2] == 'Save for vacation'
    assert goal[3] == 2000


def test_view_goals(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (9, 'viewgoaluser', 'password123')")
    cursor.execute("INSERT INTO Goal (user_id, description, required, date) VALUES (9, 'Save for car', 5000, '2023-12-31')")
    connection.commit()

    cursor.execute("SELECT * FROM Goal WHERE user_id = 9")
    goals = cursor.fetchall()

    assert len(goals) == 1
    assert goals[0][2] == 'Save for car'  # description


def test_goal_achievement(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (10, 'achievegoaluser', 'password123')")
    cursor.execute("INSERT INTO Goal (user_id, description, required, date) VALUES (10, 'Buy a house', 100000, '2023-12-31')")
    connection.commit()

    cursor.execute("UPDATE Goal SET deposit = 100000 WHERE user_id = 10")
    connection.commit()

    cursor.execute("SELECT * FROM Goal WHERE user_id = 10")
    goal = cursor.fetchone()

    assert goal is not None
    assert goal[4] >= goal[3]


def test_request_statistics(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (11, 'statsuser', 'password123')")
    cursor.execute("INSERT INTO Expense (user_id, quantity, category, date) VALUES (11, 100, 'Transport', '2023-10-10')")
    cursor.execute("INSERT INTO Income (user_id, quantity, category, date) VALUES (11, 500, 'Salary', '2023-10-10')")
    connection.commit()

    cursor.execute("SELECT SUM(quantity) FROM Expense WHERE date >= '2023-10-01'")
    total_expenses = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(quantity) FROM Income WHERE date >= '2023-10-01'")
    total_income = cursor.fetchone()[0]

    assert total_expenses == 100
    assert total_income == 500


def test_request_analysis_by_category(db):
    cursor, connection = db

    cursor.execute("INSERT INTO Users (user_id, username, password) VALUES (12, 'analysisuser', 'password123')")
    cursor.execute("INSERT INTO Expense (user_id, quantity, category, date) VALUES (12, 150, 'Food', '2023-10-05')")
    cursor.execute("INSERT INTO Expense (user_id, quantity, category, date) VALUES (12, 50, 'Transport', '2023-10-12')")
    connection.commit()

    cursor.execute("SELECT category, SUM(quantity) FROM Expense GROUP BY category")
    category_analysis = cursor.fetchall()

    assert len(category_analysis) == 2
    assert category_analysis[0][0] == 'Food' and category_analysis[0][1] == 150
    assert category_analysis[1][0] == 'Transport' and category_analysis[1][1] == 50