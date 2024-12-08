import tkinter as tk
from tkinter import messagebox
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

    @staticmethod
    def show_inventory_management():
        """Showing inventory management"""
        messagebox.showinfo("Inventory Management", "Manage inventory here!")

    @staticmethod
    def show_sales_tracking():
        """Dummy function for showing sales tracking"""
        messagebox.showinfo("Sales Tracking", "Track sales here!")

    @staticmethod
    def show_reporting():
        """Dummy function for showing reporting"""
        messagebox.showinfo("Reporting", "View reports here!")

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

def run_application():
    """Function to initialize and run the Tkinter application"""
    root = tk.Tk()
    Application(root)  # Creating an instance of the Application class
    root.mainloop()  # Starts the Tkinter event loop
