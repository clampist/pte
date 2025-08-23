"""
User module configuration - static variables like URLs, status codes
"""
from typing import Dict, List
from api.config import APIConfig


class UserConfig:
    """User module configuration"""
    
    # API endpoints
    BASE_URL = "/api/users"
    GET_ALL_USERS = "/api/users"
    GET_USER_BY_ID = "/api/users/{user_id}"
    CREATE_USER = "/api/users"
    UPDATE_USER = "/api/users/{user_id}"
    DELETE_USER = "/api/users/{user_id}"
    
    # HTTP methods (use API layer config)
    GET = APIConfig.GET
    POST = APIConfig.POST
    PUT = APIConfig.PUT
    DELETE = APIConfig.DELETE
    
    # Status codes (use API layer config)
    OK = APIConfig.OK
    CREATED = APIConfig.CREATED
    BAD_REQUEST = APIConfig.BAD_REQUEST
    NOT_FOUND = APIConfig.NOT_FOUND
    CONFLICT = APIConfig.CONFLICT
    UNSUPPORTED_MEDIA_TYPE = APIConfig.UNSUPPORTED_MEDIA_TYPE
    
    # Content types (use API layer config)
    JSON_CONTENT_TYPE = APIConfig.JSON_CONTENT_TYPE
    
    # Required fields for user operations
    REQUIRED_FIELDS = ["name", "email"]
    OPTIONAL_FIELDS = ["age"]
    
    # Default values
    DEFAULT_AGE = 0
    
    # Error messages
    ERROR_MESSAGES = {
        "missing_fields": "Missing required fields",
        "user_not_found": "User not found",
        "email_exists": "Email already exists",
        "no_update_data": "No update data provided",
        "invalid_json": "Invalid JSON data"
    }
    
    # Success messages
    SUCCESS_MESSAGES = {
        "user_deleted": "User deleted successfully"
    }
    
    @classmethod
    def get_user_url(cls, user_id: int) -> str:
        """Get user URL with ID"""
        return cls.GET_USER_BY_ID.format(user_id=user_id)
    
    @classmethod
    def get_update_url(cls, user_id: int) -> str:
        """Get update user URL with ID"""
        return cls.UPDATE_USER.format(user_id=user_id)
    
    @classmethod
    def get_delete_url(cls, user_id: int) -> str:
        """Get delete user URL with ID"""
        return cls.DELETE_USER.format(user_id=user_id)
