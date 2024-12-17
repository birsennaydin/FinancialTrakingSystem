import sqlite3
import config

def create_tables(db_name=config.DATABASE_NAME):
    """Create tables for the Brew and Bite database if they don't exist."""
    try:
        # Establish the connection and use a context manager to ensure it is properly closed
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            # Create Users table with the added 'role' column
            cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       username TEXT UNIQUE NOT NULL,
                       password TEXT NOT NULL,
                       email TEXT NOT NULL,
                       role TEXT CHECK(role IN ('Admin', 'User')) DEFAULT 'User' NOT NULL
                   )
                   ''')

            # Create Categories table
            cursor.execute('''
                   CREATE TABLE IF NOT EXISTS categories (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT UNIQUE NOT NULL
                   )
                   ''')

            # Create Expenses table
            cursor.execute('''
                   CREATE TABLE IF NOT EXISTS expenses (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER NOT NULL,
                       category_id INTEGER NOT NULL,
                       description TEXT NOT NULL,
                       amount REAL NOT NULL,
                       FOREIGN KEY (user_id) REFERENCES users(id),
                       FOREIGN KEY (category_id) REFERENCES categories(id)
                   )
                   ''')

            # Create Inventory table
            cursor.execute('''
                   CREATE TABLE IF NOT EXISTS inventory (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       item_name TEXT UNIQUE NOT NULL,
                       quantity INTEGER NOT NULL,
                       cost REAL NOT NULL,
                       restock_date TEXT NOT NULL
                   )
                   ''')

            # Create Sales table
            cursor.execute('''
                   CREATE TABLE IF NOT EXISTS sales (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       inventory_id INTEGER NOT NULL,
                       user_id INTEGER NOT NULL,
                       quantity INTEGER NOT NULL,
                       amount REAL NOT NULL,
                       sale_date TEXT NOT NULL,
                       FOREIGN KEY (inventory_id) REFERENCES inventory(id),
                       FOREIGN KEY (user_id) REFERENCES users(id)
                   )
                   ''')

            # Commit changes
            conn.commit()
            print(f"Tables created successfully in {db_name}")

    except sqlite3.Error as e:
        print(f"An error occurred while creating tables: {e}")