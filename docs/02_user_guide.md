# PTE Framework User Guide

## Overview

This guide covers all the features that users directly interact with when using the PTE Framework, including logging, testing, configuration management, and reporting.

## 🔧 Configuration

The framework uses YAML configuration files for flexible environment management:

```yaml
# config/env.yaml
idc: "local_test"  # Current IDC to test
env: "local"       # Current environment tag to test

# config/local_test.yaml
host: "http://localhost:5001"
database:
  mysql:
    host: "127.0.0.1"
    port: 3306
    username: "root"
    password: "password"
    database: "pte"
```

## 📊 Logging and Tracing

### Automatic LogID Management

Each test case automatically generates a unique LogID for end-to-end tracing:

```python
from core.logger import Log

def test_example(self):
    Log.start_test("test_example")
    
    # LogID is automatically generated and managed
    current_logid = Log.get_logid()
    
    # All logs include the LogID for tracing
    Log.info("Test step executed")
    Log.api_call("GET", "/api/users", 200, 0.5)
    
    Log.end_test("test_example", "PASSED")
```

### File Logging

Support for local file logging alongside Allure reports:

```yaml
# config/common.yaml
logging:
  enable_file_logging: true
  file:
    directory: "logs"
    filename_format: "pte_{datetime}_{testcase}_{logid}_{level}.log"
    level: "INFO"
```

## 🗄️ Database Integration

Complete database testing support with connection pooling and transaction management:

```python
from core.db_checker import BaseDBChecker, DatabaseConfig

class TestDatabaseOperations:
    def setup_method(self):
        db_config = DatabaseConfig(get_database_config())
        self.db_checker = BaseDBChecker(db_config)
    
    def test_database_operations(self):
        # Database assertions
        self.db_checker.assert_table_exists('users')
        self.db_checker.assert_column_exists('users', 'id')
        
        # Execute queries
        result = self.db_checker.execute_query("SELECT COUNT(*) FROM users")
        Checker.assert_int_data(result[0][0], "user_count")
```

## ⚡ Parallel Testing

Built-in support for parallel test execution with pytest-xdist:

```bash
# Auto-detect CPU cores
pte all --parallel

# Specify worker count
pte all --parallel=4

# Disable parallel execution
pte all --no-parallel
```

```python
import pytest

@pytest.mark.parallel
def test_api_call_safe():
    """API call can be safely executed in parallel"""
    Log.info("Running API call test")
    assert True

@pytest.mark.no_parallel
def test_database_operation():
    """Database operation should not run in parallel"""
    Log.info("Running database operation test")
    assert True
```

## 📈 Reporting and Coverage

### Allure Reports

```bash
# Generate Allure report
./generate_report.sh --generate

# Open Allure report
./generate_report.sh --open

# Run tests and generate report
./generate_report.sh --run-and-report
```

### Code Coverage

```bash
# Run tests and collect coverage
./manage_coverage.sh --run-tests all

# Generate coverage report
./manage_coverage.sh --generate-report main

# Open coverage report
./manage_coverage.sh --open main
```

## 🛠️ Command Line Interface

The framework provides a convenient `pte` command for test execution:

```bash
# Basic test execution
pte all                    # Run all tests
pte demo                   # Run demo tests
pte business               # Run business tests

# Parallel execution
pte all --parallel         # Auto-detect CPU cores
pte all --parallel=4       # Use 4 workers

# Specific test execution
pte run test/path/to/test.py
pte run test/path/to/test.py::TestClass::test_method

# With pytest options
pte run test/path -v -k "api"
pte run test/path -m "not slow"

# Database and environment tests
pte db-test                # Test database connection
pte mysql-verify           # Verify MySQL environment
```

## 🔍 Data Validation

Universal data validator for consistent assertions:

```python
from core.checker import Checker

# Basic assertions
Checker.assert_not_none(data["field"], "field")
Checker.assert_not_empty(data["list"], "list")

# Type assertions
Checker.assert_int_data(data["id"], "id")
Checker.assert_str_data(data["name"], "name")
Checker.assert_dict_data(data["config"], "config")

# Value assertions
Checker.assert_in_range(data["age"], 0, 100, "age")
Checker.assert_field_value(data, "status", "success")
```

## 🎯 Test Classification

The framework separates tests into two categories:

### Framework Demo Tests
Demonstrate framework functionality and help developers learn:
- Framework structure demonstration
- Configuration management demonstration
- Database features demonstration

### Business Case Tests
Actual business scenario tests that validate business logic:
- User management workflows
- API integration tests
- Database operation tests

## Logging System

### Static Log Usage

The PTE Framework provides a simplified static `Log` class for easy logging across all layers:

