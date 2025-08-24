# PTE Framework Architecture Guide

## Overview

This guide covers the design principles, system architecture, and implementation details of the PTE Framework. This information helps users understand how the framework works internally and how to extend it effectively.

## Design Principles

### 1. Layered Architecture

The PTE Framework follows a clear layered architecture design:

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Layer (test/)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Business Logic Layer (biz/)            │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │           API Interface Layer (api/)        │   │   │
│  │  │  ┌─────────────────────────────────────┐   │   │   │
│  │  │  │         Core Framework Layer        │   │   │   │
│  │  │  │              (core/)                │   │   │   │
│  │  │  └─────────────────────────────────────┘   │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

#### Layer Responsibilities

- **Core Layer (`core/`)**: Universal framework functionality, independent of specific business
- **API Layer (`api/`)**: HTTP client wrapper, supporting different backend systems
- **Business Layer (`biz/`)**: Business logic wrapper, inheriting core layer functionality
- **Test Layer (`test/`)**: Test case writing, using business layer functionality

### 2. Configuration Management

The framework uses a hierarchical configuration management system:

```
config/
├── env.yaml              # Environment management configuration
├── common.yaml           # Common configuration (logging, etc.)
├── local_test.yaml       # Local testing environment
├── aws_offline.yaml      # AWS offline environment
├── gcp_offline.yaml      # GCP offline environment
├── aws_online.yaml       # AWS online environment
├── gcp_online.yaml       # GCP online environment
└── settings.py           # Configuration management class
```

#### Configuration Hierarchy

1. **Environment Configuration**: Defines current IDC and environment
2. **IDC Configuration**: Specific configuration for each IDC
3. **Common Configuration**: Shared settings across all environments
4. **Dynamic Override**: Environment variables can override any setting

### 3. Test Classification

The framework separates tests into two categories:

- **Framework Demo Tests**: Demonstrate framework functionality, help developers learn
- **Business Case Tests**: Actual business scenario tests, validate business logic

## System Architecture

### Core Components

#### 1. Configuration Management (`config/`)

```python
# config/settings.py
class ConfigManager:
    """Configuration management class"""
    
    def __init__(self):
        self.env_config = self._load_env_config()
        self.idc_config = self._load_idc_config()
        self.common_config = self._load_common_config()
    
    def get_config(self, key, default=None):
        """Get configuration value with fallback chain"""
        # 1. Environment variable override
        # 2. IDC configuration
        # 3. Common configuration
        # 4. Default value
```

#### 2. Core Framework (`core/`)

```python
# core/checker.py - Universal data validator
class Checker:
    """Universal data validation utility"""
    
    @staticmethod
    def assert_not_none(value, field_name):
        """Assert value is not None"""
    
    @staticmethod
    def assert_int_data(value, field_name):
        """Assert value is integer"""
    
    @staticmethod
    def assert_field_value(data, field, expected_value):
        """Assert field value matches expected"""

# core/db_checker.py - Database operations
class BaseDBChecker:
    """Base database checker with common operations"""
    
    def __init__(self, db_config):
        self.db_config = db_config
        self.engine = self._create_engine()
    
    def execute_query(self, sql, params=None):
        """Execute SELECT query"""
    
    def execute_update(self, sql, params=None):
        """Execute UPDATE/INSERT/DELETE query"""
    
    def assert_table_exists(self, table_name):
        """Assert table exists in database"""

# core/logger.py - Logging system
class Log:
    """Unified logging utility class"""
    
    _current_logid = None
    _logger_instance = None
    
    @classmethod
    def info(cls, message, data=None):
        """Log info message with optional data"""
    
    @classmethod
    def api_call(cls, method, url, status_code=None, response_time=None, 
                 request_data=None, response_data=None):
        """Log API call with details"""
```

#### 3. API Interface (`api/`)

```python
# api/client.py - HTTP client wrapper
class APIClient:
    """HTTP client wrapper with LogID support"""
    
    def __init__(self, base_url=None, headers=None, logid=None):
        self.base_url = base_url or self._get_base_url()
        self.headers = headers or {}
        self.logid = logid or Log.get_logid()
        self._add_logid_to_headers()
    
    def get(self, endpoint, params=None, **kwargs):
        """Make GET request"""
    
    def post(self, endpoint, data=None, json=None, **kwargs):
        """Make POST request"""
    
    def _add_logid_to_headers(self):
        """Add LogID to request headers"""
```

