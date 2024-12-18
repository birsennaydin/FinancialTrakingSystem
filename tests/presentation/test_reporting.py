import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from presentation.reporting import ReportWindow
from business.reporting_logic import get_all_expenses_list, get_inventory_items_list, get_sales_history_with_user


class TestReportWindow(unittest.TestCase):

    @patch('presentation.reporting.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.reporting.get_all_expenses_list')  # Mock get_all_expenses_list
    def test_generate_expense_report(self, mock_get_all_expenses_list, mock_showerror):
        # Simulate fetching expenses
        mock_get_all_expenses_list.return_value = [
            {"username": "john", "category": "Food", "description": "Lunch", "amount": 10.0},
            {"username": "jane", "category": "Transport", "description": "Bus fare", "amount": 3.0}
        ]

        root = tk.Tk()
        app = ReportWindow(root)

        # Simulate generating the expense report
        app.generate_expense_report()

        # Check if the report was generated and the messagebox was not called with an error
        mock_showerror.assert_not_called()

    @patch('presentation.reporting.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.reporting.get_inventory_items_list')  # Mock get_inventory_items_list
    def test_generate_inventory_report(self, mock_get_inventory_items_list, mock_showerror):
        # Simulate fetching inventory items
        mock_get_inventory_items_list.return_value = [
            {"item_name": "Item 1", "quantity": 10, "cost": 5.0, "restock_date": "2024-12-01"},
            {"item_name": "Item 2", "quantity": 20, "cost": 3.0, "restock_date": "2024-12-02"}
        ]

        root = tk.Tk()
        app = ReportWindow(root)

        # Simulate generating the inventory report
        app.generate_inventory_report()

        # Check if the report was generated and the messagebox was not called with an error
        mock_showerror.assert_not_called()

    @patch('presentation.reporting.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.reporting.get_sales_history_with_user')  # Mock get_sales_history_with_user
    def test_generate_sales_report(self, mock_get_sales_history_with_user, mock_showerror):
        # Simulate fetching sales data
        mock_get_sales_history_with_user.return_value = [
            {"username": "john", "item_name": "Item 1", "quantity": 2, "amount": 10.0, "sale_date": "2024-12-01"},
            {"username": "jane", "item_name": "Item 2", "quantity": 3, "amount": 15.0, "sale_date": "2024-12-02"}
        ]

        root = tk.Tk()
        app = ReportWindow(root)

        # Simulate generating the sales report
        app.generate_sales_report()

        # Check if the report was generated and the messagebox was not called with an error
        mock_showerror.assert_not_called()


if __name__ == '__main__':
    unittest.main()
