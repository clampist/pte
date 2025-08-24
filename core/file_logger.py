"""
PTE Framework File Logger Module
Provides file logging functionality with rotation, compression, and retention
"""
import os
import logging
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
import threading
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class LogFileHandler:
    """Advanced file logging handler with rotation and retention"""
    
    def __init__(self, config: Dict[str, Any], testcase: str = None, logid: str = None):
        """
        Initialize file logger with configuration
        
        Args:
            config: Logging configuration from common.yaml
            testcase: Current test case name
            logid: Current LogID
        """
        self.config = config
        self.testcase = testcase
        self.logid = logid
        self.file_config = config.get('file', {})
        self.log_dir = Path(self.file_config.get('directory', 'logs'))
        self.filename_format = self.file_config.get('filename_format', 'pte_{date}_{level}.log')
        self.level = getattr(logging, self.file_config.get('level', 'INFO'))
        self.format_str = self.file_config.get('format', '[{timestamp}] [{level}] [{logid}] [{caller}] {message}')
        self.rotate_by_date = self.file_config.get('rotate_by_date', True)
        self.separate_by_level = self.file_config.get('separate_by_level', False)
        self.retention_days = self.file_config.get('retention_days', 30)
        self.max_size_mb = self.file_config.get('max_size_mb', 100)
        self.enable_compression = self.file_config.get('enable_compression', False)
        
        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Thread lock for file operations
        self._lock = threading.Lock()
        
        # Initialize handlers
        self.handlers = {}
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup file handlers based on configuration"""
        if self.separate_by_level:
            # Create separate handlers for each level
            levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
            for level in levels:
                self._create_handler_for_level(level)
        else:
            # Create single handler for all levels
            self._create_handler_for_level('ALL')
    
    def _create_handler_for_level(self, level: str):
        """Create file handler for specific level"""
        filename = self._generate_filename(level, self.logid, self.testcase)
        filepath = self.log_dir / filename
        
        # Create formatter
        formatter = self._create_formatter()
        
        if self.rotate_by_date:
            # Use TimedRotatingFileHandler for date-based rotation
            handler = TimedRotatingFileHandler(
                filename=filepath,
                when='midnight',
                interval=1,
                backupCount=self.retention_days,
                encoding='utf-8'
            )
            handler.suffix = "%Y%m%d"
        else:
            # Use RotatingFileHandler for size-based rotation
            max_bytes = self.max_size_mb * 1024 * 1024 if self.max_size_mb > 0 else 0
            handler = RotatingFileHandler(
                filename=filepath,
                maxBytes=max_bytes,
                backupCount=5,
                encoding='utf-8'
            )
        
        handler.setLevel(self.level)
        handler.setFormatter(formatter)
        
        # Add custom filter for level separation
        if self.separate_by_level and level != 'ALL':
            handler.addFilter(LevelFilter(level))
        
        self.handlers[level] = handler
    
    def _generate_filename(self, level: str, logid: str = None, testcase: str = None) -> str:
        """Generate filename based on format and variables"""
        now = datetime.now()
        date_str = now.strftime('%Y%m%d')
        time_str = now.strftime('%H%M%S')
        datetime_str = now.strftime('%Y%m%d_%H%M%S')
        
        # Use provided logid or instance logid or placeholder
        logid_value = logid or self.logid or '{logid}'
        
        # Use provided testcase or instance testcase or placeholder
        testcase_value = testcase or self.testcase or '{testcase}'
        

        
        # Clean testcase name (remove special characters)
        if testcase_value and testcase_value != '{testcase}':
            testcase_value = testcase_value.replace('::', '_').replace('/', '_').replace('\\', '_')
        
        filename = self.filename_format.format(
            date=date_str,
            time=time_str,
            datetime=datetime_str,
            level=level.lower(),
            logid=logid_value,
            testcase=testcase_value
        )
        
        return filename
    
    def _create_formatter(self):
        """Create custom formatter with variable substitution"""
        class VariableFormatter(logging.Formatter):
            def __init__(self, format_str):
                super().__init__()
                self.format_str = format_str
            
            def format(self, record):
                # Add timestamp if not present
                if not hasattr(record, 'timestamp'):
                    record.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Add logid if not present
                if not hasattr(record, 'logid'):
                    record.logid = getattr(record, 'logid', 'N/A')
                
                # Add caller info if not present
                if not hasattr(record, 'caller_info'):
                    record.caller_info = self._get_caller_info()
                
                # Format the message
                formatted = self.format_str.format(
                    timestamp=record.timestamp,
                    level=record.levelname,
                    logid=record.logid,
                    caller=record.caller_info,
                    message=record.getMessage()
                )
                
                return formatted
            
            def _get_caller_info(self):
                """Get the real caller info, skipping logger methods"""
                import inspect
                import os
                
                for frame_info in inspect.stack():
                    filename = frame_info.filename
                    lineno = frame_info.lineno
                    # Skip logger.py and find the real caller
                    if 'logger.py' not in filename and 'file_logger.py' not in filename and 'test' in filename:
                        return f"{os.path.basename(filename)}:{lineno}"
                return "unknown:0"
        
        return VariableFormatter(self.format_str)
    
    def get_handlers(self) -> Dict[str, logging.Handler]:
        """Get all file handlers"""
        return self.handlers
    
    def cleanup_old_logs(self):
        """Clean up old log files based on retention policy"""
        if self.retention_days <= 0:
            return
        
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        with self._lock:
            for log_file in self.log_dir.glob('*.log*'):
                try:
                    # Check file modification time
                    mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if mtime < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
                except Exception as e:
                    print(f"Error deleting old log file {log_file}: {e}")
    
    def compress_logs(self):
        """Compress old log files if compression is enabled"""
        if not self.enable_compression:
            return
        
        with self._lock:
            for log_file in self.log_dir.glob('*.log.*'):
                if not log_file.name.endswith('.gz'):
                    try:
                        with open(log_file, 'rb') as f_in:
                            gz_file = log_file.with_suffix(log_file.suffix + '.gz')
                            with gzip.open(gz_file, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        
                        # Remove original file after compression
                        log_file.unlink()
                        print(f"Compressed log file: {log_file} -> {gz_file}")
                    except Exception as e:
                        print(f"Error compressing log file {log_file}: {e}")


class LevelFilter(logging.Filter):
    """Filter to separate logs by level"""
    
    def __init__(self, level: str):
        super().__init__()
        self.level = getattr(logging, level)
    
    def filter(self, record):
        return record.levelno == self.level


class LogFileManager:
    """Manager for log file operations"""
    
    def __init__(self, config: Dict[str, Any], testcase: str = None, logid: str = None):
        """
        Initialize log file manager
        
        Args:
            config: Logging configuration from common.yaml
            testcase: Current test case name
            logid: Current LogID
        """
        self.config = config
        self.testcase = testcase
        self.logid = logid
        

        
        self.file_handler = LogFileHandler(config, testcase, logid)
        
        # Schedule cleanup and compression
        self._schedule_maintenance()
    
    def _schedule_maintenance(self):
        """Schedule periodic log maintenance"""
        # This could be enhanced with a proper scheduler
        # For now, we'll do maintenance on initialization
        self.file_handler.cleanup_old_logs()
        self.file_handler.compress_logs()
    
    def get_handlers(self) -> Dict[str, logging.Handler]:
        """Get all file handlers"""
        return self.file_handler.get_handlers()
    
    def add_handlers_to_logger(self, logger: logging.Logger):
        """Add file handlers to a logger"""
        handlers = self.get_handlers()
        for handler in handlers.values():
            logger.addHandler(handler)
    
    def remove_handlers_from_logger(self, logger: logging.Logger):
        """Remove file handlers from a logger"""
        handlers = self.get_handlers()
        for handler in handlers.values():
            logger.removeHandler(handler)
    
    def cleanup(self):
        """Perform cleanup operations"""
        self.file_handler.cleanup_old_logs()
        self.file_handler.compress_logs()
