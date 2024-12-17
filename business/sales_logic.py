from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from models.models_orm import User, Sale, Inventory, engine

# SQLAlchemy session
Session = sessionmaker(bind=engine)

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