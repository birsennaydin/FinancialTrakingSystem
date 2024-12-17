import tkinter as tk
from tkinter import messagebox

from business.user_logic import authenticate_user
from presentation.users import UserWindow, UpdateUserWindow, DeleteUserWindow, ListUsersWindow, RegisterWindow
from presentation.expenses import ExpenseWindow
from presentation.inventory import InventoryWindow
from presentation.sales import SalesTrackingWindow
from presentation.reporting import ReportWindow


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Brew and Bite - Login")

        self.logged_in_user_id = None

        # Set the window size to be larger (e.g., 800x600)
        self.root.geometry("600x400")

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_login)
        self.submit_button.pack()

        self.register_button = tk.Button(root, text="Register", command=self.show_register_window)
        self.register_button.pack()

    def submit_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validation: Check if any field is empty
        if not username or not password:
            messagebox.showerror("Input Error", "Username and password cannot be empty.")
            return

        try:
            result = authenticate_user(username, password)

            if result:
                user_role, user_id = result
                self.logged_in_user_id = user_id

                # Open the menu based on user role
                if user_role == 'Admin':
                    self.show_admin_menu()
                elif user_role == 'User':
                    self.show_user_menu()

                self.root.withdraw()  # Hide the login window after successful login

            else:
                messagebox.showerror("Login Failed", "Invalid username or password!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during login: {e}")

    def get_logged_in_user_id(self):
        """Return the logged in user's ID"""
        return self.logged_in_user_id

    def show_register_window(self):
        RegisterWindow(self.root)

    def show_admin_menu(self):
        """Display the admin menu with all options"""
        admin_menu_window = tk.Toplevel(self.root)  # Open as a new window
        admin_menu_window.title("Admin Menu")

        # Set the window size for the Admin Menu
        admin_menu_window.geometry("600x400")

        tk.Button(admin_menu_window, text="User Management", command=self.show_user_management).pack()
        tk.Button(admin_menu_window, text="Expense Management", command=self.show_expense_management).pack()
        tk.Button(admin_menu_window, text="Inventory Management", command=self.show_inventory_management).pack()
        tk.Button(admin_menu_window, text="Sales Tracking", command=self.show_sales_tracking).pack()
        tk.Button(admin_menu_window, text="Reporting", command=self.show_reporting).pack()

        # Exit button to close the window
        exit_button = tk.Button(admin_menu_window, text="Exit", command=self.exit_application)
        exit_button.pack()

    def exit_application(self):
        """Exit the application"""
        self.root.quit()

    def show_user_menu(self):
        """Display the user menu with limited options"""
        user_menu_window = tk.Toplevel(self.root)  # Open as a new window
        user_menu_window.title("User Menu")

        # Set the window size for the User Menu
        user_menu_window.geometry("600x400")

        tk.Button(user_menu_window, text="Update My Info", command=self.update_user_info).pack()

        # Exit button to close the window
        exit_button = tk.Button(user_menu_window, text="Exit", command=self.exit_application)
        exit_button.pack()

    def show_user_management(self):
        """Show user management options in a new window"""
        user_management_window = tk.Toplevel(self.root)  # Open a new window for user management
        user_management_window.title("User Management")

        # Set the window size for User Management
        user_management_window.geometry("600x400")

        tk.Button(user_management_window, text="Add User", command=self.add_user).pack()
        tk.Button(user_management_window, text="Update User", command=self.update_user).pack()
        tk.Button(user_management_window, text="Delete User", command=self.delete_user).pack()
        tk.Button(user_management_window, text="List Users", command=self.list_users).pack()

        # Exit button to close the window
        exit_button = tk.Button(user_management_window, text="Exit", command=self.exit_application)
        exit_button.pack()

    def add_user(self):
        """Function for adding a user"""
        UserWindow(self.root)

    def update_user(self):
        """Function for updating a user"""
        username = self.username_entry.get()  # Fetch logged-in username
        if username:
            UpdateUserWindow(self.root, 'Admin', username)

    def delete_user(self):
        """Function for deleting a user"""
        DeleteUserWindow(self.root)

    def list_users(self):
        """Function for list the users"""
        ListUsersWindow(self.root)

    def show_expense_management(self):
        expense_window = ExpenseWindow(self.root, self.get_logged_in_user_id())
        expense_window.top.deiconify()

    def show_inventory_management(self):
        """Display inventory management options"""
        inventory_window = InventoryWindow(self.root)
        inventory_window.top.deiconify()

    def show_sales_tracking(self):
        """Display sales tracking options"""
        sales_window = SalesTrackingWindow(self.root, self.get_logged_in_user_id())
        sales_window.top.deiconify()

    def show_reporting(self):
        """Reporting"""
        report_window = ReportWindow(self.root)
        report_window.top.deiconify()

    def update_user_info(self):
        username = self.username_entry.get()  # Fetch logged-in username
        if username:
            UpdateUserWindow(self.root, 'User', username)

    def exit_application(self):
        """Exit the application"""
        self.root.quit()