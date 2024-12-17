from sqlalchemy.orm import sessionmaker
from models.models_orm import User, Category, Expense, engine

# SQLAlchemy session
Session = sessionmaker(bind=engine)

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