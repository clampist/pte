"""
API layer configuration - API related settings
"""
from typing import Dict, Any


class APIConfig:
    """API configuration constants"""
    
    # HTTP Methods
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    
    # Status Codes
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNSUPPORTED_MEDIA_TYPE = 415
    INTERNAL_SERVER_ERROR = 500
    
    # Content Types
    JSON_CONTENT_TYPE = "application/json"
    FORM_CONTENT_TYPE = "application/x-www-form-urlencoded"
    
    # Default timeouts
    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRY_COUNT = 3
    
    # Request headers
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Universal-Test-Framework/1.0"
    }
    
    # Environment header key
    ENV_HEADER_KEY = "X-Environment"
    
    @classmethod
    def get_methods(cls) -> Dict[str, str]:
        """Get HTTP methods"""
        return {
            "GET": cls.GET,
            "POST": cls.POST,
            "PUT": cls.PUT,
            "DELETE": cls.DELETE,
            "PATCH": cls.PATCH
        }
    
    @classmethod
    def get_status_codes(cls) -> Dict[str, int]:
        """Get status codes"""
        return {
            "OK": cls.OK,
            "CREATED": cls.CREATED,
            "BAD_REQUEST": cls.BAD_REQUEST,
            "UNAUTHORIZED": cls.UNAUTHORIZED,
            "FORBIDDEN": cls.FORBIDDEN,
            "NOT_FOUND": cls.NOT_FOUND,
            "CONFLICT": cls.CONFLICT,
            "UNSUPPORTED_MEDIA_TYPE": cls.UNSUPPORTED_MEDIA_TYPE,
            "INTERNAL_SERVER_ERROR": cls.INTERNAL_SERVER_ERROR
        }
    
    @classmethod
    def get_content_types(cls) -> Dict[str, str]:
        """Get content types"""
        return {
            "JSON": cls.JSON_CONTENT_TYPE,
            "FORM": cls.FORM_CONTENT_TYPE
        }
    
    @classmethod
    def get_defaults(cls) -> Dict[str, Any]:
        """Get default API configuration"""
        return {
            "timeout": cls.DEFAULT_TIMEOUT,
            "retry_count": cls.DEFAULT_RETRY_COUNT
        }
