# tests/fixtures/test_db.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models_orm import Base, User
from config import TEST_DATABASE_NAME  # Test database URL

# Define the test database engine
TEST_DATABASE_URL = f"sqlite:///{TEST_DATABASE_NAME}"

@pytest.fixture(scope="function")
def session():
    """Fixture that provides a new session for each test function."""
    # Create an engine for the test database
    test_engine = create_engine(TEST_DATABASE_URL)

    # Create a sessionmaker bound to the test engine
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()

    # Create tables in the test database
    Base.metadata.create_all(test_engine)

    # Optionally, truncate the table before each test
    session.query(User).delete()  # Clear all users in the test database before each test
    session.commit()

    yield session

    session.rollback()  # Rollback any changes after the test
    session.close()  # Close the session

    # Drop tables after each test to clean up
    Base.metadata.drop_all(test_engine)
