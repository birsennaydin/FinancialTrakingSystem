import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from presentation.sales import SalesTrackingWindow, RecordSaleWindow, SalesHistoryWindow, TrackDailyRevenueWindow
from business.sales_logic import record_sale, get_sales_history, get_daily_revenue
from business.inventory_logic import get_inventory_items


class TestSalesTrackingWindow(unittest.TestCase):

    @patch('presentation.sales.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.sales.RecordSaleWindow')  # Mock RecordSaleWindow
    @patch('presentation.sales.SalesHistoryWindow')  # Mock SalesHistoryWindow
    @patch('presentation.sales.TrackDailyRevenueWindow')  # Mock TrackDailyRevenueWindow
    def test_sales_tracking_window_buttons(self, mock_track_daily_revenue_window, mock_sales_history_window, mock_record_sale_window, mock_showerror):
        root = tk.Tk()
        app = SalesTrackingWindow(root, user_id=1)

        # Simulate button clicks for recording a sale, viewing sales history, and tracking daily revenue
        app.record_sale()
        app.view_sales_history()
        app.track_daily_revenue()

        # Check if the appropriate windows were opened
        mock_record_sale_window.assert_called_once()
        mock_sales_history_window.assert_called_once()
        mock_track_daily_revenue_window.assert_called_once()

class TestSalesHistoryWindow(unittest.TestCase):

    @patch('presentation.sales.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.sales.get_sales_history')  # Mock get_sales_history
    def test_sales_history(self, mock_get_sales_history, mock_showerror):
        # Simulate fetching sales history
        mock_get_sales_history.return_value = [
            {"username": "john", "item_name": "Item 1", "quantity": 5, "amount": 25.00, "sale_date": "2024-12-01"},
            {"username": "jane", "item_name": "Item 2", "quantity": 3, "amount": 15.00, "sale_date": "2024-12-02"}
        ]

        root = tk.Tk()
        app = SalesHistoryWindow(root)

        # Check if the sales history is displayed correctly
        self.assertEqual(app.sales[0]["username"], "john")
        self.assertEqual(app.sales[1]["item_name"], "Item 2")
        self.assertEqual(app.sales[1]["amount"], 15.00)

    @patch('presentation.sales.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.sales.get_sales_history')  # Mock get_sales_history
    def test_no_sales_history_found(self, mock_get_sales_history, mock_showerror):
        # Simulate no sales found
        mock_get_sales_history.return_value = []

        root = tk.Tk()
        app = SalesHistoryWindow(root)

        # Check if the error message for no sales history was shown
        mock_showerror.assert_called_with("Error", "No sales history found.")

if __name__ == '__main__':
    unittest.main()
