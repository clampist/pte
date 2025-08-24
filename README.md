# PTE - Universal Backend Testing Framework

A Pytest-based universal backend testing framework that supports testing Java, Go, Python and other Web systems, featuring layered architecture design, flexible configuration management, and database integration.

## 🎯 Project Overview

PTE (Pytest Testing Environment) is a modern backend testing framework with the following features:

- **Universality**: Supports testing backend systems with different technology stacks
- **Layered Architecture**: Clear layered design with separated responsibilities
- **Configuration Management**: Flexible YAML configuration management supporting multiple environments
- **Database Integration**: Complete database testing support
- **Modularity**: Organized by business modules, easy to extend
- **Test Classification**: Separation of framework Demo tests and business Case tests

## 🏗️ Project Architecture

```
pte/
├── config/                          # Global configuration layer
│   ├── env.yaml                     # Environment management configuration
│   ├── local_test.yaml             # Local testing configuration
│   ├── aws_offline.yaml            # AWS offline configuration
│   ├── gcp_offline.yaml            # GCP offline configuration
│   ├── aws_online.yaml             # AWS online configuration
│   ├── gcp_online.yaml             # GCP online configuration
│   └── settings.py                  # Configuration management class
├── core/                            # Core framework layer
│   ├── checker.py                   # Universal data validator
│   ├── fixtures.py                  # Universal test fixtures
│   ├── markers.py                   # Test marker definitions
│   └── db_checker.py               # Database checker base class
├── api/                             # API interface layer
│   ├── client.py                    # HTTP client wrapper
│   └── config.py                    # API configuration constants
├── app/                             # Application configuration layer
│   └── department/user/config.py    # Business module configuration
├── biz/                             # Business logic layer
│   └── department/user/             # User business module
│       ├── operations.py            # Business operation wrapper
│       ├── checker.py               # Business data validator
│       ├── fixtures.py              # Business test fixtures
│       ├── db_checker.py           # User database checker
│       └── db_operations.py        # User database operations
├── data/                            # Test data layer
│   └── department/user/test_data.py # Test data definitions
├── test/                            # Test case layer
│   └── department/user/             # User test module
│       ├── README.md               # Test classification description
│       ├── demo_framework_structure.py # Framework structure demonstration
│       ├── demo_config_management.py   # Configuration management demonstration
│       ├── demo_database_features.py   # Database features demonstration
│       └── business_user_management.py # User management business scenarios
├── scripts/                         # Script tools
│   ├── run_tests_by_category.py    # Run tests by category
│   ├── test_db_connection.py       # Database connection test
│   ├── test_mysql_docker.py        # Docker MySQL verification
│   └── init_database.py            # Database initialization
├── docs/                            # Documentation
│   ├── database_integration.md     # Database integration documentation
│   └── local_mysql_verification.md # Local MySQL verification documentation
├── flask_app/                       # Flask application example
│   └── app.py                       # Example backend service
├── config_manager.py                # Configuration management tool
├── run_tests.sh                     # Test execution script
├── requirements.txt                 # Project dependencies
└── pytest.ini                      # pytest configuration
```

## 🎯 Design Principles

### 1. Layered Architecture
- **core layer**: Universal framework functionality, independent of specific business
- **api layer**: HTTP client wrapper, supporting different backend systems
- **app layer**: Business configuration management, inheriting global configuration
- **biz layer**: Business logic wrapper, inheriting core layer functionality
- **data layer**: Test data management
- **test layer**: Test case writing, using biz layer functionality

### 2. Configuration Management
- **YAML Configuration Files**: Using multiple YAML files to manage different IDC configurations
- **Environment Isolation**: Supporting multiple environments: local, dev, staging, prod
- **IDC Isolation**: Supporting different IDC configurations like AWS, GCP
- **Dynamic Switching**: Dynamically switching environments and IDCs through environment variables

### 3. Test Classification
- **Framework Demo Tests**: Demonstrating framework functionality, helping developers learn
- **Business Case Tests**: Actual business scenario tests, validating business logic

## 📋 Configuration Management

### Environment Configuration Files

#### `config/env.yaml` - Environment Management Configuration
```yaml
# Environment configuration file - defines the current IDC and environment tag to test
idc: "local_test"  # Current IDC to test
env: "local"       # Current environment tag to test
```

#### `config/local_test.yaml` - Local Testing Configuration
```yaml
# Local testing environment configuration file
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
    port: 8306
    username: "root"
    password: "patest"
    database: "pte"
    charset: "utf8mb4"
    pool_size: 5
    max_overflow: 10
    pool_timeout: 30
    pool_recycle: 3600
    description: "Local testing MySQL database"
```

### Configuration Management Tool

Use the `config_manager.py` tool to manage configurations:

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

#### 1. Environment Variable Switching
```bash
# Switch to local testing environment
export TEST_IDC=local_test
export TEST_ENV=local

# Switch to AWS offline environment
export TEST_IDC=aws_offline
export TEST_ENV=dev_ci
```

