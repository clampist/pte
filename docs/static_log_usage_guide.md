# PTE Framework Static Log Usage Guide

## 📋 Overview

This guide explains how to use the simplified static `Log` class for easy logging across all layers (app, biz, test) without needing to manage LogID explicitly.

## 🎯 What is Static Log?

The static `Log` class provides a simple interface for logging that automatically handles LogID generation and management. You can use it like `Log.info()`, `Log.warn()`, `Log.error()` without worrying about LogID details.

## 🎯 Objectives Achieved

### 1. **Removed LogID Logic Intrusion**
- ✅ Removed LogID logic from **biz layer** (`operations.py`)
- ✅ Removed LogID logic from **app layer** (no changes needed)
- ✅ Removed LogID logic from **test layer** (converted to static Log)
- ✅ Kept LogID logic in **API layer** only (as requested)

### 2. **Converted to Static Log Usage**
- ✅ Updated `business_real_api_tests_with_logid.py` to use `Log.xxx` static methods
- ✅ Removed `self.logger` usage in favor of static `Log` class
- ✅ Simplified test setup and execution

### 3. **Added Print Replacement**
- ✅ Added `Log.raw()` method for raw print-like logging
- ✅ Added `Log.print()` method as alias for `Log.raw()`
- ✅ Both methods work like original `print()` but with Allure integration

## 🚀 Quick Start

### 1. Basic Usage

```python
from core.logger import Log

# Simple logging
Log.info("This is an info message")
Log.warning("This is a warning message")
Log.error("This is an error message")
Log.debug("This is a debug message")
```

### 2. Test Layer Usage

```python
import pytest
from core.logger import Log

class TestUserManagement:
    def setup_method(self):
        # No need to initialize logger - Log class handles it automatically
        pass
    
    def test_user_creation(self):
        # Start test with automatic LogID
        Log.start_test("test_user_creation")
        
        try:
            # Your test logic here
            Log.info("Creating user")
            
            # End test successfully
            Log.end_test("test_user_creation", "PASSED")
        except Exception as e:
            # End test with failure
            Log.error(f"Test failed: {str(e)}")
            Log.end_test("test_user_creation", "FAILED")
            raise
```

### 3. App Layer Usage

```python
from core.logger import Log

class UserAppService:
    def create_user(self, user_data):
        """Create user with automatic logging"""
        Log.info("Creating user in app layer", {"user_data": user_data})
        
        try:
            # Business logic here
            result = {"id": 1, "status": "created"}
            
            Log.info("User created successfully", {"result": result})
            return result
            
        except Exception as e:
            Log.error("User creation failed", {"error": str(e)})
            raise
```

### 4. Biz Layer Usage

```python
from core.logger import Log

class UserBizService:
    def process_user_data(self, user_data):
        """Process user data with automatic logging"""
        Log.info("Processing user data in biz layer", {"user_data": user_data})
        
        try:
            # Business logic here
            processed_data = {"processed": True, "data": user_data}
            
            Log.info("User data processed successfully", {"processed_data": processed_data})
            return processed_data
            
        except Exception as e:
            Log.error("User data processing failed", {"error": str(e)})
            raise
```

## 🔧 Changes Made

### 1. **Biz Layer Cleanup** (`biz/department/user/operations.py`)

#### Before:
```python
def __init__(self, env: str = None, custom_headers: Dict[str, str] = None, logid: str = None):
    # Generate or use provided logid
    self.logid = logid or generate_logid()
    # Add logid to headers
    self.headers['logId'] = self.logid

def _make_request(self, method: str, endpoint: str, data: Dict = None, 
                 params: Dict = None, expected_status: int = 200, logger=None):
    # Log API call if logger is provided
    if logger:
        logger.api_call(...)
```

#### After:
```python
def __init__(self, env: str = None, custom_headers: Dict[str, str] = None):
    # No LogID logic - handled by API layer

def _make_request(self, method: str, endpoint: str, data: Dict = None, 
                 params: Dict = None, expected_status: int = 200):
    # Log API call using static Log class
    from core.logger import Log
    Log.api_call(...)
```

### 2. **Test Layer Conversion** (`test/department/user/business_real_api_tests_with_logid.py`)

