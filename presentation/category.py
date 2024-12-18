import tkinter as tk
from tkinter import messagebox

from business.category_logic import get_categories, get_category_id_by_name, add_category_item

class CategoryWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Category Management")
        self.top.geometry("600x400")

        # Buttons for inventory operations
        tk.Button(self.top, text="Add Inventory", command=self.add_category).pack()
        tk.Button(self.top, text="List Inventories", command=self.list_category).pack()

    def add_category(self):
        """Open the Add Inventory window"""
        AddCategoryWindow(self.top)

    def list_category(self):
        """Show the list of inventory items"""
        ListCategoryWindow(self.top)


class AddCategoryWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Add Category Item")
        self.top.geometry("600x400")

        self.item_name_label = tk.Label(self.top, text="Item Name:")
        self.item_name_label.pack()
        self.item_name_entry = tk.Entry(self.top)
        self.item_name_entry.pack()

        self.submit_button = tk.Button(self.top, text="Submit", command=self.submit_category)
        self.submit_button.pack()

    def submit_category(self):
        """Submit the new inventory item to the database"""
        item_name = self.item_name_entry.get()

        if not item_name:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            message = add_category_item(item_name)
            messagebox.showinfo("Category Added", message)
            self.top.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid values.")


class ListCategoryWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("List of Category Items")
        self.top.geometry("800x600")

        self.items = get_categories()  # Fetch categories

        if not self.items:
            messagebox.showerror("Error", "No category items found.")
            self.top.destroy()
            return

        # Display category information
        self.table_frame = tk.Frame(self.top)
        self.table_frame.pack(pady=20)

        self.header_item_name = tk.Label(self.table_frame, text="Item Name", width=20, anchor="w")
        self.header_item_name.grid(row=0, column=0, padx=10)

        # Populate the table with category data
        for i, item in enumerate(self.items, start=1):
            # Access 'name' instead of 'item_name'
            tk.Label(self.table_frame, text=item["name"], width=20, anchor="w").grid(row=i, column=0, padx=10)

        # Exit button to close the window
        exit_button = tk.Button(self.top, text="Exit", command=self.exit_application)
        exit_button.pack(pady=10)

    def exit_application(self):
        """Exit the application"""
        self.top.quit()