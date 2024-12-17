import hashlib
import config
from sqlalchemy.orm import sessionmaker
from models.models_orm import User, Category, engine

# SQLAlchemy session
Session = sessionmaker(bind=engine)

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