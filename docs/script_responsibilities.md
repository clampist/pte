# PTE Framework Script Responsibilities Description

This document explains the responsibility division of various scripts in the PTE framework, ensuring clear script functionality and single responsibility.

## 📁 Script Classification

### 🧪 Test Execution Scripts

#### `run_tests.sh` - Main Test Runner
**Responsibilities**: Run various tests in the PTE framework
- Run framework Demo tests
- Run business Case tests
- Run real API tests (requires Flask application running)
- Run database connection tests
- Verify Docker MySQL environment

**Does not include**: Flask application startup, shutdown, status management

#### `scripts/run_tests_by_category.py` - Categorized Test Runner
**Responsibilities**: Run pytest tests by category
- Run Demo test files
- Run business test files
- Run all tests and generate reports

### 🔧 Flask Environment Management Scripts

#### `manage_flask_env.sh` - Flask Environment Manager
**Responsibilities**: Manage Flask virtual environment
- Create Flask virtual environment
- Install Flask dependencies
- Check environment status
- Delete virtual environment

#### `scripts/manage_flask_env.py` - Flask Environment Management Python Script
**Responsibilities**: Python interface management for Flask environment
- Check pyenv installation status
- Manage virtual environment lifecycle
- Dependency installation and checking
- Environment information display

### 🗄️ Database Management Scripts

#### `scripts/test_db_connection.py` - Database Connection Test
**Responsibilities**: Test database connection
- Verify MySQL connection
- Test database configuration
- Check table structure

#### `scripts/test_mysql_docker.py` - Docker MySQL Verification
**Responsibilities**: Verify Docker MySQL environment
- Check MySQL container status
- Verify database configuration
- Test database operations

#### `scripts/init_database.py` - Database Initialization
**Responsibilities**: Initialize test database
- Create database and tables
- Insert initial test data
- Verify database structure

### ⚙️ Configuration Management Scripts

#### `config_manager.py` - Configuration Manager
**Responsibilities**: Manage PTE framework configuration
- View environment configuration
- Validate configuration files
- Switch environment settings
- Reload configuration

### 📊 Report Management Scripts

#### `generate_report.sh` - Allure Report Generator
**Responsibilities**: Generate and manage Allure test reports
- Install Allure command line tool
- Generate HTML test reports
- Start report server
- Manage report files

#### `scripts/generate_allure_report.py` - Allure Report Manager
**Responsibilities**: Complete lifecycle management of Allure reports
- Check Allure installation status
- Generate, open, serve reports
- List and manage reports
- Clean old reports

### 📊 Coverage Management Scripts

#### `manage_coverage.sh` - Coverage Management Shell Script
**Responsibilities**: Shell interface for coverage management
- Check server language configuration
- Run tests and collect coverage
- Generate coverage reports
- Manage coverage data

#### `scripts/manage_coverage.py` - Coverage Management Python Script
**Responsibilities**: Complete lifecycle management of coverage
- Check server language support
- Collect target application coverage (external project)
- Run tests and collect coverage
- Generate HTML and XML reports
- Manage coverage data

## 🔄 Script Collaboration Workflow

### Typical Test Workflow

1. **Start Target Application** (optional, for real API testing)
   ```bash
   # Reference target application documentation: $PTE_TARGET_ROOT/README.md
cd $PTE_TARGET_ROOT
   ./start_flask.sh
   ```

2. **Run Tests**
   ```bash
   # Framework Demo tests
   ./run_tests.sh --demo
   
   # Business Case tests
   ./run_tests.sh --business
   
   # Real API tests (requires target application running)
   ./run_tests.sh --real-api
   ```

3. **Generate Test Reports** (optional)
   ```bash
   # Generate Allure report
   ./generate_report.sh --generate
   
   # Open report to view
   ./generate_report.sh --open
   
   # Collect code coverage
   ./manage_coverage.sh --run-tests all
   
   # View coverage report
   ./manage_coverage.sh --open
   ```

4. **Stop Flask Application** (optional)
   ```bash
   ./stop_flask.sh
   ```

### Database Test Workflow

1. **Verify MySQL Environment**
   ```bash
   ./run_tests.sh --mysql-verify
   ```

2. **Test Database Connection**
   ```bash
   ./run_tests.sh --db-test
   ```

3. **Initialize Database** (if needed)
   ```bash
   python scripts/init_database.py
   ```

## 📋 Script Usage Recommendations

### Development Phase
- Use `./run_tests.sh --demo` to verify framework functionality
- Use `./run_tests.sh --business` to test business logic
- Use `./start_flask.sh` and `./run_tests.sh --real-api` for integration testing

### Debugging Phase
- Use `python scripts/manage_flask_app.py status` to check Flask status
- Use `./test_flask_api.sh` to quickly verify API
- Use `./run_tests.sh --db-test` to verify database connection

### Deployment Phase
- Use `./run_tests.sh --all` to run complete test suite
- Use `./generate_report.sh --run-and-report` to run tests and generate reports
- Use `./manage_flask_env.sh --setup` to set up Flask environment
- Use `python config_manager.py` to manage configuration
- Use `python scripts/init_database.py` to initialize production database

## 🎯 Design Principles

1. **Single Responsibility**: Each script is responsible for only one specific function
2. **Clear Division**: Separation of test execution and Flask management
3. **Easy to Use**: Provide simple and clear command line interface
4. **Error Handling**: Provide clear error messages and solution suggestions
5. **Complete Documentation**: Each script has detailed usage instructions

## 📝 Important Notes

- `run_tests.sh` no longer includes Flask application management functionality
- Manual startup of Flask application is required before running real API tests
- Database scripts require correct MySQL environment configuration
- Configuration management scripts require correct YAML configuration files