#### Before:
```python
@pytest.fixture(autouse=True)
def setup(self):
    # Initialize logger with logid
    self.logger = get_test_logger("TestBusinessRealAPIWithLogID")
    # Initialize components with logid
    self.api_client = APIClient(logid=self.logger.get_logid())
    self.user_ops = UserOperations(logid=self.logger.get_logid())

def test_real_api_connection_with_logid(self):
    self.logger.start_test("test_real_api_connection_with_logid")
    self.logger.info("Starting real API connection test with logid")
    self.logger.assertion("API client initialization", ...)
    self.logger.end_test("test_real_api_connection_with_logid", "PASSED")
```

#### After:
```python
@pytest.fixture(autouse=True)
def setup(self):
    # No logger initialization needed
    # Initialize components (no need to pass logid)
    self.api_client = APIClient()
    self.user_ops = UserOperations()

def test_real_api_connection_with_static_log(self):
    Log.start_test("test_real_api_connection_with_static_log")
    Log.info("Starting real API connection test with static log")
    Log.assertion("API client initialization", ...)
    Log.end_test("test_real_api_connection_with_static_log", "PASSED")
```

### 3. **Static Log Class Enhancement** (`core/logger.py`)

#### Added Methods:
```python
@classmethod
def raw(cls, message: str, *args, **kwargs):
    """Raw print-like logging without LogID prefix (replaces print())"""
    # Format message with args and kwargs like print()
    formatted_message = message
    if args:
        formatted_message += " " + " ".join(str(arg) for arg in args)
    if kwargs:
        formatted_message += " " + " ".join(f"{k}={v}" for k, v in kwargs.items())
    
    # Log without LogID prefix
    cls._log_without_logid("INFO", formatted_message)

@classmethod
def print(cls, message: str, *args, **kwargs):
    """Alias for Log.raw() - print-like logging"""
    cls.raw(message, *args, **kwargs)
```

## 📝 Available Methods

### Basic Logging
```python
Log.info("Information message")
Log.warning("Warning message")
Log.error("Error message")
Log.debug("Debug message")
```

### Test-Specific Logging
```python
Log.start_test("test_name")
Log.end_test("test_name", "PASSED")
Log.end_test("test_name", "FAILED")
```

### API Logging
```python
Log.api_call(
    method="POST",
    url="/api/users",
    status_code=201,
    response_time=0.5,
    request_data=data,
    response_data=response
)
```

### Data Validation Logging
```python
Log.data_validation("field_name", expected_value, actual_value, True)
Log.assertion("assertion_description", expected, actual, expected)
```

### Print Replacement
```python
Log.raw("Raw message without LogID prefix")
Log.print("Print-like message")  # Alias for Log.raw()
```

## 🎯 Best Practices

### 1. Use Static Log Class
- Prefer `Log.info()` over `self.logger.info()`
- No need to manage logger instances manually
- Automatic LogID handling

### 2. Consistent Test Structure
```python
def test_example(self):
    Log.start_test("test_example")
    try:
        # Test logic
        Log.info("Test step")
        # Assertions
        Log.end_test("test_example", "PASSED")
    except Exception as e:
        Log.error(f"Test failed: {e}")
        Log.end_test("test_example", "FAILED")
        raise
```

### 3. API Testing
```python
def test_api_endpoint(self):
    Log.start_test("test_api_endpoint")
    
    # API call with automatic logging
    response = self.api_client.post("/api/users", data=user_data)
    
    # Validation with logging
    Log.assertion("Status code check", 201, response.status_code, 201)
    
    Log.end_test("test_api_endpoint", "PASSED")
```

## 🔍 Troubleshooting

### 1. LogID Not Generated
- Ensure you're using the static `Log` class
- Check that pytest fixtures are loaded
- Verify `core/__init__.py` imports fixtures

### 2. LogID Not in API Headers
- Ensure API client is properly initialized
- Check that LogID is set before making API calls
- Verify API client configuration

### 3. LogID Not in Allure Reports
- Check Allure configuration
- Ensure LogID attachment is enabled
- Verify test execution with Allure

## 📚 Related Documentation

- [LogID Usage Guide](logid_usage_guide.md) - Comprehensive LogID functionality
- [File Logging Guide](file_logging_guide.md) - Local file logging capabilities
- [Parallel Testing Guide](parallel_testing_guide.md) - Running tests in parallel