```python
from core.logger import Log

# Basic logging
Log.info("Information message")
Log.warning("Warning message")
Log.error("Error message")
Log.debug("Debug message")

# Test-specific logging
Log.start_test("test_name")
Log.end_test("test_name", "PASSED")
Log.end_test("test_name", "FAILED")

# API logging
Log.api_call(
    method="POST",
    url="/api/users",
    status_code=201,
    response_time=0.5,
    request_data=data,
    response_data=response
)

# Data validation logging
Log.data_validation("field_name", expected_value, actual_value, True)
Log.assertion("assertion_description", expected, actual, expected)

# Print replacement
Log.raw("Raw message without LogID prefix")
Log.print("Print-like message")  # Alias for Log.raw()
```

### Automatic LogID Management

Each test case automatically generates a unique LogID for end-to-end tracing:

```python
def test_example(self):
    Log.start_test("test_example")
    
    # LogID is automatically generated and managed
    current_logid = Log.get_logid()
    print(f"Current LogID: {current_logid}")
    
    # All logs include the LogID for tracing
    Log.info("Test step executed")
    
    Log.end_test("test_example", "PASSED")
```

### File Logging

The framework supports local file logging alongside Allure reports:

```yaml
# config/common.yaml
logging:
  enable_file_logging: true
  
  file:
    directory: "logs"
    filename_format: "pte_{datetime}_{testcase}_{logid}_{level}.log"
    level: "INFO"
    format: "[{timestamp}] [{level}] [{logid}] [{caller}] {message}"
    rotate_by_date: true
    separate_by_level: false
    retention_days: 30
    max_size_mb: 100
    enable_compression: false
```

## Testing Framework

### Test Structure

```python
import pytest
from core.logger import Log
from core.checker import Checker

class TestYourFeature:
    def setup_method(self):
        # Setup code runs before each test
        pass
    
    def test_example(self):
        """Test example with proper structure"""
        Log.start_test("test_example")
        
        try:
            # Test logic here
            result = {"status": "success"}
            
            # Assertions
            Checker.assert_dict_data(result, "result")
            Checker.assert_field_value(result, "status", "success")
            
            Log.end_test("test_example", "PASSED")
        except Exception as e:
            Log.error(f"Test failed: {str(e)}")
            Log.end_test("test_example", "FAILED")
            raise
```

### Data Validation

Use the universal data validator for consistent assertions:

```python
from core.checker import Checker

# Basic assertions
Checker.assert_not_none(data["field"], "field")
Checker.assert_not_empty(data["list"], "list")

# Type assertions
Checker.assert_int_data(data["id"], "id")
Checker.assert_str_data(data["name"], "name")
Checker.assert_bool_data(data["active"], "active")
Checker.assert_float_data(data["price"], "price")
Checker.assert_list_data(data["items"], "items")
Checker.assert_dict_data(data["config"], "config")

# Value assertions
Checker.assert_in_range(data["age"], 0, 100, "age")
Checker.assert_string_length(data["name"], 1, 50, "name")
Checker.assert_field_value(data, "status", "success")
```

### API Testing

```python
from api.client import APIClient
from core.logger import Log

class TestAPIEndpoints:
    def setup_method(self):
        self.api_client = APIClient()
    
    def test_user_creation(self):
        """Test user creation API"""
        Log.start_test("test_user_creation")
        
        # Test data
        user_data = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        
        # Make API call
        response = self.api_client.post("/api/users", json=user_data)
        
        # Assertions
        assert response.status_code == 201
        result = response.json()
        Checker.assert_dict_data(result, "response")
        Checker.assert_field_value(result, "name", "John Doe")
        
        Log.end_test("test_user_creation", "PASSED")
```

### Database Testing

```python
from core.db_checker import BaseDBChecker, DatabaseConfig
from core.logger import Log

class TestDatabaseOperations:
    def setup_method(self):
        from config.settings import get_database_config
        db_config = DatabaseConfig(get_database_config())
        self.db_checker = BaseDBChecker(db_config)
    
    def test_user_operations(self):
        """Test user database operations"""
        Log.start_test("test_user_operations")
        
        # Database assertions
        self.db_checker.assert_table_exists('users')
        self.db_checker.assert_column_exists('users', 'id')
        
        # Execute queries
        result = self.db_checker.execute_query("SELECT COUNT(*) FROM users")
        Checker.assert_int_data(result[0][0], "user_count")
        
        Log.end_test("test_user_operations", "PASSED")
```

### Business Operations

