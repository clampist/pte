# PTE Framework Quick Start Guide

## Overview

PTE (Pytest Testing Environment) is a universal backend testing framework that supports testing Java, Go, Python and other Web systems. This guide will help you get started quickly.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd pte

# Set up Python environment
pyenv activate pte
pip install -r requirements.txt

# Install PTE command (optional)
./install_pte.sh --install
source ~/.zshrc

# Set up database environment
docker run --name mysql57 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql:5.7
```

### Basic Usage

```bash
# Run all tests
pte all

# Run tests in parallel
pte all --parallel

# Run specific test categories
pte demo                    # Framework demo tests
pte business               # Business case tests

# Run specific test paths
pte run test/path/to/test.py
pte run test/path/to/test.py::TestClass::test_method
```

### Writing Your First Test

```python
import pytest
from core.logger import Log
from core.checker import Checker

class TestExample:
    def test_basic_functionality(self):
        """Basic test example"""
        Log.start_test("test_basic_functionality")
        
        # Your test logic here
        result = {"status": "success"}
        
        # Assertions using universal data validator
        Checker.assert_dict_data(result, "result")
        Checker.assert_field_value(result, "status", "success")
        
        Log.end_test("test_basic_functionality", "PASSED")
```

## Prerequisites

- Python 3.6+
- Docker (for MySQL environment)
- Git

## Installation

### 1. Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd pte

# Or download and extract if you have the source code
```

### 2. Set Up Python Environment

```bash
# Create and activate virtual environment
pyenv activate pte

# Install dependencies
pip install -r requirements.txt
```

### 3. Install PTE Command (Optional)

```bash
# Install pte command to system PATH
./install_pte.sh --install

# Reload shell configuration
source ~/.zshrc  # or ~/.bashrc, ~/.bash_profile

# Verify installation
pte help
```

### 4. Set Up Database Environment

```bash
# Start MySQL container
docker run --name mysql57 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql:5.7

# Verify MySQL environment
python scripts/test_mysql_docker.py
```

## Basic Configuration

### 1. Environment Configuration

The framework uses YAML configuration files for different environments:

```yaml
# config/env.yaml
idc: "local_test"  # Current IDC to test
env: "local"       # Current environment tag to test
```

```yaml
# config/local_test.yaml
host: "http://localhost:5001"
timeout: 30
retry_count: 3
default_headers:
  Content-Type: "application/json"
  Accept: "application/json"
  User-Agent: "Universal-Test-Framework/1.0"

database:
  mysql:
    host: "127.0.0.1"
    port: 3306
    username: "root"
    password: "password"
    database: "pte"
    charset: "utf8mb4"
```

### 2. Verify Configuration

```bash
# Validate configuration files
python config_manager.py validate

# View current configuration
python config_manager.py show-idc local_test
```

## Running Your First Tests

### 1. Framework Demo Tests

```bash
# Run framework demonstration tests
pte demo

# Or using script
./run_tests.sh --demo
```

### 2. Business Case Tests

```bash
# Run business scenario tests
pte business

# Or using script
./run_tests.sh --business
```

### 3. All Tests

```bash
# Run all tests
pte all

# Run tests in parallel
pte all --parallel

# Or using script
./run_tests.sh --all
```

### 4. Database Tests

```bash
# Test database connection
pte db-test

# Verify MySQL environment
pte mysql-verify
```

## Writing Your First Test

### 1. Basic Test Structure

```python
# test/your_module/test_basic.py
import pytest
from core.logger import Log
from core.checker import Checker

class TestBasicFunctionality:
    def test_simple_assertion(self):
        """Basic test example"""
        Log.start_test("test_simple_assertion")
        
        # Your test logic here
        result = {"status": "success", "data": "test"}
        
        # Assertions
        Checker.assert_dict_data(result, "result")
        Checker.assert_field_value(result, "status", "success")
        
        Log.end_test("test_simple_assertion", "PASSED")
```

### 2. API Testing

```python
# test/your_module/test_api.py
import pytest
from core.logger import Log
from api.client import APIClient

class TestAPIEndpoints:
    def setup_method(self):
        self.api_client = APIClient()
    
    def test_get_users(self):
        """Test GET /api/users endpoint"""
        Log.start_test("test_get_users")
        
        # Make API call
        response = self.api_client.get("/api/users")
        
        # Assertions
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        
        Log.end_test("test_get_users", "PASSED")
```

### 3. Database Testing

```python
# test/your_module/test_database.py
import pytest
from core.logger import Log
from core.db_checker import BaseDBChecker, DatabaseConfig

class TestDatabaseOperations:
    def setup_method(self):
        from config.settings import get_database_config
        db_config = DatabaseConfig(get_database_config())
        self.db_checker = BaseDBChecker(db_config)
    
    def test_user_table_exists(self):
        """Test database table existence"""
        Log.start_test("test_user_table_exists")
        
        # Database assertions
        self.db_checker.assert_table_exists('users')
        self.db_checker.assert_column_exists('users', 'id')
        
        Log.end_test("test_user_table_exists", "PASSED")
```

## Test Reports and Coverage

### 1. Allure Reports

```bash
# Install Allure command line tool
./generate_report.sh --install

# Generate Allure report
./generate_report.sh --generate

# Open Allure report
./generate_report.sh --open
```

### 2. Code Coverage

```bash
# Run tests and collect coverage
./manage_coverage.sh --run-tests all

# Generate coverage report
./manage_coverage.sh --generate-report main

# Open coverage report
./manage_coverage.sh --open main
```

## Common Commands

### Test Execution

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
```

### Configuration Management

```bash
# List all IDCs
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

# Or use scripts
./run_tests.sh --demo
./run_tests.sh --business
```

## Troubleshooting

### Common Issues

1. **"command not found: pte"**
   ```bash
   # Install pte command
   ./install_pte.sh --install
   source ~/.zshrc
   ```

2. **Database connection failed**
   ```bash
   # Check MySQL container
   docker ps | grep mysql
   
   # Restart MySQL container
   docker restart mysql57
   ```

3. **Configuration validation failed**
   ```bash
   # Check configuration files
   python config_manager.py validate
   python config_manager.py show-idc local_test
   ```

### Getting Help

```bash
# Show pte command help
pte help

# Show script help
./run_tests.sh --help
./generate_report.sh --help
./manage_coverage.sh --help
```

## Next Steps

1. **Explore Framework Features**: Run demo tests to understand framework capabilities
2. **Read Documentation**: Check other documentation files for detailed information
3. **Write Your Tests**: Start writing tests for your specific use cases
4. **Customize Configuration**: Modify configuration files for your environment
5. **Extend Framework**: Add custom checkers, operations, and fixtures as needed

## Support

- Check the [User Guide](02_user_guide.md) for detailed usage information
- Review the [Architecture Guide](03_architecture_guide.md) for design principles
- Refer to the [Installation Guide](04_installation_guide.md) for setup details
