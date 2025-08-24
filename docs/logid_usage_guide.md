# PTE Framework LogID Usage Guide

## 📋 Overview

This guide explains how to use the enhanced logging functionality with LogID support in the PTE Framework. The LogID feature provides end-to-end tracing from test case execution to API requests and responses.

## 🎯 What is LogID?

LogID is a unique identifier (containing numbers and lowercase letters) that:
- **Tracks test execution**: From test start to completion
- **Links API requests**: All API calls include the LogID in headers
- **Enables tracing**: Connect logs across test framework and target application
- **Supports debugging**: Easy to locate specific test execution in logs

## ✨ Key Features Implemented

### 1. **32-Character LogID Generation**
- **Format**: Numbers + lowercase letters (e.g., `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6`)
- **Uniqueness**: Based on timestamp + random data + UUID + MD5 hash
- **Traceability**: Each test case gets a unique LogID for the entire execution

### 2. **Enhanced Logging System**
- **Structured Logging**: Consistent format with timestamps and LogID
- **Log Levels**: INFO, WARNING, ERROR, DEBUG with LogID context
- **Allure Integration**: LogID appears in test reports and attachments
- **Console Output**: Formatted logs with LogID for easy searching

### 3. **API Client Integration**
- **Automatic LogID Headers**: All API requests include `logId` header
- **Request/Response Logging**: Detailed API call tracking with timing
- **Error Handling**: Comprehensive error logging with LogID context
- **Performance Monitoring**: Response time tracking for each API call

### 4. **Business Operations Support**
- **LogID Propagation**: Business operations inherit LogID from test context
- **Enhanced Tracing**: All business logic operations include LogID
- **Error Context**: Detailed error information with LogID for debugging

## 🏗️ Architecture Components

### Core Logger Module (`core/logger.py`)
```python
# Key Classes
- LogIdGenerator: Generates unique 32-character LogIDs
- PTELogger: Base logger with LogID support
- TestLogger: Test-specific logger with lifecycle management

# Key Features
- Automatic LogID generation
- Structured logging with timestamps
- Allure integration
- Header generation with LogID
- API call logging
- Assertion and validation logging
```

### Enhanced API Client (`api/client.py`)
```python
# Enhanced Features
- LogID parameter in constructor
- Automatic LogID header injection
- Request/response logging with timing
- Error handling with LogID context
- Performance monitoring
```

### Business Operations (`biz/department/user/operations.py`)
```python
# Enhanced Features
- LogID parameter support
- Enhanced request logging
- Error context with LogID
- Retry mechanism with LogID tracking
```

## 🚀 Quick Start

### 1. Basic Usage in Test Cases

```python
from core.logger import Log

class TestYourFeature:
    def setup_method(self):
        # No need to initialize logger - Log class handles it automatically
        pass
    
    def test_example(self):
        # Start test with automatic LogID
        Log.start_test("test_example")
        
        try:
            # Your test logic here
            Log.info("Test step executed")
            
            # End test successfully
            Log.end_test("test_example", "PASSED")
        except Exception as e:
            # End test with failure
            Log.error(f"Test failed: {str(e)}")
            Log.end_test("test_example", "FAILED")
            raise
```

### 2. API Client with LogID

```python
from api.client import APIClient
from core.logger import Log

class TestAPI:
    def setup_method(self):
        # Initialize API client (LogID handled automatically)
        self.api_client = APIClient()
    
    def test_api_call(self):
        Log.start_test("test_api_call")
        
        # Make API call with logging
        response = self.api_client.get("/api/users")
        
        Log.end_test("test_api_call", "PASSED")
```

### 3. Business Operations with LogID

```python
from biz.department.user.operations import UserOperations
from core.logger import Log

class TestUserOperations:
    def setup_method(self):
        # Initialize operations (LogID handled automatically)
        self.user_ops = UserOperations()
    
    def test_user_creation(self):
        Log.start_test("test_user_creation")
        
        # Call business operation with logging
        result = self.user_ops.create_user(user_data)
        
        Log.end_test("test_user_creation", "PASSED")
```

## 📝 LogID Generation

### Automatic Generation
```python
from core.logger import Log

# LogID is automatically generated when needed
current_logid = Log.get_logid()
print(f"Current LogID: {current_logid}")
```

### Manual LogID Assignment
```python
from core.logger import Log, generate_logid

# Generate a new LogID manually
logid = generate_logid()
Log.set_logid(logid)
```

