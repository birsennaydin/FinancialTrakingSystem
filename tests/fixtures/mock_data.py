# tests/fixtures/mock_data.py

import pytest
from models.models_orm import User


@pytest.fixture
def mock_user_data():
    """
    Fixture to provide mock user data for tests.
    This can be used to create a user in the database.
    """
    return {
        "name": "Test User",
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "TestPassword123"
    }


@pytest.fixture
def create_mock_user(session, mock_user_data):
    """
    Fixture that creates a user in the test database using mock data.
    This ensures that a user is created before the test starts.
    """
    # Assuming 'register_user' is the business logic function that registers a user
    from business.user_logic import register_user  # Import the register_user function

    # Register the user using the mock data
    message = register_user(mock_user_data["name"], mock_user_data["username"], mock_user_data["email"])
    print(f"MockUser result: {message}")
    # Query and return the created user
    user = session.query(User).filter_by(username=mock_user_data["username"]).first()
    return user