#### 4. Business Logic (`biz/`)

```python
# biz/department/user/operations.py - Business operations
class UserOperations:
    """User business operations wrapper"""
    
    def __init__(self, env=None, custom_headers=None):
        self.api_client = APIClient(custom_headers=custom_headers)
        self.config = self._load_config(env)
    
    def get_all_users(self):
        """Get all users"""
        return self.api_client.get("/api/users")
    
    def create_user(self, user_data):
        """Create new user"""
        return self.api_client.post("/api/users", json=user_data)
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.api_client.get(f"/api/users/{user_id}")

# biz/department/user/db_operations.py - Database operations
class UserDBOperations:
    """User database operations"""
    
    def __init__(self):
        self.db_checker = self._create_db_checker()
    
    def create_test_user(self, user_data):
        """Create test user in database"""
    
    def update_test_user(self, user_id, update_data):
        """Update test user in database"""
    
    def delete_test_user(self, user_id):
        """Delete test user from database"""
```

### Data Flow Architecture

#### 1. Test Execution Flow

```
Test Case → Business Operations → API Client → HTTP Request → Target System
    ↓              ↓                ↓            ↓              ↓
  Logging → Business Logging → API Logging → Request Logging → Response Logging
```

#### 2. Configuration Flow

```
Environment Variables → Config Manager → IDC Config → Common Config → Default Values
        ↓                    ↓              ↓            ↓              ↓
    Override Values → Merged Configuration → Framework Components
```

#### 3. Logging Flow

```
Test Execution → Log Class → File Logger → Allure Reporter → Console Output
      ↓            ↓           ↓            ↓              ↓
   LogID → Structured Log → File Output → Allure Report → Console Display
```

## Implementation Details

### 1. LogID System

#### Automatic LogID Generation

```python
# core/fixtures.py
@pytest.fixture(autouse=True)
def auto_logid():
    """Automatically generate and set LogID for each test case"""
    logid = generate_logid()
    Log.set_logid(logid)
    Log._get_logger()._add_logid_attachment("auto_generated")
    yield logid

# core/logger.py
def generate_logid() -> str:
    """Generate unique 32-character LogID"""
    timestamp = str(int(time.time() * 1000))
    random_data = str(random.randint(1000, 9999))
    uuid_data = str(uuid.uuid4())
    
    # Combine and hash
    combined = f"{timestamp}{random_data}{uuid_data}"
    return hashlib.md5(combined.encode()).hexdigest()
```

#### LogID Propagation

```python
# API Client automatically adds LogID to headers
def _add_logid_to_headers(self):
    """Add LogID to request headers"""
    if self.logid:
        self.headers['logId'] = self.logid

# Business operations inherit LogID from test context
def __init__(self, env=None, custom_headers=None):
    self.api_client = APIClient(custom_headers=custom_headers)
    # LogID is automatically available from Log.get_logid()
```

### 2. Configuration Management

#### Configuration Loading

```python
# config/settings.py
def _load_env_config(self):
    """Load environment configuration"""
    env_file = os.path.join(self.config_dir, 'env.yaml')
    return self._load_yaml_file(env_file)

def _load_idc_config(self):
    """Load IDC-specific configuration"""
    idc_name = self.env_config.get('idc', 'local_test')
    idc_file = os.path.join(self.config_dir, f'{idc_name}.yaml')
    return self._load_yaml_file(idc_file)

def _load_common_config(self):
    """Load common configuration"""
    common_file = os.path.join(self.config_dir, 'common.yaml')
    return self._load_yaml_file(common_file)
```

#### Environment Variable Override

```python
def get_config(self, key, default=None):
    """Get configuration with environment variable override"""
    # Check environment variable first
    env_key = f"TEST_{key.upper()}"
    if env_key in os.environ:
        return os.environ[env_key]
    
    # Check IDC configuration
    if key in self.idc_config:
        return self.idc_config[key]
    
    # Check common configuration
    if key in self.common_config:
        return self.common_config[key]
    
    return default
```

### 3. Database Integration

#### Connection Pooling