#### 2. Script Switching
```bash
# Use test execution script
./run_tests.sh --demo        # Run framework Demo tests
./run_tests.sh --business    # Run business Case tests
./run_tests.sh --all         # Run all tests
./run_tests.sh --db-test     # Test database connection
./run_tests.sh --mysql-verify # Verify Docker MySQL environment
```

## 🔧 Core Components

### 1. Data Validator (core/checker.py)

#### Universal Data Validation
```python
from core.checker import DataChecker

# Basic assertions
DataChecker.assert_not_none(data["field"], "field")
DataChecker.assert_not_empty(data["list"], "list")

# Type assertions
DataChecker.assert_int_data(data["id"], "id")
DataChecker.assert_str_data(data["name"], "name")
DataChecker.assert_bool_data(data["active"], "active")
DataChecker.assert_float_data(data["price"], "price")
DataChecker.assert_list_data(data["items"], "items")
DataChecker.assert_dict_data(data["config"], "config")

# Value assertions
DataChecker.assert_in_range(data["age"], 0, 100, "age")
DataChecker.assert_string_length(data["name"], 1, 50, "name")
```

### 2. Database Checker (core/db_checker.py)

#### Database Operations
```python
from core.db_checker import BaseDBChecker, DatabaseConfig

# Create database configuration
db_config = DatabaseConfig(mysql_config)
db_checker = BaseDBChecker(db_config)

# Basic database operations
result = db_checker.execute_query("SELECT * FROM users")
affected = db_checker.execute_update("UPDATE users SET name='test' WHERE id=1")

# Database assertions
db_checker.assert_table_exists('users')
db_checker.assert_column_exists('users', 'name')
db_checker.assert_record_exists('users', 'id = 1')
db_checker.assert_field_value('users', 'name', 'test', 'id = 1')
```

### 3. Business Operation Wrapper (biz/department/user/operations.py)

```python
from biz.department.user.operations import UserOperations

# Use default environment configuration
user_ops = UserOperations()

# Business operations
result = user_ops.get_all_users()
user = user_ops.get_user_by_id(1)
new_user = user_ops.create_user({"name": "Zhang San", "email": "zhangsan@example.com"})
updated_user = user_ops.update_user(1, {"name": "Li Si"})
success = user_ops.delete_user(1)
```

### 4. Database Operations (biz/department/user/db_operations.py)

```python
from biz.department.user.db_operations import UserDBOperations

# Database operations
db_ops = UserDBOperations()

# User database operations
user_id = db_ops.create_test_user(user_data)
affected = db_ops.update_test_user(user_id, update_data)
success = db_ops.delete_test_user(user_id)

# Database assertions
db_ops.assert_user_created(user_id, user_data)
db_ops.assert_user_updated(user_id, update_data)
db_ops.assert_user_deleted(user_id)
```

## 🧪 Test Case Writing

### 1. Framework Demo Tests

#### Framework Structure Demonstration
```python
# test/department/user/demo_framework_structure.py
class TestFrameworkStructureDemo:
    def test_framework_layers_demo(self):
        """Demonstrate PTE framework layered structure"""
        # Demonstrate core layer, api layer, biz layer, data layer, etc.
```

#### Configuration Management Demonstration
```python
# test/department/user/demo_config_management.py
class TestConfigurationManagementDemo:
    def test_yaml_config_loading_demo(self):
        """Demonstrate YAML configuration loading functionality"""
        # Demonstrate configuration loading, environment switching, etc.
```

#### Database Features Demonstration
```python
# test/department/user/demo_database_features.py
class TestDatabaseFeaturesDemo:
    def test_database_connection_demo(self):
        """Demonstrate database connection functionality"""
        # Demonstrate database connection, SQL building, table operations, etc.
```

### 2. Business Case Tests

#### User Management Business Scenarios
```python
# test/department/user/business_user_management.py
class TestUserManagementBusinessCases:
    def test_user_registration_workflow(self):
        """Complete user registration workflow"""
        # Complete user registration business workflow test
```

## 📦 Dependency Management

### Main Project Dependencies (requirements.txt)
- **pytest**: Testing framework
- **requests**: HTTP client
- **PyYAML**: YAML configuration file processing
- **pymysql**: MySQL database connection
- **sqlalchemy**: SQL toolkit and ORM
- **allure-pytest**: Allure test reports
- **pytest-cov**: Test coverage collection

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Activate Python environment
pyenv activate pte

# Install main project dependencies
pip install -r requirements.txt
```

### 1.5. Install pte Command (Optional)
```bash
# Install pte command to system PATH for global access
./install_pte.sh --install
source ~/.zshrc  # or restart terminal

# Verify installation
pte help

# Check installation status
./install_pte.sh --status
```

### 2. Set Up Docker MySQL Environment
```bash
# Start MySQL container
docker run --name mysql57 -p 8306:3306 -e MYSQL_ROOT_PASSWORD=patest -d mysql:5.7

