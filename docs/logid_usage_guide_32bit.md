# PTE Framework LogID Usage Guide (32-bit)

## 📋 Overview

This guide explains how to use the enhanced logging functionality with 32-bit LogID support in the PTE Framework. The LogID feature provides end-to-end tracing from test case execution to API requests and responses.

## 🎯 What is LogID?

LogID is a unique 32-character identifier (containing numbers and lowercase letters) that:
- **Tracks test execution**: From test start to completion
- **Links API requests**: All API calls include the LogID in headers
- **Enables tracing**: Connect logs across test framework and target application
- **Supports debugging**: Easy to locate specific test execution in logs

## 🚀 Quick Start

### 1. Basic Usage in Test Cases

```python
from core.logger import get_test_logger

class TestYourFeature:
    def setup_method(self):
        # Initialize logger with auto-generated LogID
        self.logger = get_test_logger("TestYourFeature")
    
    def test_example(self):
        # Start test with LogID
        self.logger.start_test("test_example")
        
        try:
            # Your test logic here
            self.logger.info("Test step executed")
            
            # End test successfully
            self.logger.end_test("test_example", "PASSED")
        except Exception as e:
            # End test with failure
            self.logger.error(f"Test failed: {str(e)}")
            self.logger.end_test("test_example", "FAILED")
            raise
```

### 2. API Client with LogID

```python
from api.client import APIClient
from core.logger import get_test_logger

class TestAPI:
    def setup_method(self):
        self.logger = get_test_logger("TestAPI")
        # Initialize API client with LogID
        self.api_client = APIClient(logid=self.logger.get_logid())
    
    def test_api_call(self):
        self.logger.start_test("test_api_call")
        
        # Make API call with logging
        response = self.api_client.get("/api/users", logger=self.logger)
        
        self.logger.end_test("test_api_call", "PASSED")
```

### 3. Business Operations with LogID

```python
from biz.department.user.operations import UserOperations
from core.logger import get_test_logger

class TestUserOperations:
    def setup_method(self):
        self.logger = get_test_logger("TestUserOperations")
        # Initialize operations with LogID
        self.user_ops = UserOperations(logid=self.logger.get_logid())
    
    def test_user_creation(self):
        self.logger.start_test("test_user_creation")
        
        # Call business operation with logging
        result = self.user_ops.create_user(user_data, logger=self.logger)
        
        self.logger.end_test("test_user_creation", "PASSED")
```

## 📝 LogID Generation

### Automatic Generation
```python
from core.logger import generate_logid

# Generate a new LogID
logid = generate_logid()
print(logid)  # e.g., "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"
```

### Manual LogID Assignment
```python
from core.logger import get_test_logger

# Use specific LogID
custom_logid = "mycustomlogid1234567890abcdefghijklmnopqrstuvwxyz"
logger = get_test_logger("TestClass", logid=custom_logid)
```

## 🔧 Advanced Usage

### 1. LogID in Headers

```python
# Get headers with LogID
headers = self.logger.get_headers_with_logid({
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

### 2. API Call Logging

```python
# Log API call with detailed information
self.logger.api_call(
    method="POST",
    url="/api/users",
    status_code=201,
    response_time=0.5,
    request_data={"user": {"name": "John"}},
    response_data={"id": 1, "name": "John"}
)
```

### 3. Assertion Logging

```python
# Log assertions with LogID
self.logger.assertion(
    description="User creation validation",
    condition=user_id is not None,
    expected="Not None",
    actual=user_id
)
```

### 4. Data Validation Logging

```python
# Log data validation with LogID
self.logger.data_validation(
    field="user_id",
    expected="integer",
    actual=type(user_id).__name__,
    passed=isinstance(user_id, int)
)
```

## 📊 Log Output Format

### Console Output
```
2024-01-01 12:00:00 - [TestLogger] - [LogId:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6] - INFO - 🚀 Starting test: test_user_creation
2024-01-01 12:00:00 - [TestLogger] - [LogId:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6] - INFO - 🌐 API Call: POST /api/users - Status: 201 - Time: 0.50s
2024-01-01 12:00:00 - [TestLogger] - [LogId:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6] - INFO - ✅ Test completed: test_user_creation - PASSED
```

### Allure Report Integration
- LogID appears in test title and description
- All log entries include LogID
- API calls are logged with request/response data
- Attachments include LogID for easy tracing

## 🔄 End-to-End Tracing

### 1. Test Framework Side
```python
def test_complete_workflow(self):
    self.logger.start_test("test_complete_workflow")
    
    # Step 1: Prepare data
    self.logger.info("Preparing test data", {"logid": self.logger.get_logid()})
    
    # Step 2: Make API call
    response = self.api_client.post("/api/users", json_data=user_data, logger=self.logger)
    
    # Step 3: Validate response
    self.logger.assertion("Response validation", response.status_code == 201)
    
    self.logger.end_test("test_complete_workflow", "PASSED")
