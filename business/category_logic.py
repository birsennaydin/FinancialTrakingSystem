from sqlalchemy.orm import sessionmaker
from models.models_orm import Category, engine

# SQLAlchemy session
Session = sessionmaker(bind=engine)

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

def add_category_item(item_name):
    """Add a new item to the category"""
    session = Session()  # Start a new session
    try:
        # Check if the user already exists
        if check_category_exists(session, item_name):
            return "Category already exists."

        # Create a new category item and add it to the session
        category_item = Category(name=item_name)
        session.add(category_item)
        session.commit()  # Commit the changes
        return "Category item added successfully."
    except Exception as e:
        print(f"Error adding category item: {e}")
        session.rollback()  # Rollback in case of error
        return "An error occurred while adding the inventory item."
    finally:
        session.close()  # Close the session

def check_category_exists(session, name):
    """Check if a category with the given name already exists."""
    try:
        # Query the category by name
        category = session.query(Category).filter((Category.name == name)).first()
        return category is not None
    except Exception as e:
        print(f"Error checking category existence: {e}")
        return False