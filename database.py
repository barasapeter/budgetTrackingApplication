import sqlite3
import os
import random, string


if not os.path.exists('./database'):
    os.mkdir('database')

# Create or connect to the database
conn = sqlite3.connect('database/finance.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS Users
             (Username TEXT PRIMARY KEY, Password TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Account
             (Username TEXT PRIMARY KEY, Currency TEXT, Savings_plan TEXT,
              Total_income REAL, Income_balance REAL, Savings_goal REAL,
              Savings_balance REAL, Savings_status TEXT,
              FOREIGN KEY (Username) REFERENCES Users(Username))''')

c.execute('''CREATE TABLE IF NOT EXISTS Expenses
             (ID TEXT PRIMARY KEY,
              Username TEXT,
              Description TEXT,
              Category TEXT,
              Amount REAL,
              Date TEXT,
              FOREIGN KEY (Username) REFERENCES Users(Username))''')

conn.commit()
# c.execute('drop table Expenses')

# CRUD operations
# Test passed
def create_user(username, password):
    return_message = {
        'is_successful': None,
        'message': None
    }
    try:
        c.execute("INSERT INTO Users VALUES (?, ?)", (username, password))
        conn.commit()
        return_message['is_successful'] = True
        return_message['message'] = 'Account created successfully'
    except sqlite3.IntegrityError:
        return_message['is_successful'] = False
        return_message['message'] = 'Account not created. Please try using another username'
    return return_message

# Test passed
def get_user(username, password):
    c.execute("SELECT * FROM Users WHERE Username=? AND Password=?", (username, password))
    return c.fetchone()

def update_user_password(username, new_password):
    c.execute("UPDATE Users SET Password=? WHERE Username=?", (new_password, username))
    conn.commit()

def delete_user(username):
    c.execute("DELETE FROM Users WHERE Username=?", (username,))
    conn.commit()

def create_account(username, currency, savings_plan, total_income, income_balance, savings_goal, savings_balance, savings_status):
    income_balance = income_balance

    c.execute("INSERT INTO Account VALUES (?, ?, ?, ROUND(?, 2), ROUND(?, 2), ROUND(?, 2), ROUND(?, 2), ?)",
          (username, currency, savings_plan, total_income, income_balance, savings_goal, savings_balance, savings_status))
    conn.commit()

def get_account(username):
    c.execute("SELECT * FROM Account WHERE Username=?", (username,))
    return c.fetchone()

def get_savings_balance(username):
    # Query to retrieve the savings balance for the given username
    c.execute("SELECT Savings_balance FROM Account WHERE Username = ?", (username,))
    row = c.fetchone()
    if row:
        # Extract and return the savings balance
        savings_balance = row[0]
        return savings_balance
    else:
        print('Nothing fetched!!!!!!!!!!!!!!!!')

def update_account(username, **kwargs):
    update_fields = ", ".join([f"{k}=?" for k in kwargs.keys()])
    values = tuple(kwargs.values())
    c.execute(f"UPDATE Account SET {update_fields} WHERE Username=?", values + (username,))
    conn.commit()

def update_income_balance(username, new_income_balance):
    c.execute("UPDATE Account SET Income_balance = ? WHERE Username = ?", (new_income_balance, username))
    conn.commit()

def update_savings_goal_amount(username, new_savings_goal_amount):
    c.execute('UPDATE Account SET Savings_goal = ? WHERE Username = ?', (new_savings_goal_amount, username))
    conn.commit()

def update_saving_status(username, new_savings_goal_amount):
    savings_balance = get_savings_balance(username)
    # Determine savings status based on savings goal and balance
    if savings_balance <= float(new_savings_goal_amount):
        savings_status = "Still Saving"
    else:
        savings_status = "Goal Achieved"
    c.execute('UPDATE Account SET Savings_status = ? WHERE Username = ?', (savings_status, username))
    conn.commit()



def add_expense(username, description, category, amount, date):
    c.execute("INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?)",
              (''.join([random.choice(string.digits+string.ascii_lowercase+string.ascii_uppercase) for i in range(10)]), username, description, category, amount, date))
    conn.commit()

def get_expenses(username):
    c.execute("SELECT * FROM Expenses WHERE Username=?", (username,))
    return c.fetchall()

# (ID TEXT PRIMARY KEY,
#               Username TEXT,
#               Description TEXT,
#               Category TEXT,
#               Amount REAL,
#               Date TEXT,)
def fetch_recent_expenses(username):
    c.execute('SELECT ID, Description, Category, Amount, Date FROM Expenses WHERE Username=?', (username,))
    return c.fetchall()


# Test the functions
if __name__ == '__main__':
    print(fetch_recent_expenses('BARASA'))

