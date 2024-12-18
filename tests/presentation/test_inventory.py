import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from presentation.inventory import InventoryWindow, AddInventoryWindow, UpdateInventoryWindow, DeleteInventoryWindow, ListInventoryWindow
from business.inventory_logic import add_inventory_item, update_inventory_item, delete_inventory_item, get_inventory_items


class TestInventoryWindow(unittest.TestCase):

    @patch('presentation.inventory.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.inventory.AddInventoryWindow')  # Mock AddInventoryWindow
    @patch('presentation.inventory.UpdateInventoryWindow')  # Mock UpdateInventoryWindow
    @patch('presentation.inventory.DeleteInventoryWindow')  # Mock DeleteInventoryWindow
    @patch('presentation.inventory.ListInventoryWindow')  # Mock ListInventoryWindow
    def test_inventory_window_buttons(self, mock_list_inventory_window, mock_delete_inventory_window, mock_update_inventory_window, mock_add_inventory_window, mock_showerror):
        root = tk.Tk()
        app = InventoryWindow(root)

        # Simulate button clicks for inventory operations
        app.add_inventory()
        app.update_inventory()
        app.delete_inventory()
        app.list_inventories()

        # Check if the appropriate windows were opened
        mock_add_inventory_window.assert_called_once()
        mock_update_inventory_window.assert_called_once()
        mock_delete_inventory_window.assert_called_once()
        mock_list_inventory_window.assert_called_once()


class TestAddInventoryWindow(unittest.TestCase):

    @patch('presentation.inventory.messagebox.showerror')  # Mock messagebox.showerror
    def test_add_inventory_invalid_input(self, mock_showerror):
        root = tk.Tk()
        app = AddInventoryWindow(root)

        # Simulate invalid quantity and cost
        app.item_name_entry.insert(0, "Item 1")
        app.quantity_entry.insert(0, "invalid")
        app.cost_entry.insert(0, "5.5")
        app.restock_date_entry.insert(0, "2024-12-01")

        # Call submit_inventory method
        app.submit_inventory()

        # Check if the error message for invalid input was shown
        mock_showerror.assert_called_with("Input Error", "Please enter valid numerical values for quantity and cost.")

class TestListInventoryWindow(unittest.TestCase):

    @patch('presentation.inventory.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.inventory.get_inventory_items')  # Mock get_inventory_items
    def test_list_inventory(self, mock_get_inventory_items, mock_showerror):
        # Simulate fetching inventory items, including the 'restock_date' field
        mock_get_inventory_items.return_value = [
            {"item_name": "Item 1", "quantity": 10, "cost": 5.0, "restock_date": "2024-12-01"}
        ]

        root = tk.Tk()
        app = ListInventoryWindow(root)

        # Check if the inventory items are listed correctly
        self.assertEqual(app.items[0]["item_name"], "Item 1")
        self.assertEqual(app.items[0]["quantity"], 10)
        self.assertEqual(app.items[0]["restock_date"], "2024-12-01")

    @patch('presentation.inventory.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.inventory.get_inventory_items')  # Mock get_inventory_items
    def test_no_inventory_found(self, mock_get_inventory_items, mock_showerror):
        # Simulate no inventory items found
        mock_get_inventory_items.return_value = []

        root = tk.Tk()
        app = ListInventoryWindow(root)

        # Check if the error message is shown
        mock_showerror.assert_called_with("Error", "No inventory items found.")

if __name__ == '__main__':
    unittest.main()
