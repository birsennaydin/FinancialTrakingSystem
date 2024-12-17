import pytest
from sqlalchemy.orm import sessionmaker

from business.user_logic import authenticate_user, register_user
from models.models_orm import User, engine
import hashlib

# SQLAlchemy session
Session = sessionmaker(bind=engine)

# Mock Data Fixture (Optional)
@pytest.fixture
def mock_user_data():
    return {
        "name": "Test User",
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "TestPassword123"
    }


# Test for user authentication
def test_authenticate_user(mock_user_data):
    # Add a user to the database
    session = Session()
    password_hash = hashlib.sha256(mock_user_data["password"].encode()).hexdigest()
    user = User(
        name=mock_user_data["name"],
        username=mock_user_data["username"],
        email=mock_user_data["email"],
        password=password_hash,
        role="User"
    )
    session.add(user)
    session.commit()

    # Call the authentication function
    result = authenticate_user(mock_user_data["username"], mock_user_data["password"])

    assert result is not None
    assert result[0] == "User"  # Check role
    assert result[1] == user.id  # Check user ID

    # Clean up
    session.delete(user)
    session.commit()


# Test for user registration
def test_register_user(mock_user_data):
    message = register_user(mock_user_data["name"], mock_user_data["username"], mock_user_data["email"])

    assert "successfully" in message  # Assert the success message in registration

    # Clean up: Delete user after test
    session = Session()
    user = session.query(User).filter_by(username=mock_user_data["username"]).first()
    session.delete(user)
    session.commit()
