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


class Checker:
    """Generic data validation checker - renamed from DataChecker for shorter usage"""
    
    # ==================== Data Structure Assertions ====================
    
    @staticmethod
    def assert_data_structure(data: Dict, required_fields: List[str], message: str = None):
        """Assert data has required structure"""
        for field in required_fields:
            assert field in data, f"{message or f'Required field missing'}: {field}"
    
    @staticmethod
    def assert_field_exists(data: Dict, field_name: str, message: str = None):
        """Assert field exists in data dictionary"""
        assert field_name in data, f"{message or f'Field not found'}: {field_name}"
    
    @staticmethod
    def assert_field_not_exists(data: Dict, field_name: str, message: str = None):
        """Assert field does not exist in data dictionary"""
        assert field_name not in data, f"{message or f'Field should not exist'}: {field_name}"
    
    @staticmethod
    def assert_list_structure(data_list: List[Dict], expected_count: int = None, message: str = None):
        """Assert list structure"""
        assert isinstance(data_list, list), f"{message or 'Data must be a list'}"
        
        if expected_count is not None:
            assert len(data_list) == expected_count, \
                f"{message or f'Expected {expected_count} items, got {len(data_list)}'}"
    
    # ==================== Data Type Assertions ====================
    
    @staticmethod
    def assert_data_type(data: Any, expected_type: type, field_name: str = None, message: str = None):
        """Assert data is of expected type"""
        assert isinstance(data, expected_type), \
            f"{message or f'Type mismatch for {field_name or data}'}: expected {expected_type.__name__}, got {type(data).__name__}"
    
    @staticmethod
    def assert_int_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is integer type"""
        Checker.assert_data_type(data, int, field_name, message)
    
    @staticmethod
    def assert_str_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is string type"""
        Checker.assert_data_type(data, str, field_name, message)
    
    @staticmethod
    def assert_bool_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is boolean type"""
        Checker.assert_data_type(data, bool, field_name, message)
    
    @staticmethod
    def assert_float_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is float type"""
        Checker.assert_data_type(data, float, field_name, message)
    
    @staticmethod
    def assert_list_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is list type"""
        Checker.assert_data_type(data, list, field_name, message)
    
    @staticmethod
    def assert_dict_data(data: Any, field_name: str = None, message: str = None):
        """Assert data is dict type"""
        Checker.assert_data_type(data, dict, field_name, message)
    
    # ==================== Data Value Assertions ====================
    
    @staticmethod
    def assert_equal(actual: Any, expected: Any, field_name: str = None, message: str = None):
        """Assert actual value equals expected value"""
        assert actual == expected, \
            f"{message or f'Value mismatch for {field_name or "data"}'}: expected {expected}, got {actual}"
    
    @staticmethod
    def assert_not_equal(actual: Any, expected: Any, field_name: str = None, message: str = None):
        """Assert actual value does not equal expected value"""
        assert actual != expected, \
            f"{message or f'Value should not equal for {field_name or "data"}'}: got {actual}"
    
    @staticmethod
    def assert_field_value(data: Dict, field_name: str, expected_value: Any, message: str = None):
        """Assert field value in dictionary equals expected value"""
        Checker.assert_field_exists(data, field_name, message)
        Checker.assert_equal(data[field_name], expected_value, field_name, message)
    
    @staticmethod
    def assert_dict_equal(actual: Dict, expected: Dict, message: str = None):
        """Assert two dictionaries are equal"""
        assert actual == expected, \
            f"{message or 'Dictionary mismatch'}: expected {expected}, got {actual}"
    
    # ==================== Data Existence Assertions ====================
    
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
    def assert_length(data: Any, expected_length: int, field_name: str = None, message: str = None):
        """Assert data has expected length"""
        actual_length = len(data)
        assert actual_length == expected_length, \
            f"{message or f'Length mismatch for {field_name or "data"}'}: expected {expected_length}, got {actual_length}"
    
    @staticmethod
    def assert_length_greater_than(data: Any, min_length: int, field_name: str = None, message: str = None):
        """Assert data length is greater than minimum"""
        actual_length = len(data)
        assert actual_length > min_length, \
            f"{message or f'Length too short for {field_name or "data"}'}: must be > {min_length}, got {actual_length}"
    
    # ==================== Comparison Assertions ====================
    
    @staticmethod
    def assert_greater_than(actual: Union[int, float], expected: Union[int, float], field_name: str = None, message: str = None):
        """Assert actual value is greater than expected value"""
        assert actual > expected, \
            f"{message or f'{field_name or actual} must be greater than {expected}, got {actual}'}"
    
    @staticmethod
    def assert_greater_equal(actual: Union[int, float], expected: Union[int, float], field_name: str = None, message: str = None):
        """Assert actual value is greater than or equal to expected value"""
        assert actual >= expected, \
            f"{message or f'{field_name or actual} must be greater than or equal to {expected}, got {actual}'}"
    
    @staticmethod
    def assert_less_than(actual: Union[int, float], expected: Union[int, float], field_name: str = None, message: str = None):
        """Assert actual value is less than expected value"""
        assert actual < expected, \
            f"{message or f'{field_name or actual} must be less than {expected}, got {actual}'}"
    
    @staticmethod
    def assert_less_equal(actual: Union[int, float], expected: Union[int, float], field_name: str = None, message: str = None):
        """Assert actual value is less than or equal to expected value"""
        assert actual <= expected, \
            f"{message or f'{field_name or actual} must be less than or equal to {expected}, got {actual}'}"
    
    # ==================== Range and Validation Assertions ====================
    
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
        Checker.assert_str_data(data, field_name, message)
        assert len(data) >= min_length, \
            f"{message or f'{field_name or data} length must be at least {min_length}, got {len(data)}'}"
        
        if max_length is not None:
            assert len(data) <= max_length, \
                f"{message or f'{field_name or data} length must be at most {max_length}, got {len(data)}'}"
    
    # ==================== Object and Attribute Assertions ====================
    
    @staticmethod
    def assert_has_attr(obj: Any, attr_name: str, message: str = None):
        """Assert object has attribute"""
        assert hasattr(obj, attr_name), \
            f"{message or f'Object missing attribute'}: {attr_name}"
    
    @staticmethod
    def assert_attr_equal(obj: Any, attr_name: str, expected_value: Any, message: str = None):
        """Assert object attribute equals expected value"""
        Checker.assert_has_attr(obj, attr_name, message)
        actual_value = getattr(obj, attr_name)
        assert actual_value == expected_value, \
            f"{message or f'Attribute {attr_name} mismatch'}: expected {expected_value}, got {actual_value}"
    
    # ==================== Boolean and Condition Assertions ====================
    
    @staticmethod
    def assert_true(condition: bool, message: str = None):
        """Assert condition is True"""
        assert condition, f"{message or 'Condition should be True'}"
    
    @staticmethod
    def assert_false(condition: bool, message: str = None):
        """Assert condition is False"""
        assert not condition, f"{message or 'Condition should be False'}"
    
    @staticmethod
    def assert_is_instance(obj: Any, expected_type: type, message: str = None):
        """Assert object is instance of expected type"""
        assert isinstance(obj, expected_type), \
            f"{message or f'Object should be instance of {expected_type.__name__}'}: got {type(obj).__name__}"
    
    # ==================== Collection Assertions ====================
    
    @staticmethod
    def assert_contains(container: Any, item: Any, message: str = None):
        """Assert container contains item"""
        assert item in container, \
            f"{message or f'Container should contain item'}: {item}"
    
    @staticmethod
    def assert_not_contains(container: Any, item: Any, message: str = None):
        """Assert container does not contain item"""
        assert item not in container, \
            f"{message or f'Container should not contain item'}: {item}"
    
    @staticmethod
    def assert_list_contains(data_list: List, item: Any, message: str = None):
        """Assert list contains item"""
        Checker.assert_list_data(data_list, message)
        Checker.assert_contains(data_list, item, message)
    
    @staticmethod
    def assert_dict_contains_key(data_dict: Dict, key: str, message: str = None):
        """Assert dictionary contains key"""
        Checker.assert_dict_data(data_dict, message)
        Checker.assert_contains(data_dict, key, message)
    
    @staticmethod
    def assert_dict_contains_value(data_dict: Dict, value: Any, message: str = None):
        """Assert dictionary contains value"""
        Checker.assert_dict_data(data_dict, message)
        assert value in data_dict.values(), \
            f"{message or f'Dictionary should contain value'}: {value}"


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


# Backward compatibility alias
DataChecker = Checker