```

### 2. Target Application Side
The target application receives the LogID in the `logId` header:
```
Headers:
{
    "logId": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6",
    "Content-Type": "application/json",
    "Authorization": "Bearer token123"
}
```

### 3. Tracing in Target Application
```python
# In your target application
@app.route('/api/users', methods=['POST'])
def create_user():
    logid = request.headers.get('logId')
    logger.info(f"Creating user with LogID: {logid}")
    
    # Process request
    user_data = request.json
    user = create_user_in_db(user_data)
    
    logger.info(f"User created successfully with LogID: {logid}", {
        "user_id": user.id,
        "logid": logid
    })
    
    return jsonify({"id": user.id, "logid": logid}), 201
```

## 🎨 Best Practices

### 1. Consistent LogID Usage
```python
# Good: Use the same LogID throughout the test
def test_user_workflow(self):
    self.logger.start_test("test_user_workflow")
    logid = self.logger.get_logid()
    
    # Use logid in all operations
    self.api_client = APIClient(logid=logid)
    self.user_ops = UserOperations(logid=logid)
    
    # All API calls will use the same LogID
    self.api_client.post("/api/users", json_data=user_data, logger=self.logger)
```

### 2. Error Handling with LogID
```python
def test_with_error_handling(self):
    self.logger.start_test("test_with_error_handling")
    
    try:
        # Test logic
        result = self.api_client.get("/api/users", logger=self.logger)
        self.logger.assertion("API call successful", result.status_code == 200)
        
    except Exception as e:
        # Log error with LogID
        self.logger.error(f"Test failed: {str(e)}", {
            "error_type": type(e).__name__,
            "logid": self.logger.get_logid()
        })
        self.logger.end_test("test_with_error_handling", "FAILED")
        raise
```

### 3. Performance Monitoring
```python
def test_performance(self):
    self.logger.start_test("test_performance")
    
    # Monitor API call performance
    start_time = time.time()
    response = self.api_client.get("/api/users", logger=self.logger)
    response_time = time.time() - start_time
    
    # Log performance metrics
    self.logger.info("Performance metrics", {
        "response_time": response_time,
        "status_code": response.status_code,
        "logid": self.logger.get_logid()
    })
    
    self.logger.end_test("test_performance", "PASSED")
```

## 🔍 Debugging with LogID

### 1. Finding Test Execution
```bash
# Search for specific LogID in logs
grep "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6" test.log
```

### 2. Allure Report Search
- Open Allure report
- Search for LogID in test details
- View all log entries for the specific test

### 3. Target Application Logs
```bash
# Search for LogID in application logs
grep "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6" app.log
```

## 🚨 Common Issues and Solutions

### Issue 1: LogID Not in Headers
```python
# Problem: LogID not appearing in API request headers
# Solution: Ensure LogID is added to headers
self.api_client = APIClient(logid=self.logger.get_logid())
# or
headers = self.logger.get_headers_with_logid()
```

### Issue 2: Multiple LogIDs in Same Test
```python
# Problem: Different LogIDs for different operations
# Solution: Use consistent LogID
logid = self.logger.get_logid()
self.api_client = APIClient(logid=logid)
self.user_ops = UserOperations(logid=logid)
```

### Issue 3: LogID Not in Allure Report
```python
# Problem: LogID not visible in Allure
# Solution: Ensure proper Allure integration
self.logger.start_test("test_name")  # This adds LogID to Allure
```

## 📚 Related Documentation

- [Allure Report Guide](allure_report_guide.md)
- [Logging Migration Guide](logging_migration_guide.md)
- [PTE Framework Documentation](README.md)

## 🔗 Integration Examples

### Flask Application Integration
```python
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/users', methods=['POST'])
def create_user():
    logid = request.headers.get('logId', 'unknown')
    logger.info(f"[LogId:{logid}] Creating user")
    
    try:
        user_data = request.json
        # Process user creation
        user_id = create_user_in_database(user_data)
        
        logger.info(f"[LogId:{logid}] User created successfully", {
            "user_id": user_id,
            "logid": logid
        })
        
        return jsonify({
            "id": user_id,
            "status": "created",
            "logid": logid
        }), 201
        
    except Exception as e:
        logger.error(f"[LogId:{logid}] User creation failed", {
            "error": str(e),
            "logid": logid
        })
        return jsonify({
            "error": str(e),
            "logid": logid
        }), 500
```

### Django Application Integration
```python
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        logid = request.headers.get('logId', 'unknown')
        logger.info(f"[LogId:{logid}] Creating user")
        
        try:
            user_data = request.POST
            # Process user creation
            user_id = create_user_in_database(user_data)
            
            logger.info(f"[LogId:{logid}] User created successfully", {
                "user_id": user_id,
                "logid": logid
            })
            
            return JsonResponse({
                "id": user_id,
                "status": "created",
                "logid": logid
            }, status=201)
            
        except Exception as e:
            logger.error(f"[LogId:{logid}] User creation failed", {
                "error": str(e),
                "logid": logid
            })
            return JsonResponse({
                "error": str(e),
                "logid": logid
            }, status=500)
```

This 32-bit LogID functionality provides comprehensive tracing capabilities for your test framework, enabling easy debugging and monitoring of test execution across both the test framework and target application.
