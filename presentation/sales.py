from tkinter import messagebox
import tkinter as tk
from tkcalendar import Calendar
import datetime
from business.sales_logic import record_sale, get_sales_history, get_daily_revenue
from business.inventory_logic import get_inventory_items

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
        self.items = get_inventory_items()
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
            sale_message = record_sale(item_id, quantity, total_amount, sale_date, self.logged_in_user_id)
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

        self.sales = get_sales_history()

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
            revenue = get_daily_revenue(date)
            messagebox.showinfo("Daily Revenue", f"Total revenue for {date} is £{revenue:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        self.top.destroy()