## 🔧 Advanced Features

### 1. Automatic LogID Management

The framework automatically handles LogID generation and management through pytest fixtures:

```python
# This happens automatically for every test
@pytest.fixture(autouse=True)
def auto_logid():
    """Automatically generate and set LogID for each test case"""
    logid = generate_logid()
    Log.set_logid(logid)
    Log._get_logger()._add_logid_attachment("auto_generated")
    yield logid
```

### 2. LogID Attachment to Allure Reports

LogID is automatically attached to Allure reports for easy tracing:

```python
# This happens automatically when LogID is set
Log._get_logger()._add_logid_attachment("auto_generated")
```

### 3. API Request Logging

All API requests automatically include LogID in headers:

```python
# API client automatically adds LogID to headers
headers = {
    'Content-Type': 'application/json',
    'logId': current_logid  # Added automatically
}
```

## 📊 Log Output Examples

### Console Output Format
```
2024-01-01 12:00:00 - [TestLogger] - [LogId:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6] - INFO - 🚀 Starting test: test_user_creation
2024-01-01 12:00:00 - [TestLogger] - [LogId:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6] - INFO - 🌐 API Call: POST /api/users - Status: 201 - Time: 0.50s
2024-01-01 12:00:00 - [TestLogger] - [LogId:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6] - INFO - ✅ Test completed: test_user_creation - PASSED
```

### API Request Headers
```http
GET /api/users HTTP/1.1
Host: localhost:5001
logId: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
Content-Type: application/json
Authorization: Bearer token123
```

## 🔄 End-to-End Tracing Flow

### 1. Test Case Execution
```python
def test_user_creation(self):
    # 1. Generate LogID for test case
    self.logger = get_test_logger("TestUserCreation")
    logid = self.logger.get_logid()  # a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
    
    # 2. Start test with LogID
    self.logger.start_test("test_user_creation")
    
    # 3. Initialize components with LogID
    self.api_client = APIClient(logid=logid)
    self.user_ops = UserOperations(logid=logid)
```

## 📊 Logging Methods

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

## 🚨 LogID Uniqueness Issues and Solutions

### Problem Description

In the PTE Framework's automatic LogID functionality, it was discovered that each test case's LogID appeared as the same value in log files, rather than the expected unique values.

### Root Cause Analysis

1. **Log Handler Creation Timing**: File handlers were created during `PTELogger` initialization with fixed filenames
2. **Handler Reuse**: Even when LogID was updated, handlers continued writing to the same file
3. **File Locking**: Log files were locked by handlers, preventing dynamic switching

### Solution: Test Case-Separated Log Files

#### Core Approach

By creating independent log files for each test case, we ensure that each test case's logs have unique LogIDs, and log file names include test case information.

#### Implementation

1. **Modified Log Filename Format**:
```yaml
filename_format: "pte_{datetime}_{testcase}_{logid}_{level}.log"
```

2. **Refactored Log Class**: Merged `PTELogger`, `TestLogger`, and static `Log` classes into a unified `Log` class

3. **Modified LogFileHandler**: Supports dynamic filename generation with test case names and LogIDs

4. **Updated conftest.py**: Automatically retrieves test case names and sets unique LogIDs

#### Verification Results

**Test Case 1**:
- **Filename**: `pte_20250824_114652_test_logid_debug_1_2024ac37ca755ea0dc95715c9cf1fa4a_all.log`
- **LogID**: `2024ac37ca755ea0dc95715c9cf1fa4a`
- **Test Case**: `test_logid_debug_1`

**Test Case 2**:
- **Filename**: `pte_20250824_114652_test_logid_debug_2_e081f1e56977bfc204416580ff8b0e1f_all.log`
- **LogID**: `e081f1e56977bfc204416580ff8b0e1f`
- **Test Case**: `test_logid_debug_2`

#### Benefits

1. **Uniqueness Guarantee**: Each test case has an independent LogID
2. **File Separation**: Each test case's logs are written to independent files
3. **Easy Tracing**: Filenames include test case names and LogIDs
4. **Zero Configuration**: Users don't need to manually set LogIDs
5. **Backward Compatibility**: Maintains existing API unchanged

## 📚 Related Documentation

- [File Logging Guide](file_logging_guide.md) - Local file logging capabilities
- [Parallel Testing Guide](parallel_testing_guide.md) - Running tests in parallel
- [Static Log Usage Guide](static_log_usage_guide.md) - Simplified logging interface
