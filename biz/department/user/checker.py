"""
User business checker - extends core checker with user-specific validations
"""
from core.checker import ResponseChecker, DataChecker, ErrorChecker
from typing import Dict, List


class UserResponseChecker(ResponseChecker):
    """User-specific response checker"""
    
    @staticmethod
    def assert_user_response_structure(response_or_data, message: str = None):
        """Assert user response has required structure"""
        required_keys = ["users", "count"]
        ResponseChecker.assert_response_structure(response_or_data, required_keys, message)
    
    @staticmethod
    def assert_single_user_response(response_or_data, message: str = None):
        """Assert single user response structure"""
        required_keys = ["id", "name", "email"]
        ResponseChecker.assert_response_structure(response_or_data, required_keys, message)


class UserDataChecker(DataChecker):
    """User-specific data checker"""
    
    # User required fields
    USER_REQUIRED_FIELDS = ["id", "name", "email"]
    USER_CREATE_REQUIRED_FIELDS = ["name", "email"]
    
    @staticmethod
    def assert_user_data(user_data: Dict, message: str = None):
        """Assert user data structure"""
        # Check required fields
        UserDataChecker.assert_data_structure(user_data, UserDataChecker.USER_REQUIRED_FIELDS, message)
        
        # Check data types using specific type methods
        UserDataChecker.assert_int_data(user_data["id"], "id", message)
        UserDataChecker.assert_str_data(user_data["name"], "name", message)
        UserDataChecker.assert_str_data(user_data["email"], "email", message)
        
        # Check email format
        assert "@" in user_data["email"], f"{message or 'Invalid email format'}: {user_data['email']}"
    
    @staticmethod
    def assert_user_create_data(user_data: Dict, message: str = None):
        """Assert user creation data structure"""
        # Check required fields for creation
        UserDataChecker.assert_data_structure(user_data, UserDataChecker.USER_CREATE_REQUIRED_FIELDS, message)
        
        # Check data types using specific type methods
        UserDataChecker.assert_str_data(user_data["name"], "name", message)
        UserDataChecker.assert_str_data(user_data["email"], "email", message)
        
        # Check email format
        assert "@" in user_data["email"], f"{message or 'Invalid email format'}: {user_data['email']}"
        
        # Check optional age field if present
        if "age" in user_data:
            UserDataChecker.assert_int_data(user_data["age"], "age", message)
    
    @staticmethod
    def assert_user_update_data(user_data: Dict, message: str = None):
        """Assert user update data structure"""
        # For updates, at least one field should be present
        if not user_data:
            raise ValueError(f"{message or 'Update data cannot be empty'}")
        
        # Check each field if present
        if "name" in user_data:
            UserDataChecker.assert_str_data(user_data["name"], "name", message)
            UserDataChecker.assert_not_empty(user_data["name"], "name", message)
        
        if "email" in user_data:
            UserDataChecker.assert_str_data(user_data["email"], "email", message)
            UserDataChecker.assert_not_empty(user_data["email"], "email", message)
            # Check email format
            assert "@" in user_data["email"], f"{message or 'Invalid email format'}: {user_data['email']}"
        
        if "age" in user_data:
            UserDataChecker.assert_int_data(user_data["age"], "age", message)
            UserDataChecker.assert_in_range(user_data["age"], 0, 150, "age", message)
    
    @staticmethod
    def assert_user_list(user_list: List[Dict], expected_count: int = None, message: str = None):
        """Assert user list structure"""
        UserDataChecker.assert_list_structure(user_list, expected_count, message)
        
        # Validate each user in the list
        for user in user_list:
            UserDataChecker.assert_user_data(user, message)
    
    @staticmethod
    def assert_user_age_range(user_data: Dict, min_age: int = 0, max_age: int = 150, message: str = None):
        """Assert user age is within valid range"""
        if "age" in user_data:
            UserDataChecker.assert_in_range(user_data["age"], min_age, max_age, "age", message)
    
    @staticmethod
    def assert_user_name_length(user_data: Dict, min_length: int = 1, max_length: int = 50, message: str = None):
        """Assert user name length is within valid range"""
        UserDataChecker.assert_string_length(user_data["name"], min_length, max_length, "name", message)
    
    @staticmethod
    def assert_user_email_format(user_data: Dict, message: str = None):
        """Assert user email has valid format"""
        email = user_data["email"]
        UserDataChecker.assert_str_data(email, "email", message)
        UserDataChecker.assert_not_empty(email, "email", message)
        
        # Basic email format validation
        assert "@" in email, f"{message or 'Invalid email format'}: {email}"
        assert "." in email.split("@")[1], f"{message or 'Invalid email format'}: {email}"
        assert len(email.split("@")[0]) > 0, f"{message or 'Invalid email format'}: {email}"


class UserErrorChecker(ErrorChecker):
    """User-specific error checker"""
    
    @staticmethod
    def assert_user_not_found_error(response, message: str = None):
        """Assert user not found error"""
        UserErrorChecker.assert_error_response(
            response, 
            "User not found", 
            404
        )
    
    @staticmethod
    def assert_user_duplicate_email_error(response, message: str = None):
        """Assert duplicate email error"""
        UserErrorChecker.assert_error_response(
            response,
            "Email already exists",
            409
        )
    
    @staticmethod
    def assert_user_missing_fields_error(response, message: str = None):
        """Assert missing fields error"""
        UserErrorChecker.assert_error_response(
            response,
            "Missing required fields",
            400
        )