# Verify MySQL environment
python scripts/test_mysql_docker.py
```

### 3. Verify Configuration
```bash
# Validate configuration files
python config_manager.py validate

# View current configuration
python config_manager.py show-idc local_test
```

### 4. Run Tests
```bash
# Option 1: Using pte command (after installation)
pte demo                    # Run framework Demo tests
pte business                # Run business Case tests
pte all                     # Run all tests
pte all --parallel          # Run all tests in parallel
pte db-test                 # Test database connection

# Option 2: Using run_tests.sh script
./run_tests.sh --demo       # Run framework Demo tests
./run_tests.sh --business   # Run business Case tests
./run_tests.sh --all        # Run all tests
./run_tests.sh --db-test    # Test database connection

# Run real API tests (requires target application to be started first)
# Please refer to target application documentation: $PTE_TARGET_ROOT/README.md
```

### 5. Use Python Scripts to Run
```bash
# Run tests by category
python scripts/run_tests_by_category.py --demo
python scripts/run_tests_by_category.py --business
python scripts/run_tests_by_category.py --all

# View available tests
python scripts/run_tests_by_category.py --list
```

### 6. Allure Test Reports
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

### 7. Code Coverage
```bash
# Check server language configuration
./manage_coverage.sh --check-language

# Run tests and collect coverage
./manage_coverage.sh --run-tests demo
./manage_coverage.sh --run-tests business
./manage_coverage.sh --run-tests all

# Collect Flask application coverage
./manage_coverage.sh --collect-flask

# Generate coverage report
./manage_coverage.sh --generate-report main    # Main project coverage
./manage_coverage.sh --generate-report flask   # Flask application coverage

# Show coverage summary
./manage_coverage.sh --show-summary main       # Main project summary
./manage_coverage.sh --show-summary flask      # Flask application summary

# Open coverage report
./manage_coverage.sh --open main               # Main project report
./manage_coverage.sh --open flask              # Flask application report

# Clean coverage data
./manage_coverage.sh --clean all               # Clean all data
./manage_coverage.sh --clean main              # Clean main project data
./manage_coverage.sh --clean flask             # Clean Flask application data
```

## 📊 Test Results

### Framework Demo Tests
- ✅ Framework structure demonstration: 10 tests passed
- ✅ Configuration management demonstration: 9 tests passed
- ✅ Database features demonstration: 10 tests passed

### Business Case Tests
- ✅ User management business scenarios: 8 tests passed

### Database Integration
- ✅ Docker MySQL environment verification: Passed
- ✅ Database connection test: Passed
- ✅ SQL building test: Passed
- ✅ Database operation test: Passed

## 🎯 Advantage Features

1. **Universality**: Supports testing backend systems with different technology stacks
2. **Layered Architecture**: Clear layered design with separated responsibilities
3. **Configuration Management**: Flexible YAML configuration management supporting multiple environments and IDCs
4. **Database Integration**: Complete database testing support
5. **Test Classification**: Separation of framework Demo tests and business Case tests
6. **Modularity**: Organized by business modules, easy to extend
7. **Tool Support**: Rich script tools and configuration management tools
8. **Command Line Interface**: Easy-to-use `pte` command for test execution
9. **Complete Documentation**: Detailed documentation and usage guides

## 💻 Command Line Usage

### Installing pte Command

The PTE framework provides a convenient `pte` command for running tests. You can install it globally:

```bash
# Install pte command to system PATH
./install_pte.sh --install
source ~/.zshrc  # or restart terminal

# Verify installation
pte help
```

### Basic Usage

```bash
# Run all tests
pte all

# Run tests in parallel
pte all --parallel

# Run specific test categories
pte demo                    # Framework demo tests
pte business                # Business case tests

# Run specific test paths
pte run test/department/user
pte run test/department/user/demo_*.py

# Run with pytest options
pte run test/department/user -v -k "api"
pte run test/department/user -m "not slow"

# Database and environment tests
pte db-test                 # Test database connection
pte mysql-verify            # Verify MySQL environment
```

### Advanced Usage

```bash
# Parallel testing with specific worker count
pte all --parallel=4

# Run specific test method
pte run test/department/user/demo_framework_structure.py::TestFrameworkStructureDemo::test_api_client_demo

# Run with custom pytest options
pte run test/department/user -v --tb=short --maxfail=1
```

For more detailed information, see [Command Line Usage Guide](docs/command_line_usage_guide.md).

## 🔄 Version History

- **v3.0**: Introduced database integration, restructured test classification
- **v2.0**: Introduced YAML configuration files, restructured configuration management
- **v1.0**: Basic framework architecture, supporting multi-environment configuration

## 📚 Related Documentation

- [Test Classification Description](test/department/user/README.md)
- [Database Integration Documentation](docs/database_integration.md)
- [Local MySQL Verification Documentation](docs/local_mysql_verification.md)
- [Command Line Usage Guide](docs/command_line_usage_guide.md)
- [Target Application Documentation]($PTE_TARGET_ROOT/README.md)

## 🤝 Contributing Guidelines

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
