"""
Global configuration settings for test environments
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigLoader:
    """YAML configuration loader with IDC-specific support"""
    
    def __init__(self, idc_name: str = None):
        """
        Initialize configuration loader
        
        Args:
            idc_name: IDC name (aws_offline, gcp_offline, aws_online, gcp_online)
        """
        self.config_dir = Path(__file__).parent
        
        # Load env.yaml first
        self.env_config = self._load_env_config()
        
        # Determine IDC name
        if idc_name is None:
            idc_name = self.env_config.get("idc", "aws_offline")
        
        self.idc_name = idc_name
        self.idc_config = self._load_idc_config(idc_name)
    
    def _load_env_config(self) -> Dict[str, Any]:
        """Load env.yaml configuration"""
        env_file = self.config_dir / "env.yaml"
        if not env_file.exists():
            raise FileNotFoundError(f"Environment config file not found: {env_file}")
        
        with open(env_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _load_idc_config(self, idc_name: str) -> Dict[str, Any]:
        """Load IDC-specific configuration"""
        # Direct mapping from IDC name to config file
        config_file = f"{idc_name}.yaml"
        idc_file = self.config_dir / config_file
        
        if not idc_file.exists():
            raise FileNotFoundError(f"IDC config file not found: {idc_file}")
        
        with open(idc_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def reload_config(self):
        """Reload configuration from files"""
        self.env_config = self._load_env_config()
        self.idc_config = self._load_idc_config(self.idc_name)
    
    def get_env_config(self) -> Dict[str, Any]:
        """Get environment configuration"""
        return self.env_config
    
    def get_idc_config(self) -> Dict[str, Any]:
        """Get IDC configuration"""
        return self.idc_config
    
    def get_environments(self) -> Dict[str, Any]:
        """Get environments configuration"""
        return self.idc_config.get("environments", {})
    
    def get_test_config(self) -> Dict[str, Any]:
        """Get test configuration"""
        return self.idc_config.get("test_config", {})
    
    def get_host(self) -> str:
        """Get host URL"""
        return self.idc_config.get("host", "")
    
    def get_default_timeout(self) -> int:
        """Get default timeout"""
        return self.idc_config.get("timeout", 30)
    
    def get_default_retry_count(self) -> int:
        """Get default retry count"""
        return self.idc_config.get("retry_count", 3)
    
    def get_default_headers(self) -> Dict[str, str]:
        """Get default headers"""
        return self.idc_config.get("default_headers", {})
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return self.idc_config.get("database", {})


# Global configuration loader instance
_config_loader = ConfigLoader()


class TestEnvironment:
    """Test environment configuration with IDC-specific support"""
    
    @classmethod
    def get_current_idc(cls) -> str:
        """Get current IDC"""
        return os.getenv("TEST_IDC", _config_loader.env_config.get("idc", "aws_offline"))
    
    @classmethod
    def get_current_env(cls) -> str:
        """Get current test environment"""
        return os.getenv("TEST_ENV", _config_loader.env_config.get("env", "prod"))
    
    @classmethod
    def get_server_language(cls) -> str:
        """Get server language configuration"""
        return _config_loader.env_config.get("server_language", "python")
    
    @classmethod
    def _get_config_loader(cls) -> ConfigLoader:
        """Get current configuration loader"""
        current_idc = cls.get_current_idc()
        if current_idc != _config_loader.idc_name:
            # Create new loader if IDC changed
            return ConfigLoader(current_idc)
        return _config_loader
    
    @classmethod
    def get_config(cls, env: str = None) -> Dict[str, Any]:
        """Get configuration for specified environment"""
        if env is None:
            env = cls.get_current_env()
        
        config_loader = cls._get_config_loader()
        environments = config_loader.get_environments()
        
        if env not in environments:
            raise ValueError(f"Unknown environment: {env}")
        
        env_config = environments[env].copy()
        
        # Merge with default configuration
        env_config["host"] = config_loader.get_host()
        if "timeout" not in env_config:
            env_config["timeout"] = config_loader.get_default_timeout()
        if "retry_count" not in env_config:
            env_config["retry_count"] = config_loader.get_default_retry_count()
        
        # Merge headers
        default_headers = config_loader.get_default_headers()
        env_headers = env_config.get("headers", {})
        env_config["headers"] = {**default_headers, **env_headers}
        
        return env_config
    
    @classmethod
    def get_host(cls, env: str = None) -> str:
        """Get host URL for specified environment"""
        config = cls.get_config(env)
        return config["host"]
    
    @classmethod
    def get_headers(cls, env: str = None) -> Dict[str, str]:
        """Get default headers for specified environment"""
        config = cls.get_config(env)
        return config["headers"].copy()
    
    @classmethod
    def get_timeout(cls, env: str = None) -> int:
        """Get timeout for specified environment"""
        config = cls.get_config(env)
        return config["timeout"]
    
    @classmethod
    def get_retry_count(cls, env: str = None) -> int:
        """Get retry count for specified environment"""
        config = cls.get_config(env)
        return config["retry_count"]
    
    @classmethod
    def get_description(cls, env: str = None) -> str:
        """Get environment description"""
        config = cls.get_config(env)
        return config.get("description", "")
    
    @classmethod
    def get_idc(cls) -> str:
        """Get current IDC"""
        return cls.get_current_idc()
    
    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        """Get database configuration"""
        config_loader = cls._get_config_loader()
        return config_loader.get_database_config()
    
    @classmethod
    def get_mysql_config(cls) -> Dict[str, Any]:
        """Get MySQL database configuration"""
        db_config = cls.get_database_config()
        return db_config.get("mysql", {})
    
    @classmethod
    def list_environments(cls) -> Dict[str, str]:
        """List all available environments with descriptions"""
        config_loader = cls._get_config_loader()
        environments = config_loader.get_environments()
        return {env: config.get("description", "") for env, config in environments.items()}
    
    @classmethod
    def list_available_idcs(cls) -> Dict[str, str]:
        """List all available IDCs with descriptions"""
        # Hardcoded IDC list since we removed available_idcs from env.yaml
        return {
            "aws_offline": "Offline AWS Environment",
            "gcp_offline": "Offline GCP Environment", 
            "aws_online": "Online AWS Environment",
            "gcp_online": "Online GCP Environment"
        }
    
    @classmethod
    def reload_config(cls):
        """Reload configuration from file"""
        cls._get_config_loader().reload_config()


class APIConfig:
    """API configuration constants - now directly defined in api/config.py"""
    
    # This class is now just a placeholder for backward compatibility
    # All actual API configuration is now in api/config.py
    pass


class TestConfig:
    """Test configuration constants"""
    
    @classmethod
    def _get_test_config(cls) -> Dict[str, Any]:
        """Get test configuration from current config"""
        config_loader = TestEnvironment._get_config_loader()
        return config_loader.get_test_config()
    
    @classmethod
    def get_test_data_dir(cls) -> str:
        """Get test data directory"""
        return cls._get_test_config().get("test_data_dir", "data")
    
    @classmethod
    def get_test_report_dir(cls) -> str:
        """Get test report directory"""
        return cls._get_test_config().get("test_report_dir", "reports")
    
    @classmethod
    def get_test_log_dir(cls) -> str:
        """Get test log directory"""
        return cls._get_test_config().get("test_log_dir", "logs")
    
    @classmethod
    def get_default_markers(cls) -> list:
        """Get default test markers"""
        return cls._get_test_config().get("default_markers", [])
    
    # Convenience properties for backward compatibility
    @property
    def TEST_DATA_DIR(self) -> str:
        return self.get_test_data_dir()
    
    @property
    def TEST_REPORT_DIR(self) -> str:
        return self.get_test_report_dir()
    
    @property
    def TEST_LOG_DIR(self) -> str:
        return self.get_test_log_dir()
    
    @property
    def DEFAULT_MARKERS(self) -> list:
        return self.get_default_markers()


# Create singleton instances for backward compatibility
test_config = TestConfig()
