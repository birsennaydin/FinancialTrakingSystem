import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
import business_logic

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
            user_role, user_id = business_logic.authenticate_user(username, password)

            if user_role:
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


class UpdateUserWindow:
    def __init__(self, parent, role, username):
        self.top = tk.Toplevel(parent)
        self.top.title("Update User Info")

        # Set the window size
        self.top.geometry("600x400")

        self.username = username
        self.role = role

        # Fetch all users' usernames if role is Admin
        if self.role == 'Admin':
            self.users = business_logic.get_all_usernames()  # Fetch all usernames
            if not self.users:
                messagebox.showerror("Error", "No users found.")
                self.top.destroy()
                return

            # Add a drop-down to select a user
            self.select_label = tk.Label(self.top, text="Select User:")
            self.select_label.pack()

            self.selected_user = tk.StringVar()
            self.selected_user.set(self.users[0])  # Default value
            self.select_option = tk.OptionMenu(self.top, self.selected_user, *self.users)
            self.select_option.pack()

            self.submit_button = tk.Button(self.top, text="Select User", command=self.load_user_info)
            self.submit_button.pack()
        else:
            # If the role is 'User', directly load the user's info
            self.load_user_info()

        # Exit button to close the window
        exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        exit_button.pack()

    def exit_application(self):
        """Exit the application"""
        self.top.quit()

    def load_user_info(self):
        # If the role is Admin, get the selected user's info
        if self.role == 'Admin':
            selected_user = self.selected_user.get()
            user_info = business_logic.get_user_info(selected_user)
        else:
            # If the role is 'User', get the logged-in user's info
            user_info = business_logic.get_user_info(self.username)

        if not user_info:
            messagebox.showerror("Error", "User not found.")
            return

        name, username, email, role = user_info

        # Populate fields with current user information
        self.name_label = tk.Label(self.top, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.top)
        self.name_entry.insert(0, name)
        self.name_entry.pack()

        self.username_label = tk.Label(self.top, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.top)
        self.username_entry.insert(0, username)
        self.username_entry.config(state='disabled')  # Username can't be changed
        self.username_entry.pack()

        self.email_label = tk.Label(self.top, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self.top)
        self.email_entry.insert(0, email)
        self.email_entry.pack()

        self.password_label = tk.Label(self.top, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.top, show="*")  # This will display "******"
        self.password_entry.pack()

        self.role_label = tk.Label(self.top, text="Role:")
        self.role_label.pack()
        self.role_var = tk.StringVar()
        self.role_var.set(role)
        # Role options based on the current user's role
        if self.role == 'User':
            self.role_option = tk.OptionMenu(self.top, self.role_var, "User")
        else:
            self.role_option = tk.OptionMenu(self.top, self.role_var, "Admin", "User")
        self.role_option.pack()

        self.submit_button = tk.Button(self.top, text="Submit", command=self.submit_update_user)
        self.submit_button.pack()

    def submit_update_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        # Validation: Check if any field is empty
        if not name or not email:
            messagebox.showerror("Input Error", "Name and email must be filled out.")
            return

        # If password is empty, it will be considered as no update to password
        if not password:
            password = None

        try:
            # If user is Admin, update the selected user
            if self.role == 'Admin':
                message = business_logic.update_user_info(self.selected_user.get(), name, email, password, role)
            else:
                # If user is 'User', update only their own information
                message = business_logic.update_user_info(self.username, name, email, password, role)

            messagebox.showinfo("Update User", message)
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during update: {e}")

class ListUsersWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("List of Users")

        # Set the window size (increase width and height)
        self.top.geometry("800x600")  # Widening the window

        # Fetch all users' information
        self.users_info = business_logic.get_all_users_info()

        if not self.users_info:
            messagebox.showerror("Error", "No users found.")
            self.top.destroy()
            return

        # Display user information in a table-like format
        self.table_frame = tk.Frame(self.top)
        self.table_frame.pack(pady=20)

        # Create headers for the table
        self.header_username = tk.Label(self.table_frame, text="Username", width=20, anchor="w")
        self.header_username.grid(row=0, column=0, padx=10)

        self.header_email = tk.Label(self.table_frame, text="Email", width=30, anchor="w")
        self.header_email.grid(row=0, column=1, padx=10)

        self.header_role = tk.Label(self.table_frame, text="Role", width=15, anchor="w")
        self.header_role.grid(row=0, column=2, padx=10)

        # Populate the table with user data
        for i, user in enumerate(self.users_info, start=1):
            tk.Label(self.table_frame, text=user["username"], width=20, anchor="w").grid(row=i, column=0, padx=10)
            tk.Label(self.table_frame, text=user["email"], width=30, anchor="w").grid(row=i, column=1, padx=10)
            tk.Label(self.table_frame, text=user["role"], width=15, anchor="w").grid(row=i, column=2, padx=10)

        # Add Exit button to close the window
        exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        exit_button.pack(pady=10)

    def exit_application(self):
        """Exit the application"""
        self.top.quit()

class DeleteUserWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Delete User")

        # Set the window size
        self.top.geometry("600x400")

        # Fetch all users' usernames
        self.users = business_logic.get_all_usernames()  # Fetch all usernames

        if not self.users:
            messagebox.showerror("Error", "No users found.")
            self.top.destroy()
            return

        # Add a drop-down to select a user
        self.select_label = tk.Label(self.top, text="Select User to Delete:")
        self.select_label.pack()

        self.selected_user = tk.StringVar()
        self.selected_user.set(self.users[0])  # Default value
        self.select_option = tk.OptionMenu(self.top, self.selected_user, *self.users)
        self.select_option.pack()

        # Submit button to delete the selected user
        self.submit_button = tk.Button(self.top, text="Submit", command=self.submit_delete_user)
        self.submit_button.pack()

        # Exit button to close the window
        exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        exit_button.pack()

    def submit_delete_user(self):
        selected_user = self.selected_user.get()

        if not selected_user:
            messagebox.showerror("Input Error", "Please select a user to delete.")
            return

        try:
            # Call the business logic to delete the user
            message = business_logic.delete_user(selected_user)
            messagebox.showinfo("Delete User", message)
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during user deletion: {e}")

    def exit_application(self):
        """Exit the application"""
        self.top.quit()

class RegisterWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Register")

        # Set the window size for Register window
        self.top.geometry("600x400")

        self.name_label = tk.Label(self.top, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.top)
        self.name_entry.pack()

        self.username_label = tk.Label(self.top, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.top)
        self.username_entry.pack()

        self.email_label = tk.Label(self.top, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self.top)
        self.email_entry.pack()

        self.submit_button = tk.Button(self.top, text="Submit", command=self.submit_register)
        self.submit_button.pack()

        self.back_button = tk.Button(self.top, text="Back", command=self.top.destroy)
        self.back_button.pack()

        # Exit button to close the window
        exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        exit_button.pack()

    def submit_register(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()

        # Validation: Check if any field is empty
        if not name or not username or not email:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            message = business_logic.register_user(name, username, email)
            messagebox.showinfo("Registration", message)
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during registration: {e}")

    def exit_application(self):
        """Exit the application"""
        self.top.quit()


class UserWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Add Register")

        # Set the window size for User window
        self.top.geometry("600x400")

        self.name_label = tk.Label(self.top, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.top)
        self.name_entry.pack()

        self.username_label = tk.Label(self.top, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.top)
        self.username_entry.pack()

        self.email_label = tk.Label(self.top, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self.top)
        self.email_entry.pack()

        # Role selection
        self.role_label = tk.Label(self.top, text="Role:")
        self.role_label.pack()
        self.role_var = tk.StringVar()
        self.role_var.set("User")  # Default value
        self.role_option = tk.OptionMenu(self.top, self.role_var, "Admin", "User")
        self.role_option.pack()

        self.submit_button = tk.Button(self.top, text="Submit", command=self.submit_add_user)
        self.submit_button.pack()

        self.back_button = tk.Button(self.top, text="Back", command=self.top.destroy)
        self.back_button.pack()

        # Exit button to close the window
        exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        exit_button.pack()

    def submit_add_user(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        role = self.role_var.get()

        # Validation: Check if any field is empty
        if not name or not username or not email:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            message = business_logic.register_user(name, username, email, role)
            messagebox.showinfo("Add User", message)
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during user addition: {e}")

    def exit_application(self):
        """Exit the application"""
        self.top.quit()


class ExpenseWindow:
    def __init__(self, parent, user_id):
        self.top = tk.Toplevel(parent)
        self.top.title("Expense Management")
        self.top.geometry("600x400")

        self.logged_in_user_id = user_id

        # Record Daily Expense
        tk.Button(self.top, text="Record Daily Expense", command=self.record_expense).pack()

        # List Expenses
        tk.Button(self.top, text="List Expenses", command=self.list_expenses).pack()

    def record_expense(self):
        """Record daily expense"""
        RecordExpenseWindow(self.top, self.logged_in_user_id)

    def list_expenses(self):
        """List all expenses"""
        ListExpensesWindow(self.top)


class RecordExpenseWindow:
    def __init__(self, parent, user_id):
        self.top = tk.Toplevel(parent)
        self.top.title("Record Daily Expense")
        self.top.geometry("600x400")

        self.user_id = user_id

        self.category_label = tk.Label(self.top, text="Category:")
        self.category_label.pack()

        # Category dropdown
        self.categories = business_logic.get_categories()
        self.category_var = tk.StringVar()
        self.category_var.set(self.categories[0]["name"])  # Default to first category
        self.category_option = tk.OptionMenu(self.top, self.category_var, *[category["name"] for category in self.categories])
        self.category_option.pack()

        self.description_label = tk.Label(self.top, text="Description:")
        self.description_label.pack()
        self.description_entry = tk.Entry(self.top)
        self.description_entry.pack()

        self.amount_label = tk.Label(self.top, text="Amount:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.top)
        self.amount_entry.pack()

        self.submit_button = tk.Button(self.top, text="Submit", command=self.submit_expense)
        self.submit_button.pack()

        # Add Exit button to close the window
        exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        exit_button.pack(pady=10)

    def submit_expense(self):
        """Submit the expense to the database"""
        category_name = self.category_var.get()
        description = self.description_entry.get()
        amount = self.amount_entry.get()

        if not description or not amount:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            amount = float(amount)
            category_id = business_logic.get_category_id_by_name(category_name)
            message = business_logic.record_expense(self.user_id, category_id, description, amount)
            messagebox.showinfo("Expense Recorded", "Expense has been successfully recorded.")
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during expense recording: {e}")

    def exit_application(self):
        """Exit the application"""
        self.top.quit()


class ListExpensesWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("List of Expenses")
        self.top.geometry("800x600")

        self.expenses = business_logic.get_all_expenses()  # Get expenses with user info

        if not self.expenses:
            messagebox.showerror("Error", "No expenses found.")
            self.top.destroy()
            return

        # Display expense information
        self.table_frame = tk.Frame(self.top)
        self.table_frame.pack(pady=20)

        # Create headers for the table
        self.header_username = tk.Label(self.table_frame, text="Username", width=20, anchor="w")
        self.header_username.grid(row=0, column=0, padx=10)

        self.header_category = tk.Label(self.table_frame, text="Category", width=20, anchor="w")
        self.header_category.grid(row=0, column=1, padx=10)

        self.header_description = tk.Label(self.table_frame, text="Description", width=30, anchor="w")
        self.header_description.grid(row=0, column=2, padx=10)

        self.header_amount = tk.Label(self.table_frame, text="Amount", width=15, anchor="w")
        self.header_amount.grid(row=0, column=3, padx=10)

        # Populate the table with expense data
        for i, expense in enumerate(self.expenses, start=1):
            tk.Label(self.table_frame, text=expense["username"], width=20, anchor="w").grid(row=i, column=0, padx=10)
            tk.Label(self.table_frame, text=expense["category"], width=20, anchor="w").grid(row=i, column=1, padx=10)
            tk.Label(self.table_frame, text=expense["description"], width=30, anchor="w").grid(row=i, column=2, padx=10)
            tk.Label(self.table_frame, text=expense["amount"], width=15, anchor="w").grid(row=i, column=3, padx=10)

        # Exit button to close the window
        exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        exit_button.pack(pady=10)

    def exit_application(self):
        """Exit the application"""
        self.top.quit()

class InventoryWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Inventory Management")
        self.top.geometry("600x400")

        # Buttons for inventory operations
        tk.Button(self.top, text="Add Inventory", command=self.add_inventory).pack()
        tk.Button(self.top, text="Update Inventory", command=self.update_inventory).pack()
        tk.Button(self.top, text="Delete Inventory", command=self.delete_inventory).pack()
        tk.Button(self.top, text="List Inventories", command=self.list_inventories).pack()

    def add_inventory(self):
        """Open the Add Inventory window"""
        AddInventoryWindow(self.top)

    def update_inventory(self):
        """Open the Update Inventory window"""
        UpdateInventoryWindow(self.top)

    def delete_inventory(self):
        """Open the Delete Inventory window"""
        DeleteInventoryWindow(self.top)

    def list_inventories(self):
        """Show the list of inventory items"""
        ListInventoryWindow(self.top)


class AddInventoryWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Add Inventory Item")
        self.top.geometry("600x400")

        self.item_name_label = tk.Label(self.top, text="Item Name:")
        self.item_name_label.pack()
        self.item_name_entry = tk.Entry(self.top)
        self.item_name_entry.pack()

        self.quantity_label = tk.Label(self.top, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(self.top)
        self.quantity_entry.pack()

        self.cost_label = tk.Label(self.top, text="Cost:")
        self.cost_label.pack()
        self.cost_entry = tk.Entry(self.top)
        self.cost_entry.pack()

        self.restock_date_label = tk.Label(self.top, text="Restock Date (YYYY-MM-DD):")
        self.restock_date_label.pack()
        self.restock_date_entry = tk.Entry(self.top)
        self.restock_date_entry.pack()

        self.submit_button = tk.Button(self.top, text="Submit", command=self.submit_inventory)
        self.submit_button.pack()

    def submit_inventory(self):
        """Submit the new inventory item to the database"""
        item_name = self.item_name_entry.get()
        quantity = self.quantity_entry.get()
        cost = self.cost_entry.get()
        restock_date = self.restock_date_entry.get()

        if not item_name or not quantity or not cost or not restock_date:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            quantity = int(quantity)
            cost = float(cost)
            message = business_logic.add_inventory_item(item_name, quantity, cost, restock_date)
            messagebox.showinfo("Inventory Added", message)
            self.top.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values for quantity and cost.")


class UpdateInventoryWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Update Inventory Item")
        self.top.geometry("600x400")

        # Dropdown to select inventory item for update
        self.items = business_logic.get_inventory_items()

        if not self.items:
            messagebox.showerror("Error", "No inventory items found.")
            self.top.destroy()
            return

        self.select_label = tk.Label(self.top, text="Select Inventory Item:")
        self.select_label.pack()

        self.selected_item = tk.StringVar()
        self.selected_item.set(self.items[0]["item_name"])  # Default value
        self.select_option = tk.OptionMenu(self.top, self.selected_item, *[item["item_name"] for item in self.items])
        self.select_option.pack()

        self.item_name_label = tk.Label(self.top, text="Item Name:")
        self.item_name_label.pack()
        self.item_name_entry = tk.Entry(self.top)
        self.item_name_entry.pack()

        self.quantity_label = tk.Label(self.top, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(self.top)
        self.quantity_entry.pack()

        self.cost_label = tk.Label(self.top, text="Cost:")
        self.cost_label.pack()
        self.cost_entry = tk.Entry(self.top)
        self.cost_entry.pack()

        self.restock_date_label = tk.Label(self.top, text="Restock Date:")
        self.restock_date_label.pack()
        self.restock_date_entry = tk.Entry(self.top)
        self.restock_date_entry.pack()

        self.submit_button = tk.Button(self.top, text="Submit", command=self.submit_update_inventory)
        self.submit_button.pack()

    def submit_update_inventory(self):
        """Submit the updated inventory item"""
        item_name = self.item_name_entry.get()
        quantity = self.quantity_entry.get()
        cost = self.cost_entry.get()
        restock_date = self.restock_date_entry.get()

        if not item_name or not quantity or not cost or not restock_date:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            item_id = next(item["id"] for item in self.items if item["item_name"] == self.selected_item.get())
            quantity = int(quantity)
            cost = float(cost)
            message = business_logic.update_inventory_item(item_id, item_name, quantity, cost, restock_date)
            messagebox.showinfo("Inventory Updated", message)
            self.top.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values for quantity and cost.")


class DeleteInventoryWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Delete Inventory Item")
        self.top.geometry("600x400")

        self.items = business_logic.get_inventory_items()

        if not self.items:
            messagebox.showerror("Error", "No inventory items found.")
            self.top.destroy()
            return

        self.select_label = tk.Label(self.top, text="Select Inventory Item to Delete:")
        self.select_label.pack()

        self.selected_item = tk.StringVar()
        self.selected_item.set(self.items[0]["item_name"])  # Default value
        self.select_option = tk.OptionMenu(self.top, self.selected_item, *[item["item_name"] for item in self.items])
        self.select_option.pack()

        self.submit_button = tk.Button(self.top, text="Submit", command=self.submit_delete_inventory)
        self.submit_button.pack()

    def submit_delete_inventory(self):
        selected_item_name = self.selected_item.get()

        if not selected_item_name:
            messagebox.showerror("Input Error", "Please select an inventory item to delete.")
            return

        try:
            item_id = next(item["id"] for item in self.items if item["item_name"] == selected_item_name)
            message = business_logic.delete_inventory_item(item_id)
            messagebox.showinfo("Inventory Deleted", message)
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during deletion: {e}")


class ListInventoryWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("List of Inventory Items")
        self.top.geometry("800x600")

        self.items = business_logic.get_inventory_items()

        if not self.items:
            messagebox.showerror("Error", "No inventory items found.")
            self.top.destroy()
            return

        # Display inventory information
        self.table_frame = tk.Frame(self.top)
        self.table_frame.pack(pady=20)

        self.header_item_name = tk.Label(self.table_frame, text="Item Name", width=20, anchor="w")
        self.header_item_name.grid(row=0, column=0, padx=10)

        self.header_quantity = tk.Label(self.table_frame, text="Quantity", width=15, anchor="w")
        self.header_quantity.grid(row=0, column=1, padx=10)

        self.header_cost = tk.Label(self.table_frame, text="Cost", width=15, anchor="w")
        self.header_cost.grid(row=0, column=2, padx=10)

        self.header_restock_date = tk.Label(self.table_frame, text="Restock Date", width=15, anchor="w")
        self.header_restock_date.grid(row=0, column=3, padx=10)

        for i, item in enumerate(self.items, start=1):
            tk.Label(self.table_frame, text=item["item_name"], width=20, anchor="w").grid(row=i, column=0, padx=10)
            tk.Label(self.table_frame, text=item["quantity"], width=15, anchor="w").grid(row=i, column=1, padx=10)
            tk.Label(self.table_frame, text=item["cost"], width=15, anchor="w").grid(row=i, column=2, padx=10)
            tk.Label(self.table_frame, text=item["restock_date"], width=15, anchor="w").grid(row=i, column=3, padx=10)

        # Exit button to close the window
        exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        exit_button.pack(pady=10)

    def exit_application(self):
        """Exit the application"""
        self.top.quit()

class SalesTrackingWindow:
    def __init__(self, parent, user_id):
        self.top = tk.Toplevel(parent)
        self.top.title("Sales Tracking")
        self.top.geometry("600x400")

        self.logged_in_user_id = user_id

        # Buttons for sales tracking operations
        tk.Button(self.top, text="Record Sale", command=self.record_sale).pack()
        tk.Button(self.top, text="Sales History", command=self.view_sales_history).pack()
        tk.Button(self.top, text="Track Daily Revenue", command=self.track_daily_revenue).pack()

    def record_sale(self):
        """Open the Record Sale window"""
        RecordSaleWindow(self.top, self.logged_in_user_id)

    def view_sales_history(self):
        """Open the Sales History window"""
        SalesHistoryWindow(self.top)

    def track_daily_revenue(self):
        """Open the Track Daily Revenue window"""
        TrackDailyRevenueWindow(self.top)

class RecordSaleWindow:
    def __init__(self, parent, user_id):
        self.top = tk.Toplevel(parent)
        self.top.title("Record Sale")
        self.top.geometry("700x500")

        # Fetch available items from inventory
        self.items = business_logic.get_inventory_items()
        self.logged_in_user_id = user_id

        if not self.items:
            messagebox.showerror("Error", "No inventory items found.")
            self.top.destroy()
            return

        self.select_label = tk.Label(self.top, text="Select Item:")
        self.select_label.pack()

        self.selected_item = tk.StringVar()
        self.selected_item.set(self.items[0]["item_name"])  # Default value
        self.select_option = tk.OptionMenu(self.top, self.selected_item, *[item["item_name"] for item in self.items], command=self.update_stock)
        self.select_option.pack()

        # Stock label and value
        self.stock_label = tk.Label(self.top, text="Stock:")
        self.stock_label.pack()

        self.stock_value = tk.Label(self.top, text="0")
        self.stock_value.pack()

        self.quantity_label = tk.Label(self.top, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(self.top)
        self.quantity_entry.insert(0, "0")  # Default to 0
        self.quantity_entry.pack()

        self.amount_label = tk.Label(self.top, text="Total Amount:")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(self.top)
        self.amount_entry.insert(0, "0.00")  # Default to 0.00
        self.amount_entry.config(state='readonly')  # Make it readonly initially
        self.amount_entry.pack()

        self.sale_date_label = tk.Label(self.top, text="Sale Date (YYYY-MM-DD):")
        self.sale_date_label.pack()

        # Create a calendar widget for Sale Date
        self.sale_date_entry = tk.Entry(self.top)
        self.sale_date_entry.pack()
        self.sale_date_entry.bind("<FocusIn>", self.show_calendar)  # Show calendar when clicked

        self.submit_button = tk.Button(self.top, text="Submit Sale", command=self.submit_sale)
        self.submit_button.pack()

        # Exit button
        self.exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        self.exit_button.pack()

        # Update the stock label initially
        self.update_stock(self.selected_item.get())  # Call the function to set the stock

        # Bind the quantity entry to update the total automatically when the quantity changes
        self.quantity_entry.bind('<KeyRelease>', self.calculate_total)

        self.calendar_window = None

    def update_stock(self, selected_item_name):
        """Update the stock value dynamically when an item is selected"""
        selected_item = next(item for item in self.items if item["item_name"] == selected_item_name)
        stock_quantity = selected_item["quantity"]  # Get the stock quantity from the selected item

        self.stock_value.config(text=str(stock_quantity))  # Update the stock label

        # Recalculate the total amount when the stock changes
        self.calculate_total()

    def calculate_total(self, event=None):
        """Calculate total amount based on quantity and item cost"""
        quantity = self.quantity_entry.get().strip()  # Trim any extra spaces

        # Check if the quantity is a valid number
        try:
            quantity = int(quantity)
        except ValueError:
            self.amount_entry.config(state='normal')
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, "Invalid quantity")
            self.amount_entry.config(state='readonly')
            return

        # Ensure quantity is greater than 0
        if quantity <= 0:
            self.amount_entry.config(state='normal')
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, "Quantity must be > 0")
            self.amount_entry.config(state='readonly')
            return

        # Find the selected item and its cost
        selected_item_name = self.selected_item.get()
        selected_item = next(item for item in self.items if item["item_name"] == selected_item_name)
        item_cost = selected_item["cost"]

        # Ensure the quantity is not greater than the available stock
        stock_quantity = selected_item["quantity"]
        if quantity > stock_quantity:
            self.amount_entry.config(state='normal')
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, "Stock not enough")
            self.amount_entry.config(state='readonly')
            return

        # Calculate the total amount
        total_amount = item_cost * quantity
        self.amount_entry.config(state='normal')
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, f"{total_amount:.2f}")
        self.amount_entry.config(state='readonly')

    def show_calendar(self, event=None):
        """Show a calendar when the user clicks on the Sale Date input"""
        if self.calendar_window is None:
            self.calendar_window = Calendar(self.top, selectmode="day", date_pattern="yyyy-mm-dd")
            self.calendar_window.pack()
            self.calendar_window.bind("<<CalendarSelected>>", self.set_sale_date)

    def set_sale_date(self, event):
        """Set the selected date into the Sale Date entry"""
        selected_date = self.calendar_window.get_date()
        self.sale_date_entry.delete(0, tk.END)
        self.sale_date_entry.insert(0, selected_date)
        self.calendar_window.destroy()
        self.calendar_window = None

    def submit_sale(self):
        """Submit the sale and update inventory"""
        selected_item_name = self.selected_item.get()
        quantity = self.quantity_entry.get().strip()  # Trim spaces from input
        sale_date = self.sale_date_entry.get()

        if not quantity or not sale_date:
            messagebox.showerror("Input Error", "Quantity and Sale Date must be filled out.")
            return

        # Check if quantity is greater than 0
        try:
            # Try converting to integer
            quantity = int(quantity)

            # Ensure quantity is greater than 0
            if quantity <= 0:
                messagebox.showerror("Input Error", "Quantity must be greater than 0.")
                return

        except ValueError:
            # If there's a ValueError, show the error message
            messagebox.showerror("Input Error", "Please enter a valid number for quantity.")
            return

        # Validate Sale Date format
        try:
            # Ensure the date is in the correct format (YYYY-MM-DD)
            datetime.datetime.strptime(sale_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Date Error", "Incorrect date format. Please use YYYY-MM-DD.")
            return

        try:
            # Find the item id and stock
            selected_item = next(item for item in self.items if item["item_name"] == selected_item_name)
            item_id = selected_item["id"]
            stock_quantity = selected_item["quantity"]

            # Ensure the quantity is valid
            if quantity > stock_quantity:
                messagebox.showerror("Stock Error", "Stock is not sufficient for this sale.")
                return

            # Calculate the total amount (already done automatically)
            total_amount = float(self.amount_entry.get())  # Get the total amount from the entry field

            # Call business logic to record the sale and update the inventory
            sale_message = business_logic.record_sale(item_id, quantity, total_amount, sale_date, self.logged_in_user_id)
            messagebox.showinfo("Sale Record", sale_message)

            # Optionally close the window after a successful sale
            self.top.destroy()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for quantity.")

    def exit_application(self):
        """Exit the application"""
        self.top.quit()

class SalesHistoryWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Sales History")
        self.top.geometry("800x600")

        self.sales = business_logic.get_sales_history()

        if not self.sales:
            messagebox.showerror("Error", "No sales history found.")
            self.top.destroy()
            return

        # Display sales history
        self.table_frame = tk.Frame(self.top)
        self.table_frame.pack(pady=20)

        # Create headers for the table
        self.header_username = tk.Label(self.table_frame, text="Username", width=20, anchor="w")
        self.header_username.grid(row=0, column=0, padx=10)

        self.header_item_name = tk.Label(self.table_frame, text="Item Name", width=20, anchor="w")
        self.header_item_name.grid(row=0, column=1, padx=10)

        self.header_quantity = tk.Label(self.table_frame, text="Quantity", width=15, anchor="w")
        self.header_quantity.grid(row=0, column=2, padx=10)

        self.header_amount = tk.Label(self.table_frame, text="Total Amount", width=15, anchor="w")
        self.header_amount.grid(row=0, column=3, padx=10)

        self.header_sale_date = tk.Label(self.table_frame, text="Sale Date", width=20, anchor="w")
        self.header_sale_date.grid(row=0, column=4, padx=10)

        # Populate the table with sales data including username and item_name
        for i, sale in enumerate(self.sales, start=1):
            tk.Label(self.table_frame, text=sale["username"], width=20, anchor="w").grid(row=i, column=0, padx=10)
            tk.Label(self.table_frame, text=sale["item_name"], width=20, anchor="w").grid(row=i, column=1, padx=10)
            tk.Label(self.table_frame, text=sale["quantity"], width=15, anchor="w").grid(row=i, column=2, padx=10)
            tk.Label(self.table_frame, text=sale["amount"], width=15, anchor="w").grid(row=i, column=3, padx=10)
            tk.Label(self.table_frame, text=sale["sale_date"], width=20, anchor="w").grid(row=i, column=4, padx=10)

        # Exit button to close the window
        exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        exit_button.pack(pady=10)

    def exit_application(self):
        """Exit the application"""
        self.top.quit()

class TrackDailyRevenueWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Track Daily Revenue")
        self.top.geometry("600x400")

        self.date_label = tk.Label(self.top, text="Enter Date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(self.top)
        self.date_entry.pack()

        self.submit_button = tk.Button(self.top, text="Submit", command=self.submit_date)
        self.submit_button.pack()

    def submit_date(self):
        """Submit the date to track revenue"""
        date = self.date_entry.get()

        if not date:
            messagebox.showerror("Input Error", "Please enter a date.")
            return

        try:
            revenue = business_logic.get_daily_revenue(date)
            messagebox.showinfo("Daily Revenue", f"Total revenue for {date} is £{revenue:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        self.top.destroy()

class ReportWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Financial Reports")
        self.top.geometry("600x400")

        # Labels for the report options
        self.report_label = tk.Label(self.top, text="Generate Financial Reports", font=("Arial", 16))
        self.report_label.pack(pady=20)

        # Button for expense report
        self.expense_report_button = tk.Button(self.top, text="Generate Expense Report", command=self.generate_expense_report)
        self.expense_report_button.pack(pady=10)

        # Button for inventory report
        self.inventory_report_button = tk.Button(self.top, text="Generate Inventory Report", command=self.generate_inventory_report)
        self.inventory_report_button.pack(pady=10)

        # Button for sales report
        self.sales_report_button = tk.Button(self.top, text="Generate Sales Report", command=self.generate_sales_report)
        self.sales_report_button.pack(pady=10)

        # Exit button
        self.exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        self.exit_button.pack(pady=20)

    def generate_expense_report(self):
        """Generate and display the expense report"""
        try:
            # Fetch expense data from the business logic layer
            expenses = business_logic.get_all_expenses()

            if not expenses:
                messagebox.showinfo("Report", "No expenses found.")
                return

            # Create a new window to display the report
            report_window = tk.Toplevel(self.top)
            report_window.title("Expense Report")
            report_window.geometry("800x600")

            # Create a table to display expense data
            table_frame = tk.Frame(report_window)
            table_frame.pack(pady=20)

            # Create headers for the expense table
            tk.Label(table_frame, text="Username", width=20, anchor="w").grid(row=0, column=0, padx=10)
            tk.Label(table_frame, text="Category", width=20, anchor="w").grid(row=0, column=1, padx=10)
            tk.Label(table_frame, text="Description", width=30, anchor="w").grid(row=0, column=2, padx=10)
            tk.Label(table_frame, text="Amount", width=15, anchor="w").grid(row=0, column=3, padx=10)

            # Populate the table with expenses data
            for i, expense in enumerate(expenses, start=1):
                tk.Label(table_frame, text=expense["username"], width=20, anchor="w").grid(row=i, column=0, padx=10)
                tk.Label(table_frame, text=expense["category"], width=20, anchor="w").grid(row=i, column=1, padx=10)
                tk.Label(table_frame, text=expense["description"], width=30, anchor="w").grid(row=i, column=2, padx=10)
                tk.Label(table_frame, text=expense["amount"], width=15, anchor="w").grid(row=i, column=3, padx=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the expense report: {e}")

    def generate_inventory_report(self):
        """Generate and display the inventory report"""
        try:
            # Fetch inventory data from the business logic layer
            inventory = business_logic.get_inventory_items()

            if not inventory:
                messagebox.showinfo("Report", "No inventory found.")
                return

            # Create a new window to display the report
            report_window = tk.Toplevel(self.top)
            report_window.title("Inventory Report")
            report_window.geometry("800x600")

            # Create a table to display inventory data
            table_frame = tk.Frame(report_window)
            table_frame.pack(pady=20)

            # Create headers for the inventory table
            tk.Label(table_frame, text="Item Name", width=20, anchor="w").grid(row=0, column=0, padx=10)
            tk.Label(table_frame, text="Quantity", width=15, anchor="w").grid(row=0, column=1, padx=10)
            tk.Label(table_frame, text="Cost", width=15, anchor="w").grid(row=0, column=2, padx=10)
            tk.Label(table_frame, text="Restock Date", width=20, anchor="w").grid(row=0, column=3, padx=10)

            # Populate the table with inventory data
            for i, item in enumerate(inventory, start=1):
                tk.Label(table_frame, text=item["item_name"], width=20, anchor="w").grid(row=i, column=0, padx=10)
                tk.Label(table_frame, text=item["quantity"], width=15, anchor="w").grid(row=i, column=1, padx=10)
                tk.Label(table_frame, text=item["cost"], width=15, anchor="w").grid(row=i, column=2, padx=10)
                tk.Label(table_frame, text=item["restock_date"], width=20, anchor="w").grid(row=i, column=3, padx=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the inventory report: {e}")

    def generate_sales_report(self):
        """Generate and display the sales report including the username"""
        try:
            # Fetch sales data with associated username from the business logic layer
            sales = business_logic.get_sales_history_with_user()

            if not sales:
                messagebox.showinfo("Report", "No sales found.")
                return

            # Create a new window to display the report
            report_window = tk.Toplevel(self.top)
            report_window.title("Sales Report")
            report_window.geometry("800x600")

            # Create a table to display sales data
            table_frame = tk.Frame(report_window)
            table_frame.pack(pady=20)

            # Create headers for the sales table
            tk.Label(table_frame, text="Username", width=20, anchor="w").grid(row=0, column=0, padx=10)
            tk.Label(table_frame, text="Item Name", width=20, anchor="w").grid(row=0, column=1, padx=10)
            tk.Label(table_frame, text="Quantity", width=15, anchor="w").grid(row=0, column=2, padx=10)
            tk.Label(table_frame, text="Amount", width=15, anchor="w").grid(row=0, column=3, padx=10)
            tk.Label(table_frame, text="Sale Date", width=20, anchor="w").grid(row=0, column=4, padx=10)

            # Populate the table with sales data
            for i, sale in enumerate(sales, start=1):
                tk.Label(table_frame, text=sale["username"], width=20, anchor="w").grid(row=i, column=0, padx=10)
                tk.Label(table_frame, text=sale["item_name"], width=20, anchor="w").grid(row=i, column=1, padx=10)
                tk.Label(table_frame, text=sale["quantity"], width=15, anchor="w").grid(row=i, column=2, padx=10)
                tk.Label(table_frame, text=sale["amount"], width=15, anchor="w").grid(row=i, column=3, padx=10)
                tk.Label(table_frame, text=sale["sale_date"], width=20, anchor="w").grid(row=i, column=4, padx=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the sales report: {e}")

    def exit_application(self):
        """Exit the report window"""
        self.top.quit()

def run_application():
    """Function to initialize and run the Tkinter application"""
    root = tk.Tk()
    Application(root)  # Creating an instance of the Application class
    root.mainloop()  # Starts the Tkinter event loop
