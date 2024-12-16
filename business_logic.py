import hashlib
import utils
import config
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models_orm import User, Category, Expense, Inventory, Sale, engine

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
        print(f"User: {user.username}, Role: {user.role}")
        # If user exists
        if user:
            # Hash the input password to compare with the stored hashed password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Check if the password matches
            if user.password == hashed_password:
                print(f"User: {user.password}, Role: {hashed_password}")
                return user.role, user.id  # Return the user's role and id
        return None  # Invalid password or user not found
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None
    finally:
        session.close()

def register_user(name, username, email, role="User"):
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

def insert_user(session, name, username, password, email, role="User"):
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
        print(f"UpdateUsers: ", username, name, email, password, role)
        # Check if the email is already in use by another user
        existing_user = session.query(User).filter(User.email == email, User.username != username).first()
        print(f"UpdateUsers22: ", existing_user)
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

def get_categories():
    """Fetch all categories from the database"""
    session = Session()  # Start a new session
    try:
        # Query all categories from the categories table
        categories = session.query(Category.id, Category.name).all()
        return [{"id": category[0], "name": category[1]} for category in categories]  # Return list of categories
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return []
    finally:
        session.close()  # Close the session


def get_category_id_by_name(category_name):
    """Get the category ID based on the category name"""
    session = Session()  # Start a new session
    try:
        # Query the category ID based on the name
        category = session.query(Category.id).filter_by(name=category_name).first()
        if category:
            return category[0]
        else:
            raise ValueError("Category not found.")
    except Exception as e:
        print(f"Error fetching category ID: {e}")
        return None
    finally:
        session.close()  # Close the session


def record_expense(user_id, category_id, description, amount):
    """Record a new expense into the database"""
    session = Session()  # Start a new session
    try:
        # Create a new expense entry and add it to the session
        expense = Expense(user_id=user_id, category_id=category_id, description=description, amount=amount)
        session.add(expense)
        session.commit()  # Commit the changes
        print("Expense recorded successfully.")
    except Exception as e:
        print(f"Error recording expense: {e}")
        session.rollback()  # Rollback in case of error
    finally:
        session.close()  # Close the session

def get_all_expenses():
    """Fetch all expenses from the database with associated user information"""
    session = Session()  # Start a new session
    try:
        # Join the expenses, categories, and users tables to fetch the required fields
        expenses = session.query(User.username, Category.name, Expense.description, Expense.amount) \
                          .join(Category, Expense.category_id == Category.id) \
                          .join(User, Expense.user_id == User.id) \
                          .all()

        return [{"username": expense[0], "category": expense[1], "description": expense[2], "amount": expense[3]} for expense in expenses]
    except Exception as e:
        print(f"Error fetching expenses: {e}")
        return []
    finally:
        session.close()  # Close the session


def add_inventory_item(item_name, quantity, cost, restock_date):
    """Add a new item to the inventory"""
    session = Session()  # Start a new session
    try:
        # Create a new inventory item and add it to the session
        inventory_item = Inventory(item_name=item_name, quantity=quantity, cost=cost, restock_date=restock_date)
        session.add(inventory_item)
        session.commit()  # Commit the changes
        return "Inventory item added successfully."
    except Exception as e:
        print(f"Error adding inventory item: {e}")
        session.rollback()  # Rollback in case of error
        return "An error occurred while adding the inventory item."
    finally:
        session.close()  # Close the session


def delete_inventory_item(item_id):
    """Delete an inventory item"""
    session = Session()  # Start a new session
    try:
        # Query and delete the inventory item by its id
        item = session.query(Inventory).filter_by(id=item_id).first()
        if item:
            session.delete(item)  # Delete the item
            session.commit()  # Commit the changes
            return "Inventory item deleted successfully."
        else:
            return "Inventory item not found."
    except Exception as e:
        print(f"Error deleting inventory item: {e}")
        session.rollback()  # Rollback in case of error
        return "An error occurred while deleting the inventory item."
    finally:
        session.close()  # Close the session

def get_inventory_id_by_name(item_name):
    """Fetch the inventory item ID based on the item name"""
    session = Session()  # Start a new session
    try:
        # Query the inventory table by item name
        item = session.query(Inventory).filter_by(item_name=item_name).first()
        return item.id if item else None
    except Exception as e:
        print(f"Error fetching inventory item ID: {e}")
        return None
    finally:
        session.close()  # Close the session


def get_inventory_items():
    """Fetch all inventory items from the database"""
    session = Session()  # Start a new session
    try:
        # Query all inventory items
        items = session.query(Inventory).all()
        return [{
            "id": item.id,
            "item_name": item.item_name,
            "quantity": item.quantity,
            "cost": item.cost,
            "restock_date": item.restock_date
        } for item in items]
    except Exception as e:
        print(f"Error fetching inventory items: {e}")
        return []
    finally:
        session.close()  # Close the session