```python
from biz.department.user.operations import UserOperations
from core.logger import Log

class TestUserBusinessLogic:
    def setup_method(self):
        self.user_ops = UserOperations()
    
    def test_user_workflow(self):
        """Test complete user workflow"""
        Log.start_test("test_user_workflow")
        
        # Create user
        user_data = {"name": "Jane Doe", "email": "jane@example.com"}
        new_user = self.user_ops.create_user(user_data)
        Checker.assert_dict_data(new_user, "new_user")
        
        # Get user
        user_id = new_user["id"]
        user = self.user_ops.get_user_by_id(user_id)
        Checker.assert_field_value(user, "name", "Jane Doe")
        
        # Update user
        update_data = {"name": "Jane Smith"}
        updated_user = self.user_ops.update_user(user_id, update_data)
        Checker.assert_field_value(updated_user, "name", "Jane Smith")
        
        # Delete user
        success = self.user_ops.delete_user(user_id)
        assert success is True
        
        Log.end_test("test_user_workflow", "PASSED")
```

## Configuration Management

### Environment Configuration

The framework uses YAML files for configuration management:

```yaml
# config/env.yaml - Environment management
idc: "local_test"  # Current IDC to test
env: "local"       # Current environment tag to test
```

```yaml
# config/local_test.yaml - Local environment
host: "http://localhost:5001"
timeout: 30
retry_count: 3
default_headers:
  Content-Type: "application/json"
  Accept: "application/json"
  User-Agent: "PTE/1.0"

database:
  mysql:
    host: "127.0.0.1"
    port: 3306
    username: "root"
    password: "password"
    database: "pte"
    charset: "utf8mb4"
    pool_size: 5
    max_overflow: 10
    pool_timeout: 30
    pool_recycle: 3600
```

### Configuration Management Commands

```bash
# List all available IDCs
python config_manager.py list-idcs

# Show specific IDC configuration
python config_manager.py show-idc local_test

# Show current configuration
python config_manager.py current

# Validate configuration files
python config_manager.py validate
```

### Environment Switching

```bash
# Switch environment via environment variables
export TEST_IDC=local_test
export TEST_ENV=local

# Switch to different environments
export TEST_IDC=aws_offline
export TEST_ENV=dev_ci

export TEST_IDC=gcp_online
export TEST_ENV=prod
```

## Test Execution

### Command Line Interface

```bash
# Basic test execution
pte all                    # Run all tests
pte demo                   # Run demo tests
pte business               # Run business tests

# Parallel execution
pte all --parallel         # Auto-detect CPU cores
pte all --parallel=4       # Use 4 workers
pte all --no-parallel      # Disable parallel execution

# Specific test execution
pte run test/path/to/test.py
pte run test/path/to/test.py::TestClass::test_method
pte run "test/department/user/*.py"

# With pytest options
pte run test/path -v -k "api"
pte run test/path -m "not slow"
pte run test/path --tb=short --maxfail=1
```

### Test Markers

```python
import pytest

@pytest.mark.parallel
def test_api_call_safe():
    """API call can be safely executed in parallel"""
    Log.info("Running API call test")
    assert True

@pytest.mark.no_parallel
def test_database_operation():
    """Database operation should not run in parallel"""
    Log.info("Running database operation test")
    assert True
```

### Script Execution

```bash
# Using run_tests.sh script
./run_tests.sh --demo       # Run demo tests
./run_tests.sh --business   # Run business tests
./run_tests.sh --all        # Run all tests
./run_tests.sh --db-test    # Test database connection

# Using Python scripts
python scripts/run_tests_by_category.py --demo
python scripts/run_tests_by_category.py --business
python scripts/run_tests_by_category.py --all
```

## Reporting and Coverage

### Allure Reports

```bash
# Install Allure command line tool
./generate_report.sh --install

# Generate Allure report
./generate_report.sh --generate

# Open Allure report
./generate_report.sh --open

# Start Allure report server
./generate_report.sh --serve

# Run tests and generate report
./generate_report.sh --run-and-report

# Clean old reports
./generate_report.sh --clean
```

### Code Coverage

```bash
# Run tests and collect coverage
./manage_coverage.sh --run-tests demo
./manage_coverage.sh --run-tests business
./manage_coverage.sh --run-tests all

# Generate coverage report
./manage_coverage.sh --generate-report main    # Main project coverage
./manage_coverage.sh --generate-report flask   # Flask application coverage

# Show coverage summary
./manage_coverage.sh --show-summary main
./manage_coverage.sh --show-summary flask

# Open coverage report
./manage_coverage.sh --open main
./manage_coverage.sh --open flask

# Clean coverage data
./manage_coverage.sh --clean all
```

## Best Practices

### Test Structure

