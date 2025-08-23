# PTE Framework Static Log Usage Guide

## 📋 Overview

This guide explains how to use the simplified static `Log` class for easy logging across all layers (app, biz, test) without needing to manage LogID explicitly.

## 🎯 What is Static Log?

The static `Log` class provides a simple interface for logging that automatically handles LogID generation and management. You can use it like `Log.info()`, `Log.warn()`, `Log.error()` without worrying about LogID details.

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

## 📝 Available Methods

### Basic Logging
```python
Log.info(message: str, data: Optional[Dict] = None)
Log.warning(message: str, data: Optional[Dict] = None)
Log.error(message: str, data: Optional[Dict] = None)
Log.debug(message: str, data: Optional[Dict] = None)
```

### Test Lifecycle
```python
Log.start_test(test_method_name: str)
Log.end_test(test_method_name: str, status: str = "PASSED")
Log.test_start(test_name: str)
Log.test_complete(test_name: str, status: str = "PASSED")
```

### Assertions and Validation
```python
Log.assertion(description: str, condition: bool, expected: Any = None, actual: Any = None)
Log.data_validation(field: str, expected: Any, actual: Any, passed: bool)
```

### API Calls
```python
Log.api_call(method: str, url: str, status_code: Optional[int] = None, 
             response_time: Optional[float] = None, request_data: Optional[Dict] = None,
             response_data: Optional[Dict] = None)
```

### Headers and LogID
```python
Log.get_logid() -> str
Log.get_headers_with_logid(additional_headers: Optional[Dict] = None) -> Dict[str, str]
Log.set_logid(logid: str)
```

### Allure Integration
```python
Log.step(step_name: str)  # Returns decorator for Allure steps
```

## 🔧 Advanced Usage

### 1. Logging with Data

```python
# Log with structured data
Log.info("User operation completed", {
    "user_id": 123,
    "operation": "create",
    "status": "success"
})

# Log errors with context
Log.error("Database connection failed", {
    "error_type": "ConnectionError",
    "database": "users_db",
    "retry_count": 3
})
```

### 2. Assertions with Context

```python
# Simple assertion
Log.assertion("User ID validation", user_id is not None)

# Detailed assertion
Log.assertion(
    description="User age validation",
    condition=18 <= user_age <= 100,
    expected="18-100",
    actual=user_age
)
```

### 3. Data Validation

```python
# Validate data types
Log.data_validation("user_id", "integer", type(user_id).__name__, isinstance(user_id, int))
Log.data_validation("user_name", "string", type(user_name).__name__, isinstance(user_name, str))

# Validate business rules
Log.data_validation("email_format", "valid_email", "invalid_format", "@" in email)
```

### 4. API Call Logging

```python
# Log API calls with details
Log.api_call(
    method="POST",
    url="/api/users",
    status_code=201,
    response_time=0.5,
    request_data={"user": {"name": "John"}},
    response_data={"id": 1, "name": "John"}
)
```

### 5. Headers with LogID

```python
# Get headers with current LogID
headers = Log.get_headers_with_logid({
    'Authorization': 'Bearer token123',
    'Custom-Header': 'value'
})

# Result:
# {
#     'logId': 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6',
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer token123',
#     'Custom-Header': 'value'
# }
```

## 📊 Log Output Format

### Console Output
```
2024-01-01 12:00:00 - [PTELogger] - [LOGID:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6] - INFO - 🚀 Starting test: test_user_creation
2024-01-01 12:00:00 - [PTELogger] - [LOGID:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6] - INFO - Creating user in app layer
2024-01-01 12:00:00 - [PTELogger] - [LOGID:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6] - INFO - ✅ Test completed: test_user_creation - PASSED
```

## 🔄 Automatic LogID Management

### 1. Automatic Generation
- LogID is automatically generated when first needed
- Same LogID is used throughout the entire session
- No need to manually manage LogID

### 2. Session Persistence
```python
# LogID is automatically generated and reused
logid1 = Log.get_logid()  # First call generates LogID
logid2 = Log.get_logid()  # Same LogID returned
assert logid1 == logid2   # True
```

### 3. Manual LogID Setting
```python
# Set custom LogID if needed
Log.set_logid("mycustomlogid1234567890abcdefghijklmnopqrstuvwxyz")
```

