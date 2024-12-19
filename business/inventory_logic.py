from sqlalchemy.orm import sessionmaker
from models.models_orm import Inventory, engine

# SQLAlchemy session
Session = sessionmaker(bind=engine)

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