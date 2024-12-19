import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import messagebox
from presentation.application import Application
from business.user_logic import authenticate_user


class TestApplication(unittest.TestCase):

    @patch('presentation.application.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.application.authenticate_user')  # Mock authenticate_user
    def test_empty_username(self, mock_authenticate_user, mock_showerror):
        # Create the Tkinter root window and application instance
        root = tk.Tk()
        app = Application(root)

        # Leave the username empty and set a password
        app.username_entry.insert(0, "")  # Empty username
        app.password_entry.insert(0, "password")

        # Call the submit_login method
        app.submit_login()

        # Assert that showerror was called with the expected error message for empty username
        mock_showerror.assert_called_with("Input Error", "Username and password cannot be empty.")

    @patch('presentation.application.messagebox.showerror')  # Mock messagebox.showerror to prevent actual error popups
    @patch('presentation.application.authenticate_user')  # Mock authenticate_user to simulate authentication behavior
    def test_empty_password(self, mock_authenticate_user,mock_showerror):
        # Create the Tkinter root window and the application instance
        root = tk.Tk()
        app = Application(root)

        # Simulate empty password field by mocking the get method of the password entry
        app.username_entry.insert(0, "testuser")  # Set a test username
        app.password_entry.insert(0, "")  # Leave the password field empty

        # Call the submit_login method
        app.submit_login()

        # Check if showerror was called with the expected error message for empty fields
        mock_showerror.assert_called_with("Input Error", "Username and password cannot be empty.")

    @patch('presentation.application.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.application.authenticate_user')  # Mock authenticate_user
    def test_invalid_login(self, mock_authenticate_user, mock_showerror):
        # Simulate an invalid login attempt
        mock_authenticate_user.return_value = None  # Mock authentication failure

        # Create the Tkinter root window and the application instance
        root = tk.Tk()
        app = Application(root)

        # Set the username and password for invalid login
        app.username_entry.insert(0, "testuser")
        app.password_entry.insert(0, "wrongpassword")

        # Call the submit_login method
        app.submit_login()

        # Check if the showerror method was called with the appropriate error message
        mock_showerror.assert_called_with("Login Failed", "Invalid username or password!")

    @patch('presentation.application.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.application.authenticate_user')  # Mock authenticate_user
    def test_valid_login(self, mock_authenticate_user, mock_showerror):
        # Simulate successful authentication
        mock_authenticate_user.return_value = ('Admin', 1)  # Simulate 'Admin' role with user ID 1

        # Create the Tkinter root window and application instance
        root = tk.Tk()
        app = Application(root)

        # Set valid username and password
        app.username_entry.insert(0, "testuser")
        app.password_entry.insert(0, "correctpassword")

        # Call the submit_login method
        app.submit_login()

        # Check that the showerror was not called (login should succeed)
        mock_showerror.assert_not_called()

        # Assert the logged-in user ID is correctly set
        self.assertEqual(app.get_logged_in_user_id(), 1)

    @patch('presentation.application.messagebox.showerror')  # Mock messagebox.showerror
    @patch('presentation.application.authenticate_user')  # Mock authenticate_user
    @patch('presentation.application.Application.show_admin_menu')  # Mock show_admin_menu
    @patch('presentation.application.Application.show_user_menu')  # Mock show_user_menu
    def test_role_based_menu(self, mock_show_user_menu, mock_show_admin_menu, mock_authenticate_user, mock_showerror):
        # Simulate successful authentication with an Admin role
        mock_authenticate_user.return_value = ('Admin', 1)  # 'Admin' role, user ID 1

        # Create the Tkinter root window and application instance
        root = tk.Tk()
        app = Application(root)

        # Set valid username and password
        app.username_entry.insert(0, "testuser")
        app.password_entry.insert(0, "correctpassword")

        # Call the submit_login method
        app.submit_login()

        # Assert that the Admin menu is shown (since the role is 'Admin')
        mock_show_admin_menu.assert_called_once()
        mock_show_user_menu.assert_not_called()

        # Simulate successful authentication with a User role
        mock_authenticate_user.return_value = ('Employee', 2)  # 'User' role, user ID 2

        # Call the submit_login method again
        app.submit_login()

        # Assert that the User menu is shown (since the role is 'User')
        mock_show_user_menu.assert_called_once()
        mock_show_admin_menu.assert_called_once()  # Ensures Admin menu was already called before


if __name__ == '__main__':
    unittest.main()