## 🎨 Best Practices

### 1. Consistent Usage
```python
# Good: Use Log class consistently
def process_data(self, data):
    Log.info("Processing data", {"data_size": len(data)})
    
    try:
        result = self.business_logic(data)
        Log.info("Data processed successfully", {"result": result})
        return result
    except Exception as e:
        Log.error("Data processing failed", {"error": str(e)})
        raise
```

### 2. Error Handling
```python
def risky_operation(self):
    try:
        # Risky operation
        result = self.perform_operation()
        Log.info("Operation successful", {"result": result})
        return result
    except Exception as e:
        Log.error("Operation failed", {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "operation": "perform_operation"
        })
        raise
```

### 3. Performance Monitoring
```python
import time

def monitored_operation(self):
    start_time = time.time()
    
    try:
        result = self.expensive_operation()
        response_time = time.time() - start_time
        
        Log.info("Operation completed", {
            "response_time": response_time,
            "result_size": len(result)
        })
        return result
    except Exception as e:
        response_time = time.time() - start_time
        Log.error("Operation failed", {
            "response_time": response_time,
            "error": str(e)
        })
        raise
```

## 🔍 Debugging with Static Log

### 1. Finding Logs
```bash
# Search for specific LogID in logs
grep "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6" test.log
```

### 2. Allure Report Integration
- LogID appears in test title and description
- All log entries include LogID for easy tracing
- API calls are logged with request/response data
- Attachments include LogID for debugging

## 🚨 Common Issues and Solutions

### Issue 1: LogID Changes During Test
```python
# Problem: LogID changes during test execution
# Solution: LogID is automatically managed and consistent
logid1 = Log.get_logid()
# ... some operations ...
logid2 = Log.get_logid()
assert logid1 == logid2  # Should be True
```

### Issue 2: Missing LogID in Headers
```python
# Problem: LogID not in API request headers
# Solution: Use Log.get_headers_with_logid()
headers = Log.get_headers_with_logid()
# Headers automatically include LogID
```

### Issue 3: No Logs Appearing
```python
# Problem: No logs appearing in output
# Solution: Ensure proper import and usage
from core.logger import Log
Log.info("Test message")  # Should appear in logs
```

## 📚 Integration Examples

### Flask Application Integration
```python
from flask import Flask, request, jsonify
from core.logger import Log

app = Flask(__name__)

@app.route('/api/users', methods=['POST'])
def create_user():
    Log.info("Creating user via API")
    
    try:
        user_data = request.json
        Log.info("User data received", {"user_data": user_data})
        
        # Process user creation
        user_id = create_user_in_database(user_data)
        
        Log.info("User created successfully", {"user_id": user_id})
        
        return jsonify({
            "id": user_id,
            "status": "created"
        }), 201
        
    except Exception as e:
        Log.error("User creation failed", {"error": str(e)})
        return jsonify({"error": str(e)}), 500
```

### Django Application Integration
```python
from django.http import JsonResponse
from core.logger import Log

def create_user(request):
    if request.method == 'POST':
        Log.info("Creating user via Django")
        
        try:
            user_data = request.POST
            Log.info("User data received", {"user_data": user_data})
            
            # Process user creation
            user_id = create_user_in_database(user_data)
            
            Log.info("User created successfully", {"user_id": user_id})
            
            return JsonResponse({
                "id": user_id,
                "status": "created"
            }, status=201)
            
        except Exception as e:
            Log.error("User creation failed", {"error": str(e)})
            return JsonResponse({"error": str(e)}, status=500)
```

## 🎉 Benefits

### 1. **Simplicity**
- No need to manage logger instances
- No need to pass logger parameters
- Simple `Log.info()` syntax

### 2. **Automatic LogID Management**
- LogID is automatically generated and managed
- Consistent LogID throughout session
- No manual LogID handling required

### 3. **Cross-Layer Compatibility**
- Works in app, biz, and test layers
- Same interface everywhere
- Consistent logging format

### 4. **Rich Features**
- Allure integration
- Structured data logging
- Performance monitoring
- Error context

The static `Log` class provides a clean, simple interface for logging across all layers while automatically handling LogID management behind the scenes.
