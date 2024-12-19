import tkinter as tk
from tkinter import messagebox

from business.inventory_logic import get_inventory_id_by_name, get_inventory_items, add_inventory_item, update_inventory_item

class InventoryWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Inventory Management")
        self.top.geometry("600x400")

        # Buttons for inventory operations
        tk.Button(self.top, text="Add Inventory", command=self.add_inventory).pack()
        tk.Button(self.top, text="Update Inventory", command=self.update_inventory).pack()
        tk.Button(self.top, text="List Inventories", command=self.list_inventories).pack()

    def add_inventory(self):
        """Open the Add Inventory window"""
        AddInventoryWindow(self.top)

    def update_inventory(self):
        """Open the Update Inventory window"""
        UpdateInventoryWindow(self.top)

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
            message = add_inventory_item(item_name, quantity, cost, restock_date)
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
        self.items = get_inventory_items()
        print(f"Inventories Datas: {self.items}")
        if not self.items:
            messagebox.showerror("Error", "No inventory items found.")
            self.top.destroy()
            return

        self.select_label = tk.Label(self.top, text="Select Inventory Item:")
        self.select_label.pack()

        self.selected_item = tk.StringVar()
        self.selected_item.set(self.items[0]["item_name"])  # Default value
        # OptionMenu for selecting inventory item
        self.select_option = tk.OptionMenu(self.top, self.selected_item, *[item["item_name"] for item in self.items],
                                           command=self.update_fields)
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

        # Initial population of fields
        self.update_fields(self.selected_item.get())

    def update_fields(self, selected_item_name):
        """Update the input fields with the selected item's data."""
        # Find the selected item in the inventory list
        selected_item = next(item for item in self.items if item["item_name"] == selected_item_name)

        # Populate the fields with the selected item’s data
        self.item_name_entry.delete(0, tk.END)
        self.item_name_entry.insert(0, selected_item["item_name"])

        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, selected_item["quantity"])

        self.cost_entry.delete(0, tk.END)
        self.cost_entry.insert(0, selected_item["cost"])

        self.restock_date_entry.delete(0, tk.END)
        self.restock_date_entry.insert(0, selected_item["restock_date"])

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
            message = update_inventory_item(item_id, item_name, quantity, cost, restock_date)
            messagebox.showinfo("Inventory Updated", message)
            self.top.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values for quantity and cost.")


class ListInventoryWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("List of Inventory Items")
        self.top.geometry("800x600")

        self.items = get_inventory_items()

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