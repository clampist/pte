"""
User business fixtures - extends core fixtures with user-specific data
"""
import pytest
from typing import Dict, List
from config.settings import TestEnvironment


@pytest.fixture(scope="session")
def test_environment():
    """Get current test environment"""
    return TestEnvironment.get_current_env()


@pytest.fixture(scope="session")
def test_host():
    """Get test host URL"""
    return TestEnvironment.get_host()


@pytest.fixture(scope="session")
def test_headers():
    """Get test headers"""
    return TestEnvironment.get_headers()


@pytest.fixture(scope="session")
def test_timeout():
    """Get test timeout"""
    return TestEnvironment.get_timeout()


@pytest.fixture(scope="function")
def sample_user_data():
    """Sample user data fixture"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "age": 25
    }


@pytest.fixture(scope="function")
def sample_users_list():
    """Sample users list fixture"""
    return [
        {"name": "User 1", "email": "user1@example.com", "age": 20},
        {"name": "User 2", "email": "user2@example.com", "age": 25},
        {"name": "User 3", "email": "user3@example.com", "age": 30}
    ]


@pytest.fixture(scope="function")
def valid_user_data():
    """Valid user data fixture"""
    return {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "age": 25
    }


@pytest.fixture(scope="function")
def invalid_user_data_no_name():
    """Invalid user data - missing name"""
    return {
        "email": "test@example.com",
        "age": 25
    }


@pytest.fixture(scope="function")
def invalid_user_data_no_email():
    """Invalid user data - missing email"""
    return {
        "name": "Test User",
        "age": 25
    }


@pytest.fixture(scope="function")
def duplicate_email_user_data():
    """User data with duplicate email"""
    return {
        "name": "Duplicate User",
        "email": "john.smith@example.com",  # Existing email
        "age": 30
    }


@pytest.fixture(scope="function")
def update_user_data():
    """User update data fixture"""
    return {
        "name": "Updated User",
        "age": 26
    }


@pytest.fixture(scope="function")
def user_operations():
    """User operations fixture with current environment"""
    from biz.department.user.operations import UserOperations
    return UserOperations()


@pytest.fixture(scope="function")
def user_operations_with_custom_headers():
    """User operations fixture with custom headers"""
    from biz.department.user.operations import UserOperations
    custom_headers = {
        "X-Custom-Header": "test-value",
        "X-Request-ID": "test-request-123"
    }
    return UserOperations(custom_headers=custom_headers)
