"""
User test data - data for test layer
"""
from typing import Dict, List


class UserTestData:
    """User test data"""
    
    # Valid user data
    VALID_USER_1 = {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "age": 25
    }
    
    VALID_USER_2 = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "age": 30
    }
    
    VALID_USER_3 = {
        "name": "Mike Johnson",
        "email": "mike.johnson@example.com",
        "age": 28
    }
    
    # Invalid user data
    INVALID_USER_NO_NAME = {
        "email": "test@example.com",
        "age": 25
    }
    
    INVALID_USER_NO_EMAIL = {
        "name": "Test User",
        "age": 25
    }
    
    INVALID_USER_DUPLICATE_EMAIL = {
        "name": "Duplicate User",
        "email": "john.smith@example.com",  # Existing email
        "age": 30
    }
    
    # Update data
    UPDATE_NAME_ONLY = {
        "name": "Updated John Smith"
    }
    
    UPDATE_AGE_ONLY = {
        "age": 26
    }
    
    UPDATE_MULTIPLE_FIELDS = {
        "name": "Updated User",
        "age": 27,
        "email": "updated@example.com"
    }
    
    # Test user IDs
    EXISTING_USER_IDS = [1, 2, 3]
    NON_EXISTING_USER_IDS = [999, 0, -1]
    
    # Expected responses
    EXPECTED_USER_1 = {
        "id": 1,
        "name": "John Smith",
        "email": "john.smith@example.com",
        "age": 25
    }
    
    EXPECTED_USER_2 = {
        "id": 2,
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "age": 30
    }
    
    EXPECTED_USER_3 = {
        "id": 3,
        "name": "Mike Johnson",
        "email": "mike.johnson@example.com",
        "age": 28
    }
    
    # Error messages
    ERROR_MISSING_FIELDS = "Missing required fields"
    ERROR_USER_NOT_FOUND = "User not found"
    ERROR_EMAIL_EXISTS = "Email already exists"
    ERROR_NO_UPDATE_DATA = "No update data provided"
    
    # Success messages
    SUCCESS_USER_DELETED = "User deleted successfully"
    
    @classmethod
    def get_valid_users(cls) -> List[Dict]:
        """Get list of valid users"""
        return [cls.VALID_USER_1, cls.VALID_USER_2, cls.VALID_USER_3]
    
    @classmethod
    def get_invalid_users(cls) -> List[Dict]:
        """Get list of invalid users"""
        return [
            cls.INVALID_USER_NO_NAME,
            cls.INVALID_USER_NO_EMAIL,
            cls.INVALID_USER_DUPLICATE_EMAIL
        ]
    
    @classmethod
    def get_update_data_sets(cls) -> List[Dict]:
        """Get list of update data sets"""
        return [
            cls.UPDATE_NAME_ONLY,
            cls.UPDATE_AGE_ONLY,
            cls.UPDATE_MULTIPLE_FIELDS
        ]
    
    @classmethod
    def get_test_user_by_id(cls, user_id: int) -> Dict:
        """Get expected user data by ID"""
        user_map = {
            1: cls.EXPECTED_USER_1,
            2: cls.EXPECTED_USER_2,
            3: cls.EXPECTED_USER_3
        }
        return user_map.get(user_id, {})
    
    @classmethod
    def create_test_user(cls, name: str, email: str, age: int = 25) -> Dict:
        """Create test user data"""
        return {
            "name": name,
            "email": email,
            "age": age
        }
