import hashlib
import utils
from sqlalchemy.orm import sessionmaker
from models.models_orm import User, engine

# SQLAlchemy session
Session = sessionmaker(bind=engine)

def authenticate_user(username, password):
    """Authenticate the user by checking username and hashed password."""
    session = Session()
    try:
        # Trim leading/trailing spaces from username and password
        username = username.strip()
        password = password.strip()

        # Query the user by username
        user = session.query(User).filter_by(username=username).first()
        # If user exists
        if user:
            # Hash the input password to compare with the stored hashed password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Check if the password matches
            if user.password == hashed_password:
                return user.role, user.id  # Return the user's role and id
        return None  # Invalid password or user not found
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None
    finally:
        session.close()

def register_user(name, username, email, role="Employee"):
    """Register a new user after validating input."""
    session = Session()
    try:
        # Check if the user already exists
        if check_user_exists(session, username, email):
            return "Username or email already exists."

        # Generate a random password for the user
        password = utils.generate_random_password()

        # Insert the new user with the generated password (hashed)
        insert_user(session, name, username, password, email, role)

        # Return the generated password to the GUI to display to the user
        return f"User registered successfully. Your password is: {password}"
    except Exception as e:
        print(f"Error during registration: {e}")
        return "An error occurred during registration. Please try again."
    finally:
        session.close()

def check_user_exists(session, username, email):
    """Check if a user with the given username or email already exists."""
    try:
        # Query the user by username or email
        user = session.query(User).filter((User.username == username) | (User.email == email)).first()
        return user is not None
    except Exception as e:
        print(f"Error checking user existence: {e}")
        return False

def insert_user(session, name, username, password, email, role="Employee"):
    """Insert a new user with hashed password into the users table."""
    try:
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Create a new user object
        new_user = User(name=name, username=username, password=hashed_password, email=email, role=role)

        # Add the new user to the session and commit
        session.add(new_user)
        session.commit()
        print(f"User {username} registered successfully.")
    except Exception as e:
        print(f"Error inserting user: {e}")
        session.rollback()  # Rollback in case of error

def get_user_info(username):
    """Get current user information based on username."""
    session = Session()  # Start a new session
    try:
        # Query the user by username
        user = session.query(User).filter_by(username=username).first()

        # If user exists, return the user data
        if user:
            return {"name": user.name, "username": user.username, "email": user.email, "role": user.role}
        else:
            return None  # User not found
    except Exception as e:
        print(f"Error during fetching user info: {e}")
        return None
    finally:
        session.close()  # Close the session

def update_user_info(username, name, email, password=None, role=None):
    """Update the user information in the database."""
    session = Session()
    try:
        # Check if the email is already in use by another user
        existing_user = session.query(User).filter(User.email == email, User.username != username).first()
        if existing_user:
            return "This email address is already in use by another user."

        # Query the user by username
        user = session.query(User).filter_by(username=username).first()

        # If user exists, update the fields
        if user:
            user.name = name
            user.email = email

            # Update password if provided
            if password:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                user.password = hashed_password

            # Update role if provided
            if role:
                user.role = role

            # Commit the changes to the database
            session.commit()
            return "User information updated successfully."
        else:
            return "User not found."

    except Exception as e:
        print(f"Error during updating user info: {e}")
        session.rollback()  # Rollback in case of an error
        return "An error occurred while updating user information."
    finally:
        session.close()

def get_all_usernames():
    """Fetch all usernames from the database (for Admin role)."""
    session = Session()  # Start a new session
    try:
        # Query all usernames from the users table
        users = session.query(User.username).all()
        return [user[0] for user in users]  # Return list of usernames
    except Exception as e:
        print(f"Error during fetching all usernames: {e}")
        return []
    finally:
        session.close()  # Close the session


def get_all_users_info():
    """Fetch all users' information from the database"""
    session = Session()  # Start a new session
    try:
        # Query all user information (username, email, and role)
        users = session.query(User.username, User.email, User.role).all()

        # Format and return the user info as a list of dictionaries
        users_info = [{"username": user[0], "email": user[1], "role": user[2]} for user in users]

        return users_info
    except Exception as e:
        print(f"Error fetching users info: {e}")
        return []
    finally:
        session.close()  # Close the session

def delete_user(username):
    """Delete a user from the database."""
    session = Session()  # Start a new session
    try:
        # Query the user by username
        user = session.query(User).filter_by(username=username).first()

        # If the user exists, delete it
        if user:
            session.delete(user)
            session.commit()  # Commit the transaction to delete the user
            return f"User {username} deleted successfully."
        else:
            return f"User {username} not found."
    except Exception as e:
        session.rollback()  # Rollback the session in case of error
        print(f"Error deleting user: {e}")
        return "An error occurred while deleting the user."
    finally:
        session.close()  # Close the session