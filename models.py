import sqlite3
import hashlib
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
                       quantity INTEGER NOT NULL,
                       amount REAL NOT NULL,
                       sale_date TEXT NOT NULL,
                       FOREIGN KEY (inventory_id) REFERENCES inventory(id)
                   )
                   ''')

            # Commit changes
            conn.commit()
            print(f"Tables created successfully in {db_name}")

            # Ensure that default admin user exists
            create_default_admin_user(conn)

    except sqlite3.Error as e:
        print(f"An error occurred while creating tables: {e}")


def create_default_admin_user(conn):
    """Check if admin user exists, if not, create it."""
    cursor = conn.cursor()

    # Check if the admin user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?",
                   (config.DATABASE_ADMIN_USERNAME,))  # Parametreyi bir tuple olarak sağlıyoruz
    if cursor.fetchone() is None:  # No admin user found, so create one
        print("Admin user does not exist, creating default admin user.")

        # Admin user details from config.py
        name = config.DATABASE_ADMIN_NAME
        username = config.DATABASE_ADMIN_USERNAME
        password = config.DATABASE_ADMIN_PASSWORD  # This is the password that will be hash stored
        email = config.DATABASE_ADMIN_EMAIL
        role = config.DATABASE_ADMIN_ROLE

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert the admin user into the database with the correct number of parameters
        cursor.execute('''
        INSERT INTO users (name, username, password, email, role)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, username, hashed_password, email, role))
        conn.commit()
        print("Default admin user created.")

def check_user_exists(db_name, username, email):
    """Check if a user with the given username or email already exists."""
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
        return cursor.fetchone() is not None


def insert_user(db_name, name, username, password, email, role='User'):
    """Insert a new user with hashed password into the users table."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (name, username, password, email, role)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, username, hashed_password, email, role))
        conn.commit()
        print(f"User {username} registered successfully.")
