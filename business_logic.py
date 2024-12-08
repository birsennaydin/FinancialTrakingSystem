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
            cursor.execute('SELECT password, role FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user[0] == hashed_password:
                    return user[1]  # Return the role ('Admin' or 'User')
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