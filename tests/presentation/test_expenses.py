import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from presentation.expenses import ExpenseWindow, RecordExpenseWindow, ListExpensesWindow


class TestExpenseWindow(unittest.TestCase):

    @patch('presentation.expenses.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.expenses.record_expense')  # Mock record_expense
    @patch('presentation.expenses.get_categories')  # Mock get_categories to simulate categories
    @patch('presentation.expenses.get_category_id_by_name')  # Mock get_category_id_by_name to simulate category ID retrieval
    def test_record_expense(self, mock_get_category_id_by_name, mock_get_categories, mock_record_expense, mock_showerror):
        # Simulate categories and category ID
        mock_get_categories.return_value = [{"name": "Food"}, {"name": "Transport"}]
        mock_get_category_id_by_name.return_value = 1  # Assume the category ID for "Food" is 1
        mock_record_expense.return_value = "Expense recorded successfully."

        root = tk.Tk()
        app = RecordExpenseWindow(root, user_id=1)

        # Simulate user input
        app.category_var.set("Food")
        app.description_entry.insert(0, "Lunch")
        app.amount_entry.insert(0, "10.5")

        # Call submit_expense method
        app.submit_expense()

        # Check if record_expense was called with correct arguments
        mock_record_expense.assert_called_with(1, 1, "Lunch", 10.5)  # user_id, category_id, description, amount

        # Check if the success message was shown
        mock_showerror.assert_called_with("Expense Recorded", "Expense has been successfully recorded.")

    @patch('presentation.expenses.messagebox.showerror')  # Mock messagebox.showerror
    def test_record_expense_invalid_input(self, mock_showerror):
        root = tk.Tk()
        app = RecordExpenseWindow(root, user_id=1)

        # Simulate missing description and amount
        app.category_var.set("Food")
        app.description_entry.insert(0, "")  # Empty description
        app.amount_entry.insert(0, "")  # Empty amount

        # Call submit_expense method
        app.submit_expense()

        # Check if showerror was called for input validation
        mock_showerror.assert_called_with("Input Error", "All fields must be filled out.")


class TestListExpensesWindow(unittest.TestCase):

    @patch('presentation.expenses.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.expenses.get_all_expenses')  # Mock get_all_expenses to simulate fetching expenses
    def test_list_expenses(self, mock_get_all_expenses, mock_showerror):
        # Simulate fetching expenses
        mock_get_all_expenses.return_value = [
            {"username": "john", "category": "Food", "description": "Lunch", "amount": 10.5},
            {"username": "jane", "category": "Transport", "description": "Bus fare", "amount": 3.0}
        ]

        root = tk.Tk()
        app = ListExpensesWindow(root)

        # Check if expenses are displayed correctly in the window
        self.assertEqual(app.expenses[0]["username"], "john")
        self.assertEqual(app.expenses[1]["category"], "Transport")
        self.assertEqual(app.expenses[1]["amount"], 3.0)

    @patch('presentation.expenses.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.expenses.get_all_expenses')  # Mock get_all_expenses to simulate no expenses
    def test_no_expenses_found(self, mock_get_all_expenses, mock_showerror):
        # Simulate no expenses found
        mock_get_all_expenses.return_value = []

        root = tk.Tk()
        app = ListExpensesWindow(root)

        # Check if the error message is shown when no expenses are found
        mock_showerror.assert_called_with("Error", "No expenses found.")


class TestExpenseWindow(unittest.TestCase):

    @patch('presentation.expenses.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.expenses.RecordExpenseWindow')  # Mock RecordExpenseWindow
    @patch('presentation.expenses.ListExpensesWindow')  # Mock ListExpensesWindow
    def test_expense_window_buttons(self, mock_list_expenses_window, mock_record_expense_window, mock_showerror):
        root = tk.Tk()
        app = ExpenseWindow(root, user_id=1)

        # Simulate button clicks for recording an expense and listing expenses
        app.record_expense()
        app.list_expenses()

        # Check if the appropriate windows were called
        mock_record_expense_window.assert_called_once()
        mock_list_expenses_window.assert_called_once()


if __name__ == '__main__':
    unittest.main()