def record_sale(inventory_id, quantity, amount, sale_date, user_id):
    """Record a new sale transaction and update the inventory"""
    session = Session()  # Start a new session
    try:
        # Create a new sale record
        sale = Sale(
            inventory_id=inventory_id,
            quantity=quantity,
            amount=amount,
            sale_date=sale_date,
            user_id=user_id
        )
        session.add(sale)  # Add the sale record to the session

        # Update the inventory by reducing the quantity
        inventory_item = session.query(Inventory).filter_by(id=inventory_id).first()
        if inventory_item:
            inventory_item.quantity -= quantity
            session.commit()  # Commit both sale and inventory changes
            return "Sale recorded successfully!"
        else:
            return "Inventory item not found."
    except Exception as e:
        print(f"An error occurred while recording the sale: {e}")
        session.rollback()  # Rollback in case of error
        return f"An error occurred: {e}"
    finally:
        session.close()  # Close the session


def update_inventory_item(item_id, item_name, quantity, cost, restock_date):
    """Update the details of an inventory item"""
    session = Session()  # Start a new session
    try:
        # Query and update the inventory item by its id
        item = session.query(Inventory).filter_by(id=item_id).first()
        if item:
            item.item_name = item_name
            item.quantity = quantity
            item.cost = cost
            item.restock_date = restock_date
            session.commit()  # Commit the changes
            return "Inventory item updated successfully."
        else:
            return "Inventory item not found."
    except Exception as e:
        print(f"Error updating inventory item: {e}")
        session.rollback()  # Rollback in case of error
        return "An error occurred while updating the inventory item."
    finally:
        session.close()  # Close the session

def get_sales_history():
    """Retrieve sales history including username and item_name"""
    session = Session()  # Start a new session
    try:

        # Query the sales history with user and inventory details
        sales = (session.query(Sale.id, Sale.inventory_id, Sale.quantity, Sale.amount, Sale.sale_date,
                              User.username, Inventory.item_name)
                 .join(User, Sale.user_id == User.id)
                 .join(Inventory, Sale.inventory_id == Inventory.id)
                 .order_by(Sale.sale_date.desc())
                 .all())

        # Format and return the sales history with associated usernames and item names
        return [{"id": sale[0], "inventory_id": sale[1], "quantity": sale[2], "amount": sale[3],
                 "sale_date": sale[4], "username": sale[5], "item_name": sale[6]} for sale in sales]

    except Exception as e:
        print(f"An error occurred while fetching sales history: {e}")
        return []
    finally:
        session.close()  # Close the session

def get_daily_revenue(date):
    """Track revenue for a specific day"""
    session = Session()  # Start a new session
    try:
        revenue = session.query(func.sum(Sale.amount)).filter(Sale.sale_date == date).scalar()

        # Return the revenue for the specified date, or 0.0 if none
        return revenue if revenue else 0.0
    except Exception as e:
        print(f"Error tracking daily revenue: {e}")
        return 0.0
    finally:
        session.close()  # Close the session

def get_sales_history_with_user():
    """Fetch sales history with associated usernames"""
    session = Session()  # Start a new session
    try:
        # Query sales history with user and inventory details
        sales = (session.query(User.username, Inventory.item_name, Sale.quantity, Sale.amount, Sale.sale_date)
                 .join(Inventory, Sale.inventory_id == Inventory.id)
                 .join(User, Sale.user_id == User.id)
                 .all())

        # Return the formatted sales history with associated usernames
        return [{"username": sale[0], "item_name": sale[1], "quantity": sale[2], "amount": sale[3], "sale_date": sale[4]} for sale in sales]

    except Exception as e:
        print(f"Error fetching sales history with user: {e}")
        return []
    finally:
        session.close()  # Close the session

def create_default_admin_user():
    """Check if admin user exists, if not, create it."""
    session = Session()  # Start a new session
    try:
        # Check if admin user exists
        user = session.query(User).filter_by(username=config.DATABASE_ADMIN_USERNAME).first()
        if not user:
            print("Admin user does not exist, creating default admin user.")

            # Create a default admin user
            hashed_password = hashlib.sha256(config.DATABASE_ADMIN_PASSWORD.encode()).hexdigest()
            admin_user = User(name=config.DATABASE_ADMIN_NAME,
                              username=config.DATABASE_ADMIN_USERNAME,
                              password=hashed_password,
                              email=config.DATABASE_ADMIN_EMAIL,
                              role=config.DATABASE_ADMIN_ROLE)
            session.add(admin_user)
            session.commit()
            print("Default admin user created.")
    except Exception as e:
        print(f"Error creating default admin user: {e}")
    finally:
        session.close()  # Close the session

def insert_default_category():
    """Insert default category 'Bill' into categories table if not exists."""
    session = Session()  # Start a new session outside the try block
    try:
        # Check if the category 'Bill' exists
        category = session.query(Category).filter_by(name='Bill').first()
        if not category:
            # Insert default category 'Bill' if it does not exist
            default_category = Category(name='Bill')
            session.add(default_category)
            session.commit()
            print("Default category 'Bill' inserted.")

    except Exception as e:
        print(f"Error inserting default category: {e}")
    finally:
        session.close()  # Close the session


def insert_default_datas():
    session = Session()  # Start a new session outside the try block
    try:
        # Insert default admin user
        create_default_admin_user()  # This will create the default admin user if it doesn't exist

        # Insert default category
        insert_default_category()  # This will insert the default category if it doesn't exist

    except Exception as e:
        print(f"Error inserting default datas: {e}")
    finally:
        session.close()  # Close the session