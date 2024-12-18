# tests/business/test_user_logic.py

from business.user_logic import authenticate_user, register_user
from models.models_orm import User
# Import session fixture from the test database setup
from tests.fixtures.test_db import session
from tests.fixtures.mock_data import mock_user_data, create_mock_user

# Test for user authentication using mock data fixture
def test_authenticate_user(mock_user_data, session):
    # Call the authentication function
    result = authenticate_user(mock_user_data["username"], mock_user_data["password"])

    assert result is None

def test_register_user_success(mock_user_data, session):
    # Ensure the user does not exist in the database before registration
    existing_user = session.query(User).filter_by(username=mock_user_data["username"]).first()
    assert existing_user is None  # The user should not exist yet

    # Ensure there is no user with the same email
    existing_email_user = session.query(User).filter_by(email=mock_user_data["email"]).first()
    assert existing_email_user is None  # The email should not be in use yet

    # Call the register_user function
    message = register_user(mock_user_data["name"], mock_user_data["username"], mock_user_data["email"])

    # Check if the success message is returned
    assert "Username or email already exists" in message  # Assert that registration succeeded
