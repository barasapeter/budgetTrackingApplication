import unittest
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import create_user, get_user, update_user_password, delete_user, create_account, get_account, update_account, add_expense, get_expenses


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE Users
                         (Username TEXT PRIMARY KEY, Password TEXT)''')
        self.c.execute('''CREATE TABLE Account
                         (Username TEXT PRIMARY KEY, Currency TEXT, Savings_plan TEXT,
                          Total_income REAL, Income_balance REAL, Savings_goal REAL,
                          Savings_balance REAL, Savings_status TEXT)''')
        self.c.execute('''CREATE TABLE Expenses
                         (Username TEXT, Description TEXT, Category TEXT, Amount REAL, Date TEXT)''')

    def test_create_user(self):
        create_user('testuser', 'password')
        self.c.execute("SELECT * FROM Users WHERE Username='testuser'")
        user = self.c.fetchone()
        self.assertEqual(user, ('testuser', 'password'))

    def test_get_user(self):
        self.c.execute("INSERT INTO Users VALUES ('testuser', 'password')")
        user = get_user('testuser')
        self.assertEqual(user, ('testuser', 'password'))

    def test_update_user_password(self):
        self.c.execute("INSERT INTO Users VALUES ('testuser', 'password')")
        update_user_password('testuser', 'newpassword')
        self.c.execute("SELECT Password FROM Users WHERE Username='testuser'")
        password = self.c.fetchone()[0]
        self.assertEqual(password, 'newpassword')

    def test_delete_user(self):
        self.c.execute("INSERT INTO Users VALUES ('testuser', 'password')")
        delete_user('testuser')
        self.c.execute("SELECT * FROM Users WHERE Username='testuser'")
        user = self.c.fetchone()
        self.assertIsNone(user)

    def test_create_account(self):
        create_account('testuser', 'USD', 'Monthly')
        self.c.execute("SELECT * FROM Account WHERE Username='testuser'")
        account = self.c.fetchone()
        self.assertEqual(account, ('testuser', 'USD', 'Monthly', 0, 0, 0, 0, 'Healthy'))

    def test_get_account(self):
        self.c.execute("INSERT INTO Account VALUES ('testuser', 'USD', 'Monthly', 1000, 500, 2000, 1000, 'Healthy')")
        account = get_account('testuser')
        self.assertEqual(account, ('testuser', 'USD', 'Monthly', 1000, 500, 2000, 1000, 'Healthy'))

    def test_update_account(self):
        self.c.execute("INSERT INTO Account VALUES ('testuser', 'USD', 'Monthly', 1000, 500, 2000, 1000, 'Healthy')")
        update_account('testuser', Total_income=2000, Savings_goal=3000)
        self.c.execute("SELECT Total_income, Savings_goal FROM Account WHERE Username='testuser'")
        result = self.c.fetchone()
        self.assertEqual(result, (2000, 3000))

    def test_add_expense(self):
        add_expense('testuser', 'Groceries', 'Food', 50, '2023-04-01')
        self.c.execute("SELECT * FROM Expenses WHERE Username='testuser'")
        expense = self.c.fetchone()
        self.assertEqual(expense, ('testuser', 'Groceries', 'Food', 50, '2023-04-01'))

    def test_get_expenses(self):
        self.c.execute("INSERT INTO Expenses VALUES ('testuser', 'Groceries', 'Food', 50, '2023-04-01')")
        self.c.execute("INSERT INTO Expenses VALUES ('testuser', 'Rent', 'Housing', 1000, '2023-04-01')")
        expenses = get_expenses('testuser')
        self.assertEqual(len(expenses), 2)
        self.assertIn(('testuser', 'Groceries', 'Food', 50, '2023-04-01'), expenses)
        self.assertIn(('testuser', 'Rent', 'Housing', 1000, '2023-04-01'), expenses)

if __name__ == '__main__':
    unittest.main()