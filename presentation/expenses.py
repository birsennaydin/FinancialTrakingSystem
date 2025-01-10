from tkinter import messagebox
import tkinter as tk

from business.expense_logic import get_all_expenses, record_expense
from business.category_logic import get_categories, get_category_id_by_name


class ExpenseWindow:
    def __init__(self, parent, user_id):
        self.top = tk.Toplevel(parent)
        self.top.title("Expense Management")
        self.top.geometry("600x400")

        self.logged_in_user_id = user_id

        # Record Daily Expense
        tk.Button(self.top, text="Record Expense", command=self.record_expense).pack()

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
        self.top.title("Record Expense")
        self.top.geometry("600x400")

        self.user_id = user_id

        self.category_label = tk.Label(self.top, text="Category:")
        self.category_label.pack()

        # Category dropdown
        self.categories = get_categories()
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
            category_id = get_category_id_by_name(category_name)
            message = record_expense(self.user_id, category_id, description, amount)
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

        self.expenses = get_all_expenses()  # Get expenses with user info

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