from tkinter import messagebox
import tkinter as tk

from business.reporting_logic import get_inventory_items_list, get_sales_history_with_user, get_all_expenses_list

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
            expenses = get_all_expenses_list()

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
            inventory = get_inventory_items_list()

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
            sales = get_sales_history_with_user()

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