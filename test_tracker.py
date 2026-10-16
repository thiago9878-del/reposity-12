import unittest
import os
import sqlite3
from database import initialize_db, add_expense, get_all_expenses, delete_expense, get_summary, DB_NAME

class TestExpenseTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a separate test database
        cls.original_db = DB_NAME
        import database
        database.DB_NAME = "test_expenses.db"
        cls.test_db = database.DB_NAME

    def setUp(self):
        # Initialize/clear the test database before each test
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        initialize_db()

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_and_get_expenses(self):
        add_expense(10.0, "Test", "Desc", "2023-01-01")
        expenses = get_all_expenses()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0][1], 10.0)
        self.assertEqual(expenses[0][2], "Test")

    def test_delete_expense(self):
        add_expense(20.0, "Delete", "Remove me")
        expenses = get_all_expenses()
        expense_id = expenses[0][0]
        result = delete_expense(expense_id)
        self.assertTrue(result)
        self.assertEqual(len(get_all_expenses()), 0)

    def test_get_summary(self):
        add_expense(10.0, "Cat1", "Desc1")
        add_expense(25.5, "Cat2", "Desc2")
        self.assertEqual(get_summary(), 35.5)

    def test_get_summary_filtered(self):
        add_expense(10.0, "Jan", "New Year", "2023-01-15")
        add_expense(50.0, "Feb", "Valentine", "2023-02-14")
        add_expense(20.0, "Feb", "Misc", "2023-02-28")
        self.assertEqual(get_summary("01"), 10.0)
        self.assertEqual(get_summary("02"), 70.0)
        self.assertEqual(get_summary("03"), 0.0)

if __name__ == "__main__":
    unittest.main()