1. **Use proper test structure**:
   ```python
   def test_example(self):
       Log.start_test("test_example")
       try:
           # Test logic
           Log.end_test("test_example", "PASSED")
       except Exception as e:
           Log.error(f"Test failed: {e}")
           Log.end_test("test_example", "FAILED")
           raise
   ```

2. **Use data validators**:
   ```python
   # Instead of assert data["field"] is not None
   Checker.assert_not_none(data["field"], "field")
   
   # Instead of assert isinstance(data["id"], int)
   Checker.assert_int_data(data["id"], "id")
   ```

3. **Use business operations**:
   ```python
   # Instead of direct API calls
   user = self.user_ops.get_user_by_id(user_id)
   ```

### Logging Best Practices

1. **Use static Log class**:
   ```python
   # Good
   Log.info("Message")
   
   # Avoid
   self.logger.info("Message")
   ```

2. **Include context in logs**:
   ```python
   Log.info("User operation", {"user_id": 123, "action": "create"})
   Log.error("Database error", {"error": "Connection failed", "retry_count": 3})
   ```

3. **Use appropriate log levels**:
   - `Log.debug()`: Detailed debugging information
   - `Log.info()`: General information
   - `Log.warning()`: Warning messages
   - `Log.error()`: Error messages

### Configuration Best Practices

1. **Use environment variables for switching**:
   ```bash
   export TEST_IDC=local_test
   export TEST_ENV=local
   ```

2. **Validate configurations**:
   ```bash
   python config_manager.py validate
   ```

3. **Keep sensitive data secure**:
   - Use environment variables for passwords
   - Don't commit sensitive data to version control

### Performance Best Practices

1. **Use parallel execution for independent tests**:
   ```bash
   pte all --parallel
   ```

2. **Mark tests appropriately**:
   ```python
   @pytest.mark.parallel  # For independent tests
   @pytest.mark.no_parallel  # For tests that can't run in parallel
   ```

3. **Optimize database operations**:
   - Use connection pooling
   - Clean up test data
   - Use transactions where appropriate

## Troubleshooting

### Common Issues

1. **LogID not generated**:
   - Ensure you're using the static `Log` class
   - Check that pytest fixtures are loaded
   - Verify `core/__init__.py` imports fixtures

2. **Database connection failed**:
   - Check MySQL container status: `docker ps | grep mysql`
   - Verify configuration: `python config_manager.py show-idc local_test`
   - Test connection: `pte db-test`

3. **Configuration validation failed**:
   - Check YAML syntax: `python config_manager.py validate`
   - Verify file paths and permissions
   - Check environment variables

4. **Tests not running in parallel**:
   - Check pytest-xdist installation: `pip install pytest-xdist`
   - Verify test markers: `@pytest.mark.parallel`
   - Check for shared resources

### Getting Help

```bash
# Show command help
pte help
./run_tests.sh --help
./generate_report.sh --help
./manage_coverage.sh --help

# Check framework status
python config_manager.py current
pte db-test
pte mysql-verify
```

## Advanced Features

### Custom Checkers

Create custom data validators for your business logic:

```python
from core.checker import Checker

class UserChecker(Checker):
    @staticmethod
    def assert_valid_email(email, field_name="email"):
        """Assert email format is valid"""
        if not email or '@' not in email:
            raise AssertionError(f"{field_name} must be a valid email address")
    
    @staticmethod
    def assert_user_status(status, field_name="status"):
        """Assert user status is valid"""
        valid_statuses = ["active", "inactive", "pending"]
        if status not in valid_statuses:
            raise AssertionError(f"{field_name} must be one of {valid_statuses}")
```

### Custom Operations

Extend business operations for your specific needs:

```python
from biz.department.user.operations import UserOperations

class ExtendedUserOperations(UserOperations):
    def bulk_create_users(self, users_data):
        """Bulk create multiple users"""
        results = []
        for user_data in users_data:
            result = self.create_user(user_data)
            results.append(result)
        return results
    
    def search_users_by_criteria(self, criteria):
        """Search users by custom criteria"""
        # Implementation here
        pass
```

### Custom Fixtures

Create reusable test fixtures:

```python
import pytest
from core.logger import Log

@pytest.fixture
def test_user_data():
    """Provide test user data"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "status": "active"
    }

@pytest.fixture
def api_client():
    """Provide configured API client"""
    from api.client import APIClient
    return APIClient()

@pytest.fixture
def db_checker():
    """Provide database checker"""
    from core.db_checker import BaseDBChecker, DatabaseConfig
    from config.settings import get_database_config
    db_config = DatabaseConfig(get_database_config())
    return BaseDBChecker(db_config)
```
