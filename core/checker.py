"""
Core assertion checker - encapsulates pytest assertions
"""
import json
from typing import Any, Dict, List, Optional, Union


class ResponseChecker:
    """Generic response assertion checker"""
    
    @staticmethod
    def assert_status_code(response, expected_code: int, message: str = None):
        """Assert response status code"""
        status_code = getattr(response, 'status_code', None)
        if status_code is None:
            # Try to get status code from different response types
            status_code = getattr(response, 'status', None)
        
        assert status_code == expected_code, \
            f"{message or 'Status code mismatch'}: expected {expected_code}, got {status_code}"
    
    @staticmethod
    def assert_json_response(response, expected_data: Dict = None, message: str = None):
        """Assert JSON response structure and content"""
        # Handle different response types
        if hasattr(response, 'data'):
            # Flask response
            try:
                data = json.loads(response.data)
            except json.JSONDecodeError:
                assert False, f"{message or 'Invalid JSON response'}: {response.data}"
        elif hasattr(response, 'json'):
            # Requests response
            try:
                data = response.json()
            except (json.JSONDecodeError, ValueError):
                # Handle empty response or non-JSON response
                assert False, f"{message or 'Invalid JSON response'}: {response.text}"
        elif hasattr(response, 'text'):
            # Generic response with text
            try:
                data = json.loads(response.text)
            except json.JSONDecodeError:
                assert False, f"{message or 'Invalid JSON response'}: {response.text}"
        elif isinstance(response, dict):
            # Already a dict
            data = response
        else:
            assert False, f"{message or 'Cannot parse response'}: {response}"
        
        if expected_data:
            assert data == expected_data, \
                f"{message or 'Response data mismatch'}: expected {expected_data}, got {data}"
        
        return data
    
    @staticmethod
    def assert_response_contains(response, key: str, value: Any = None, message: str = None):
        """Assert response contains specific key and optionally value"""
        data = ResponseChecker.assert_json_response(response)
        
        assert key in data, f"{message or f'Key not found'}: {key}"
        
        if value is not None:
            assert data[key] == value, \
                f"{message or f'Value mismatch for key {key}'}: expected {value}, got {data[key]}"
    
    @staticmethod
    def assert_response_structure(response_or_data, required_keys: List[str], message: str = None):
        """Assert response has required structure; accepts response object or dict"""
        # If it's a Flask response-like object, parse JSON; else assume it's already a dict
        if hasattr(response_or_data, "data"):
            data = ResponseChecker.assert_json_response(response_or_data)
        else:
            data = response_or_data
        
        for key in required_keys:
            assert key in data, f"{message or f'Required key missing'}: {key}"


class DataChecker:
    """Generic data validation checker"""
    
    @staticmethod
    def assert_data_structure(data: Dict, required_fields: List[str], message: str = None):
        """Assert data has required structure"""
        for field in required_fields:
            assert field in data, f"{message or f'Required field missing'}: {field}"
    
    @staticmethod
    def assert_data_type(data: Any, expected_type: type, field_name: str = None, message: str = None):
        """Assert data is of expected type"""
        assert isinstance(data, expected_type), \
            f"{message or f'Type mismatch for {field_name or data}'}: expected {expected_type.__name__}, got {type(data).__name__}"
    
    # Specific type assertion methods
    @staticmethod
    def assert_int_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is integer type"""
        DataChecker.assert_data_type(data, int, field_name, message)
    
    @staticmethod
    def assert_str_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is string type"""
        DataChecker.assert_data_type(data, str, field_name, message)
    
    @staticmethod
    def assert_bool_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is boolean type"""
        DataChecker.assert_data_type(data, bool, field_name, message)
    
    @staticmethod
    def assert_float_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is float type"""
        DataChecker.assert_data_type(data, float, field_name, message)
    
    @staticmethod
    def assert_list_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is list type"""
        DataChecker.assert_data_type(data, list, field_name, message)
    
    @staticmethod
    def assert_dict_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is dict type"""
        DataChecker.assert_data_type(data, dict, field_name, message)
    
    @staticmethod
    def assert_list_structure(data_list: List[Dict], expected_count: int = None, message: str = None):
        """Assert list structure"""
        assert isinstance(data_list, list), f"{message or 'Data must be a list'}"
        
        if expected_count is not None:
            assert len(data_list) == expected_count, \
                f"{message or f'Expected {expected_count} items, got {len(data_list)}'}"
    
    @staticmethod
    def assert_not_none(data: Any, field_name: str = None, message: str = None):
        """Assert data is not None"""
        assert data is not None, f"{message or f'{field_name or data} cannot be None'}"
    
    @staticmethod
    def assert_not_empty(data: Any, field_name: str = None, message: str = None):
        """Assert data is not empty (for strings, lists, dicts)"""
        if isinstance(data, str):
            assert data.strip() != "", f"{message or f'{field_name or data} cannot be empty string'}"
        elif isinstance(data, (list, dict)):
            assert len(data) > 0, f"{message or f'{field_name or data} cannot be empty'}"
        else:
            assert data is not None, f"{message or f'{field_name or data} cannot be None'}"
    
    @staticmethod
    def assert_in_range(data: Union[int, float], min_value: Union[int, float], max_value: Union[int, float], 
                       field_name: str = None, message: str = None):
        """Assert numeric data is within range"""
        assert min_value <= data <= max_value, \
            f"{message or f'{field_name or data} must be between {min_value} and {max_value}, got {data}'}"
    
    @staticmethod
    def assert_string_length(data: str, min_length: int = 0, max_length: int = None, 
                            field_name: str = None, message: str = None):
        """Assert string length is within range"""
        DataChecker.assert_str_data(data, field_name, message)
        assert len(data) >= min_length, \
            f"{message or f'{field_name or data} length must be at least {min_length}, got {len(data)}'}"
        
        if max_length is not None:
            assert len(data) <= max_length, \
                f"{message or f'{field_name or data} length must be at most {max_length}, got {len(data)}'}"


class ErrorChecker:
    """Generic error response checker"""
    
    @staticmethod
    def assert_error_response(response, expected_error: str = None, expected_code: int = None):
        """Assert error response structure"""
        if expected_code:
            ResponseChecker.assert_status_code(response, expected_code)
        
        data = ResponseChecker.assert_json_response(response)
        
        assert "error" in data, "Error response must contain 'error' field"
        
        if expected_error:
            assert data["error"] == expected_error, \
                f"Expected error: {expected_error}, got: {data['error']}"


class PerformanceChecker:
    """Performance assertion checker"""
    
    @staticmethod
    def assert_response_time(response, max_time: float, message: str = None):
        """Assert response time is within limit"""
        # This would need to be implemented with timing measurement
        # For now, just a placeholder
        pass