```python
# core/db_checker.py
def _create_engine(self):
    """Create SQLAlchemy engine with connection pooling"""
    return create_engine(
        self.db_config.connection_string,
        pool_size=self.db_config.pool_size,
        max_overflow=self.db_config.max_overflow,
        pool_timeout=self.db_config.pool_timeout,
        pool_recycle=self.db_config.pool_recycle
    )
```

#### Transaction Management

```python
def execute_update(self, sql, params=None):
    """Execute UPDATE/INSERT/DELETE with transaction"""
    with self.engine.begin() as connection:
        result = connection.execute(text(sql), params or {})
        return result.rowcount
```

### 4. Parallel Testing Support

#### Pytest-xdist Integration

```python
# pte.sh - Parallel test execution
def run_pytest(self, test_path, parallel=False, workers=None):
    """Run pytest with optional parallel execution"""
    cmd = ["python", "-m", "pytest", test_path]
    
    if parallel:
        if workers:
            cmd.extend(["-n", str(workers)])
        else:
            cmd.extend(["-n", "auto"])
    
    return subprocess.run(cmd, check=True)
```

#### Test Markers

```python
# pytest.ini
[tool:pytest]
markers =
    parallel: marks tests as safe for parallel execution
    no_parallel: marks tests that should not run in parallel
```

## Extension Points

### 1. Custom Checkers

```python
# Extend the base Checker class
from core.checker import Checker

class CustomChecker(Checker):
    @staticmethod
    def assert_custom_business_rule(value, field_name):
        """Custom business rule validation"""
        if not self._validate_business_rule(value):
            raise AssertionError(f"{field_name} failed business rule validation")
```

### 2. Custom Database Operations

```python
# Extend the base database checker
from core.db_checker import BaseDBChecker

class CustomDBChecker(BaseDBChecker):
    def assert_custom_table_structure(self, table_name):
        """Custom table structure validation"""
        # Implementation here
        pass
```

### 3. Custom Business Operations

```python
# Extend business operations
from biz.department.user.operations import UserOperations

class ExtendedUserOperations(UserOperations):
    def bulk_operations(self, operations):
        """Custom bulk operations"""
        # Implementation here
        pass
```

### 4. Custom Configuration

```python
# Add custom configuration sections
# config/custom.yaml
custom_features:
    feature_flag_1: true
    feature_flag_2: false
    custom_timeout: 60
```

## Performance Considerations

### 1. Connection Pooling

- Database connections are pooled to reduce connection overhead
- Pool size and overflow settings are configurable
- Connections are automatically recycled

### 2. Logging Optimization

- File logging is configurable and can be disabled
- Log levels can be set independently for different outputs
- Log rotation prevents disk space issues

### 3. Parallel Execution

- Tests can be marked for parallel execution
- CPU core detection for optimal worker count
- Resource isolation between test processes

### 4. Configuration Caching

- Configuration is loaded once and cached
- Environment variable overrides are checked at runtime
- YAML files are parsed efficiently

## Security Considerations

### 1. Sensitive Data Handling

- Passwords and tokens should be stored in environment variables
- Configuration files should not contain sensitive data
- Log files should not include sensitive information

### 2. Database Security

- Database credentials are managed securely
- Connection strings are validated
- SQL injection prevention through parameterized queries

### 3. API Security

- API keys and tokens are handled securely
- Request headers are sanitized
- HTTPS is used for production environments

## Monitoring and Observability

### 1. Logging Strategy

- Structured logging with consistent format
- LogID for end-to-end tracing
- Multiple output destinations (file, console, Allure)

### 2. Metrics Collection

- Test execution time tracking
- API response time monitoring
- Database operation performance

### 3. Error Handling

- Comprehensive error logging
- Stack trace preservation
- Error context information

## Future Enhancements

### 1. Plugin System

- Extensible plugin architecture
- Custom test runners
- Third-party integrations

### 2. Cloud Integration

- AWS/GCP native integrations
- Container orchestration support
- Cloud-native monitoring

### 3. Advanced Reporting

- Custom report formats
- Integration with CI/CD systems
- Real-time test monitoring

### 4. Performance Testing

- Load testing capabilities
- Performance benchmarking
- Resource utilization monitoring
