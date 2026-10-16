import sqlite3
from datetime import datetime

DB_NAME = "expenses.db"

def initialize_db():
    """Initializes the database and creates the expenses table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(amount, category, description, date=None):
    """Adds a new expense to the database."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (amount, category, date, description)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, date, description))
    conn.commit()
    conn.close()

def get_all_expenses():
    """Retrieves all expenses from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_expense(expense_id):
    """Deletes an expense by its ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def get_summary(month=None):
    """Returns the total spending, optionally filtered by month (MM)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if month:
        # Filter by the month part of the ISO date (YYYY-MM-DD)
        # month should be a string like "01", "10", etc.
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%m', date) = ?", (month.zfill(2),))
    else:
        cursor.execute('SELECT SUM(amount) FROM expenses')
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0.0
