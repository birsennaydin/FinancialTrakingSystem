from sqlalchemy.orm import sessionmaker

from business.inventory_logic import get_inventory_items
from business.expense_logic import get_all_expenses
from models.models_orm import User, Inventory, Sale, engine

# SQLAlchemy session
Session = sessionmaker(bind=engine)

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


def get_inventory_items_list():
    try:
       return get_inventory_items()
    except Exception as e:
        print(f"Error fetching inventory items: {e}")
        return []

def get_all_expenses_list():
    try:
        return get_all_expenses()
    except Exception as e:
        print(f"Error fetching expenses: {e}")
        return []
