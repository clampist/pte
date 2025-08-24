"""
PTE Framework Enhanced Logger Module
Provides unified logging functionality with logid support for end-to-end tracing
"""
import logging
import allure
import os
import uuid
import time
import inspect
from typing import Optional, Any, Dict, List
from datetime import datetime
import hashlib
import random
import string

# Import configuration and file logger
try:
    from config.settings import _config_loader
    from core.file_logger import LogFileManager
except ImportError:
    # Fallback for when config is not available
    _config_loader = None
    LogFileManager = None


class LogIdGenerator:
    """Generate unique 32-character logid for tracing"""
    
    @staticmethod
    def generate_logid() -> str:
        """
        Generate a 32-character logid containing numbers and lowercase letters
        
        Returns:
            32-character string with numbers and lowercase letters
        """
        # Use timestamp + random data + hash to ensure uniqueness
        timestamp = str(int(time.time() * 1000000))  # Microsecond precision
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        unique_id = str(uuid.uuid4()).replace('-', '')[:16]
        
        # Combine and hash to get 32 characters
        combined = f"{timestamp}{random_str}{unique_id}"
        hash_obj = hashlib.md5(combined.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Convert to lowercase and ensure it's exactly 32 characters
        logid = hash_hex.lower()
        
        return logid


class PTELogger:
    """PTE Framework Logger with logid support"""
    
    # Class-level storage for accumulated logs
    _accumulated_logs = {}
    
    def __init__(self, name: str = "PTE", level: int = logging.INFO, logid: Optional[str] = None):
        """Initialize logger"""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self._logid = logid or LogIdGenerator.generate_logid()
        
        # Initialize accumulated logs for this logid
        if self._logid not in self._accumulated_logs:
            self._accumulated_logs[self._logid] = {
                'INFO': [],
                'WARNING': [],
                'ERROR': [],
                'DEBUG': []
            }
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    @property
    def logid(self):
        """Get current logid"""
        return self._logid
    
    @logid.setter
    def logid(self, value):
        """Set logid and update accumulated logs"""
        if self._logid != value:
            # Remove old logid from accumulated logs
            if self._logid in self._accumulated_logs:
                del self._accumulated_logs[self._logid]
            
            # Set new logid
            self._logid = value
            
            # Initialize accumulated logs for new logid
            if self._logid not in self._accumulated_logs:
                self._accumulated_logs[self._logid] = {
                    'INFO': [],
                    'WARNING': [],
                    'ERROR': [],
                    'DEBUG': []
                }
            
            # Recreate handlers for new logid
            self._recreate_handlers()
    
    def _recreate_handlers(self):
        """Recreate handlers for current logid"""
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Recreate handlers
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup logging handlers"""
        # Get logging configuration
        logging_config = self._get_logging_config()
        
        # Console handler
        if logging_config.get('console', {}).get('enabled', True):
            console_level = getattr(logging, logging_config.get('console', {}).get('level', 'ERROR'))
            console_handler = logging.StreamHandler()
            console_handler.setLevel(console_level)
            
            # Create custom formatter with real caller info
            class CallerFormatter(logging.Formatter):
                def format(self, record):
                    # Get real caller info (skip logger methods)
                    caller_info = self._get_caller_info()
                    record.caller_info = caller_info
                    
                    # Format: [时间戳] [INFO等级别] [LogId] [文件名：行号] [日志内容]
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    return f"[{timestamp}] [{record.levelname}] [{record.logid}] [{record.caller_info}] {record.getMessage()}"
                
                def _get_caller_info(self):
                    """Get the real caller info, skipping logger methods"""
                    for frame_info in inspect.stack():
                        filename = frame_info.filename
                        lineno = frame_info.lineno
                        # Skip logger.py and find the real caller
                        if 'logger.py' not in filename and 'test' in filename:
                            return f"{os.path.basename(filename)}:{lineno}"
                    return "unknown:0"
            
            # Custom filter to add logid
            class LogIdFilter(logging.Filter):
                def __init__(self, logger_instance):
                    super().__init__()
                    self.logger_instance = logger_instance
                
                def filter(self, record):
                    record.logid = self.logger_instance.logid
                    return True
            
            console_handler.addFilter(LogIdFilter(self))
            console_handler.setFormatter(CallerFormatter())
            
            # Add console handler
            self.logger.addHandler(console_handler)
        
        # File handler
        if logging_config.get('enable_file_logging', False) and LogFileManager:
            try:
                self.file_manager = LogFileManager(logging_config)
                handlers = self.file_manager.get_handlers()
                
                # Add LogID filter to file handlers
                for handler in handlers.values():
                    # Add LogID filter to file handlers
                    class LogIdFilter(logging.Filter):
                        def __init__(self, logger_instance):
                            super().__init__()
                            self.logger_instance = logger_instance
                        
                        def filter(self, record):
                            record.logid = self.logger_instance.logid
                            return True
                    
                    handler.addFilter(LogIdFilter(self))
                
                self.file_manager.add_handlers_to_logger(self.logger)
            except Exception as e:
                # Fallback: log error to console
                print(f"Warning: Failed to setup file logging: {e}")
    
    def _get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration from common.yaml"""
        if _config_loader:
            try:
                common_config = _config_loader.get_common_config()
                return common_config.get('logging', {})
            except Exception:
                pass
        
        # Return default configuration
        return {
            'enable_file_logging': False,
            'console': {
                'enabled': True,
                'level': 'ERROR'
            },
            'file': {
                'directory': 'logs',
                'filename_format': 'pte_{date}_{level}.log',
                'level': 'INFO',
                'format': '[{timestamp}] [{level}] [{logid}] [{caller}] {message}',
                'rotate_by_date': True,
                'separate_by_level': False,
                'retention_days': 30,
                'max_size_mb': 100,
                'enable_compression': False
            }
        }
    
    def _log_to_allure(self, level: str, message: str, data: Optional[Dict] = None):
        """Log to Allure and file with logid - optimized format"""
        # Get real caller info for logs
        caller_info = self._get_caller_info()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Format: [时间戳] [INFO等级别] [LogId] [文件名：行号] [日志内容]
        log_entry = f"[{timestamp}] [{level.upper()}] [{self.logid}] [{caller_info}] {message}"
        
        # Log to file using standard logging
        log_level = getattr(logging, level.upper())
        self.logger.log(log_level, message)
        
        # Add data as separate attachment if provided
        if data:
            allure.attach(
                str(data),
                f"DATA: {level.upper()}: {message}",
                allure.attachment_type.TEXT
            )
        
        # Accumulate logs by level for this logid
        level_key = level.upper()
        if level_key in self._accumulated_logs.get(self.logid, {}):
            self._accumulated_logs[self.logid][level_key].append(log_entry)
    
    def _get_caller_info(self) -> str:
        """Get real caller info, skipping logger methods"""
        for frame_info in inspect.stack():
            filename = frame_info.filename
            lineno = frame_info.lineno
            # Skip logger.py and find the real caller
            if 'logger.py' not in filename and 'test' in filename:
                return f"{os.path.basename(filename)}:{lineno}"
        return "unknown:0"
    
    def get_logid(self) -> str:
        """Get current logid"""
        return self.logid
    
    def get_headers_with_logid(self, additional_headers: Optional[Dict] = None) -> Dict[str, str]:
        """
        Get headers with logid for API requests
        
        Args:
            additional_headers: Additional headers to include
            
        Returns:
            Headers dictionary with logid
        """
        headers = {
            'logId': self.logid,
            'Content-Type': 'application/json'
        }
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    def info(self, message: str, data: Optional[Dict] = None):
        """Log info message with logid"""
        self._log_to_allure("INFO", message, data)
    
    def warning(self, message: str, data: Optional[Dict] = None):
        """Log warning message with logid"""
        self._log_to_allure("WARNING", message, data)
    
    def error(self, message: str, data: Optional[Dict] = None):
        """Log error message with logid"""
        self._log_to_allure("ERROR", message, data)
    
    def debug(self, message: str, data: Optional[Dict] = None):
        """Log debug message with logid"""
        self._log_to_allure("DEBUG", message, data)
    
    def step(self, step_name: str, step_func=None):
        """Decorator for Allure steps with logid logging"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                with allure.step(f"[LOGID:{self.logid}] {step_name}"):
                    self.info(f"Starting step: {step_name}")
                    try:
                        result = func(*args, **kwargs)
                        self.info(f"Step completed: {step_name}")
                        return result
                    except Exception as e:
                        self.error(f"Step failed: {step_name} - {str(e)}")
                        raise
            return wrapper
        
        if step_func:
            return decorator(step_func)
        return decorator
    
    def test_start(self, test_name: str):
        """Log test start with logid"""
        self._log_to_allure("INFO", f"🚀 Starting test: {test_name}")
    
    def test_complete(self, test_name: str, status: str = "PASSED"):
        """Log test completion with logid"""
        status_emoji = {
            "PASSED": "✅",
            "FAILED": "❌", 
            "SKIPPED": "⏭️",
            "ERROR": "💥"
        }
        emoji = status_emoji.get(status.upper(), "📝")
        self._log_to_allure("INFO", f"{emoji} Test completed: {test_name} - {status}")
        
        # Output accumulated logs as consolidated attachments
        self._output_accumulated_logs()
    
    def _output_accumulated_logs(self):
        """Output accumulated logs as consolidated attachments"""
        if self.logid in self._accumulated_logs:
            logs = self._accumulated_logs[self.logid]
            
            # Create consolidated log files by level
            for level, entries in logs.items():
                if entries:
                    consolidated_content = '\n'.join(entries)
                    allure.attach(
                        consolidated_content,
                        f"CONSOLIDATED_{level}_LOGS",
                        allure.attachment_type.TEXT
                    )
            
            # Clean up accumulated logs for this logid
            del self._accumulated_logs[self.logid]
    
    def assertion(self, description: str, condition: bool, expected: Any = None, actual: Any = None):
        """Log assertion with logid details"""
        if condition:
            self._log_to_allure("INFO", f"✅ Assertion passed: {description}")
        else:
            error_data = {
                "description": description,
                "expected": expected,
                "actual": actual,
                "logid": self.logid
            }
            self._log_to_allure("ERROR", f"❌ Assertion failed: {description}", error_data)
    
    def api_call(self, method: str, url: str, status_code: Optional[int] = None, 
                 response_time: Optional[float] = None, request_data: Optional[Dict] = None,
                 response_data: Optional[Dict] = None):
        """Log API call details with logid"""
        message = f"🌐 API Call: {method} {url}"
        if status_code:
            message += f" - Status: {status_code}"
        if response_time:
            message += f" - Time: {response_time:.2f}s"
        
        data = {
            "method": method,
            "url": url,
            "status_code": status_code,
            "response_time": response_time,
            "logid": self.logid,
            "request_data": request_data,
            "response_data": response_data
        }
        self.info(message, data)
    
    def data_validation(self, field: str, expected: Any, actual: Any, passed: bool):
        """Log data validation with logid"""
        if passed:
            self._log_to_allure("INFO", f"✅ Data validation passed: {field}")
        else:
            error_data = {
                "field": field,
                "expected": expected,
                "actual": actual,
                "logid": self.logid
            }
            self._log_to_allure("ERROR", f"❌ Data validation failed: {field}", error_data)


class TestLogger:
    """Test-specific logger with logid and enhanced features"""
    
    def __init__(self, test_class_name: str = "Test", logid: Optional[str] = None):
        """Initialize test logger with logid"""
        self.logid = logid or LogIdGenerator.generate_logid()
        self.logger = PTELogger(f"{test_class_name}Logger", logid=self.logid)
        self.test_class_name = test_class_name
        self.test_start_time = None
    
    @property
    def logid(self):
        """Get current logid"""
        return self._logid
    
    @logid.setter
    def logid(self, value):
        """Set logid and update logger"""
        self._logid = value
        if hasattr(self, 'logger'):
            self.logger.logid = value
    
    def start_test(self, test_method_name: str):
        """Start test logging with logid"""
        self.test_start_time = datetime.now()
        test_name = f"{self.test_class_name}.{test_method_name}"
        self.logger.test_start(test_name)
    
    def _add_logid_attachment(self, test_name: str):
        """Add LogID attachment to Allure report"""
        # Add LogID as Allure attachment (simple format)
        allure.attach(
            f"LogID: {self.logid}",
            "logId",
            allure.attachment_type.TEXT
        )
    
    def end_test(self, test_method_name: str, status: str = "PASSED"):
        """End test logging with logid"""
        test_name = f"{self.test_class_name}.{test_method_name}"
        if self.test_start_time:
            duration = (datetime.now() - self.test_start_time).total_seconds()
            self.logger.info(f"⏱️ Test duration: {duration:.2f} seconds")
        
        self.logger.test_complete(test_name, status)
    
    def get_logid(self) -> str:
        """Get current logid"""
        return self.logid
    
    def get_headers_with_logid(self, additional_headers: Optional[Dict] = None) -> Dict[str, str]:
        """Get headers with logid for API requests"""
        return self.logger.get_headers_with_logid(additional_headers)
    
    def step(self, step_name: str):
        """Create Allure step with logid logging"""
        return self.logger.step(step_name)
    
    def info(self, message: str, data: Optional[Dict] = None):
        """Log info message with logid"""
        self.logger.info(message, data)
    
    def warning(self, message: str, data: Optional[Dict] = None):
        """Log warning message with logid"""
        self.logger.warning(message, data)
    
    def error(self, message: str, data: Optional[Dict] = None):
        """Log error message with logid"""
        self.logger.error(message, data)
    
    def debug(self, message: str, data: Optional[Dict] = None):
        """Log debug message with logid"""
        self.logger.debug(message, data)
    
    def assertion(self, description: str, condition: bool, expected: Any = None, actual: Any = None):
        """Log assertion with logid"""
        self.logger.assertion(description, condition, expected, actual)
    
    def api_call(self, method: str, url: str, status_code: Optional[int] = None, 
                 response_time: Optional[float] = None, request_data: Optional[Dict] = None,
                 response_data: Optional[Dict] = None):
        """Log API call with logid"""
        self.logger.api_call(method, url, status_code, response_time, request_data, response_data)
    
    def data_validation(self, field: str, expected: Any, actual: Any, passed: bool):
        """Log data validation with logid"""
        self.logger.data_validation(field, expected, actual, passed)


# Global logger instance
logger = PTELogger("PTE")


def get_test_logger(test_class_name: str = "Test", logid: Optional[str] = None) -> TestLogger:
    """Get test logger instance with optional logid"""
    return TestLogger(test_class_name, logid)


def generate_logid() -> str:
    """Generate a new logid"""
    return LogIdGenerator.generate_logid()


class Log:
    """
    Static logging utility class for easy access across all layers.
    Automatically handles LogID generation and management.
    """
    
    _current_logid: Optional[str] = None
    _logger_instance: Optional[TestLogger] = None
    
    @classmethod
    def _get_logger(cls) -> TestLogger:
        """Get or create logger instance with current LogID"""
        if cls._logger_instance is None:
            cls._logger_instance = TestLogger("PTE", logid=cls._current_logid)
            # Add LogID attachment when creating logger instance
            if cls._current_logid:
                cls._logger_instance._add_logid_attachment("auto_generated")
        return cls._logger_instance
    
    @classmethod
    def set_logid(cls, logid: str):
        """Set current LogID for the session"""
        cls._current_logid = logid
        if cls._logger_instance:
            cls._logger_instance.logid = logid
            # Add LogID attachment when setting logid
            cls._logger_instance._add_logid_attachment("auto_generated")
    
    @classmethod
    def get_logid(cls) -> str:
        """Get current LogID"""
        if cls._current_logid is None:
            cls._current_logid = generate_logid()
            # Update logger instance if it exists
            if cls._logger_instance:
                cls._logger_instance.logid = cls._current_logid
                # Add LogID attachment when auto-generating logid
                cls._logger_instance._add_logid_attachment("auto_generated")
        return cls._current_logid
    
    @classmethod
    def get_headers_with_logid(cls, additional_headers: Optional[Dict] = None) -> Dict[str, str]:
        """Get headers with current LogID"""
        headers = {
            'logId': cls.get_logid(),
            'Content-Type': 'application/json'
        }
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    @classmethod
    def info(cls, message: str, data: Optional[Dict] = None):
        """Log info message with current LogID"""
        cls._get_logger().info(message, data)
    
    @classmethod
    def warning(cls, message: str, data: Optional[Dict] = None):
        """Log warning message with current LogID"""
        cls._get_logger().warning(message, data)
    
    @classmethod
    def error(cls, message: str, data: Optional[Dict] = None):
        """Log error message with current LogID"""
        cls._get_logger().error(message, data)
    
    @classmethod
    def debug(cls, message: str, data: Optional[Dict] = None):
        """Log debug message with current LogID"""
        cls._get_logger().debug(message, data)
    
    @classmethod
    def assertion(cls, description: str, condition: bool, expected: Any = None, actual: Any = None):
        """Log assertion with current LogID"""
        cls._get_logger().assertion(description, condition, expected, actual)
    
    @classmethod
    def api_call(cls, method: str, url: str, status_code: Optional[int] = None, 
                 response_time: Optional[float] = None, request_data: Optional[Dict] = None,
                 response_data: Optional[Dict] = None):
        """Log API call with current LogID"""
        cls._get_logger().api_call(method, url, status_code, response_time, request_data, response_data)
    
    @classmethod
    def data_validation(cls, field: str, expected: Any, actual: Any, passed: bool):
        """Log data validation with current LogID"""
        cls._get_logger().data_validation(field, expected, actual, passed)
    
    @classmethod
    def step(cls, step_name: str):
        """Create Allure step with current LogID"""
        return cls._get_logger().step(step_name)
    
    @classmethod
    def start_test(cls, test_method_name: str):
        """Start test logging with current LogID"""
        cls._get_logger().start_test(test_method_name)
    
    @classmethod
    def end_test(cls, test_method_name: str, status: str = "PASSED"):
        """End test logging with current LogID"""
        cls._get_logger().end_test(test_method_name, status)
    
    @classmethod
    def test_start(cls, test_name: str):
        """Log test start with current LogID"""
        cls._get_logger().test_start(test_name)
    
    @classmethod
    def test_complete(cls, test_name: str, status: str = "PASSED"):
        """Log test completion with current LogID"""
        cls._get_logger().test_complete(test_name, status)
    
    @classmethod
    def raw(cls, message: str, *args, **kwargs):
        """Raw print-like logging with unified format (replaces print())"""
        # Format message with args and kwargs like print()
        formatted_message = message
        if args:
            formatted_message = message % args if '%' in message else f"{message} {' '.join(map(str, args))}"
        
        # Print directly to console (like original print())
        print(formatted_message, **kwargs)
        
        # Also log to Allure for traceability with unified format
        cls._get_logger().logger._log_to_allure("INFO", formatted_message)
    
    @classmethod
    def print(cls, message: str, *args, **kwargs):
        """Alias for Log.raw() - direct replacement for print()"""
        cls.raw(message, *args, **kwargs)
