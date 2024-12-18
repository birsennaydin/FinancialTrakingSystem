import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from presentation.users import UpdateUserWindow
from business.user_logic import get_user_info


class TestUpdateUserWindow(unittest.TestCase):

    @patch('presentation.users.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.users.get_user_info')  # Mock get_user_info to simulate user info retrieval
    def test_load_user_info(self, mock_get_user_info, mock_showerror):
        self.role = "Admin"
        # Simulate user info retrieval
        mock_get_user_info.return_value = {"name": "Birsen", "username": "birsen.aydin", "email": "birsenn@example.com", "role": "Admin"}

        root = tk.Tk()
        app = UpdateUserWindow(root, 'Admin', 'birsen.aydin')

        # Trigger layout and ensure widgets are initialized
        root.update_idletasks()  # Ensure that all widgets, including OptionMenu, are initialized

        # Access the selected_user after the layout is initialized
        app.selected_user.set('birsen.aydin')

        # Now call load_user_info to populate the form fields
        app.load_user_info()

        # Check if the name entry is populated correctly
        self.assertEqual(app.name_entry.get(), "Birsen")
        self.assertEqual(app.username_entry.get(), "birsen.aydin")
        self.assertEqual(app.email_entry.get(), "birsenn@example.com")


if __name__ == '__main__':
    unittest.main()
