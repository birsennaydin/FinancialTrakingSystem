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