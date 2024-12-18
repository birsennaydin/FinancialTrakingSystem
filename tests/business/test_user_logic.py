# tests/business/test_user_logic.py

from business.user_logic import authenticate_user

# Import session fixture from the test database setup
from tests.fixtures.test_db import session
from tests.fixtures.mock_data import mock_user_data, create_mock_user

# Test for user authentication using mock data fixture
def test_authenticate_user(mock_user_data, session):
    # Call the authentication function
    result = authenticate_user(mock_user_data["username"], mock_user_data["password"])

    assert result is None
