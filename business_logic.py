import sqlite3

import models
import hashlib
import utils
import config


def authenticate_user(username, password):
    """Authenticate the user by checking username and hashed password."""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, password, role FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user[1] == hashed_password:
                    return user[2], user[0]  # Return the role ('Admin' or 'User'), user id
            return None
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

def register_user(name, username, email, role = "User"):
    """Register a new user after validating input."""
    try:
        if models.check_user_exists(config.DATABASE_NAME, username, email):
            return "Username or email already exists."

        # Generate a random password for the user
        password = utils.generate_random_password()

        # Insert the new user with the generated password (hashed)
        models.insert_user(config.DATABASE_NAME, name, username, password, email, role)

        # Return the generated password to the GUI to display to the user
        return f"User registered successfully. Your password is: {password}"
    except Exception as e:
        print(f"Error during registration: {e}")
        return "An error occurred during registration. Please try again."

def get_user_info(username):
    """Get current user information based on username."""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, username, email, role FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user:
                return user  # (name, username, email, role)
            else:
                return None
    except Exception as e:
        print(f"Error during fetching user info: {e}")
        return None

def update_user_info(username, name, email, password=None, role=None):
    """Update the user information in the database."""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()

            # Check if the email is already in use by another user
            cursor.execute("SELECT * FROM users WHERE email = ? AND username != ?", (email, username))
            existing_user = cursor.fetchone()
            if existing_user:
                return "This email address is already in use by another user."

            # Update query for name, email, password, and role
            query = '''UPDATE users SET name = ?, email = ?'''
            params = [name, email]

            # Only update password if provided
            if password:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                query += ", password = ?"
                params.append(hashed_password)

            # Only update role if provided
            if role:
                query += ", role = ?"
                params.append(role)

            query += " WHERE username = ?"
            params.append(username)

            cursor.execute(query, params)
            conn.commit()
            return "User information updated successfully."

    except Exception as e:
        print(f"Error during updating user info: {e}")
        return "An error occurred while updating user information."

def get_all_usernames():
    """Fetch all usernames from the database (for Admin role)."""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username FROM users')
            users = cursor.fetchall()
            return [user[0] for user in users]  # Return list of usernames
    except Exception as e:
        print(f"Error during fetching all usernames: {e}")
        return []

def get_all_users_info():
    """Fetch all users' information from the database"""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT username, email, role FROM users")
            users = cursor.fetchall()

            users_info = [{"username": user[0], "email": user[1], "role": user[2]} for user in users]

            return users_info
    except Exception as e:
        print(f"Error fetching users info: {e}")
        return []

def delete_user(username):
    """Delete a user from the database."""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()
            return f"User {username} deleted successfully."
    except Exception as e:
        print(f"Error deleting user: {e}")
        return "An error occurred while deleting the user."

def get_categories():
    """Fetch all categories from the database"""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM categories')
            categories = cursor.fetchall()
            return [{"id": category[0], "name": category[1]} for category in categories]
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return []

def get_category_id_by_name(category_name):
    """Get the category ID based on the category name"""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
            category = cursor.fetchone()
            if category:
                return category[0]
            else:
                raise ValueError("Category not found.")
    except Exception as e:
        print(f"Error fetching category ID: {e}")
        return None

def record_expense(user_id, category_id, description, amount):
    """Record a new expense into the database"""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO expenses (user_id, category_id, description, amount)
                VALUES (?, ?, ?, ?)
            ''', (user_id, category_id, description, amount))
            conn.commit()
            print("Expense recorded successfully.")
    except Exception as e:
        print(f"Error recording expense: {e}")

def get_all_expenses():
    """Fetch all expenses from the database with associated user information"""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT users.username, categories.name, expenses.description, expenses.amount
                FROM expenses
                JOIN categories ON expenses.category_id = categories.id
                JOIN users ON expenses.user_id = users.id
            ''')
            expenses = cursor.fetchall()
            return [{"username": expense[0], "category": expense[1], "description": expense[2], "amount": expense[3]} for expense in expenses]
    except Exception as e:
        print(f"Error fetching expenses: {e}")
        return []

# business_logic.py

def add_inventory_item(item_name, quantity, cost, restock_date):
    """Add a new item to the inventory"""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO inventory (item_name, quantity, cost, restock_date)
                VALUES (?, ?, ?, ?)
            ''', (item_name, quantity, cost, restock_date))
            conn.commit()
            return "Inventory item added successfully."
    except Exception as e:
        print(f"Error adding inventory item: {e}")
        return "An error occurred while adding the inventory item."

def update_inventory_item(item_id, item_name, quantity, cost, restock_date):
    """Update the details of an inventory item"""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE inventory
                SET item_name = ?, quantity = ?, cost = ?, restock_date = ?
                WHERE id = ?
            ''', (item_name, quantity, cost, restock_date, item_id))
            conn.commit()
            return "Inventory item updated successfully."
    except Exception as e:
        print(f"Error updating inventory item: {e}")
        return "An error occurred while updating the inventory item."

def delete_inventory_item(item_id):
    """Delete an inventory item"""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
            conn.commit()
            return "Inventory item deleted successfully."
    except Exception as e:
        print(f"Error deleting inventory item: {e}")
        return "An error occurred while deleting the inventory item."

def get_inventory_items():
    """Fetch all inventory items"""
    try:
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, item_name, quantity, cost, restock_date FROM inventory')
            items = cursor.fetchall()
            return [{"id": item[0], "item_name": item[1], "quantity": item[2], "cost": item[3], "restock_date": item[4]} for item in items]
    except Exception as e:
        print(f"Error fetching inventory items: {e}")
        return []
