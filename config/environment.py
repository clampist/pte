#!/usr/bin/env python3
"""
Environment Configuration
Environment variables and path configurations
"""
import os
from pathlib import Path
from typing import Optional


class EnvironmentConfig:
    """Environment configuration class"""
    
    # Project paths
    PTE_ROOT = Path(__file__).parent.parent
    TARGET_APP_ROOT = Path(os.environ.get('PTE_TARGET_ROOT', PTE_ROOT.parent / 'pte_target'))
    TARGET_APP_FLASK_DIR = TARGET_APP_ROOT / 'flask_app'
    
    # Environment variables
    TEST_IDC = os.environ.get('TEST_IDC', 'local_test')
    TEST_ENV = os.environ.get('TEST_ENV', 'local')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Server configuration
    TARGET_APP_HOST = os.environ.get('TARGET_APP_HOST', 'localhost')
    TARGET_APP_PORT = int(os.environ.get('TARGET_APP_PORT', '5001'))
    TARGET_APP_HEALTH_URL = f"http://{TARGET_APP_HOST}:{TARGET_APP_PORT}/api/health"
    
    @classmethod
    def get_pte_root(cls) -> Path:
        """Get PTE project root directory"""
        return cls.PTE_ROOT
    
    @classmethod
    def get_target_app_root(cls) -> Path:
        """Get target application root directory"""
        return cls.TARGET_APP_ROOT
    
    @classmethod
    def get_target_app_flask_dir(cls) -> Path:
        """Get target application Flask directory"""
        return cls.TARGET_APP_FLASK_DIR
    
    @classmethod
    def get_target_app_health_url(cls) -> str:
        """Get target application health check URL"""
        return cls.TARGET_APP_HEALTH_URL
    
    @classmethod
    def validate_paths(cls) -> bool:
        """Validate that all required paths exist"""
        paths_to_check = [
            cls.PTE_ROOT,
            cls.TARGET_APP_ROOT,
            cls.TARGET_APP_FLASK_DIR
        ]
        
        for path in paths_to_check:
            if not path.exists():
                print(f"❌ Path does not exist: {path}")
                return False
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current environment configuration"""
        print("=== Environment Configuration ===")
        print(f"PTE Root: {cls.PTE_ROOT}")
        print(f"Target App Root: {cls.TARGET_APP_ROOT}")
        print(f"Target App Flask Dir: {cls.TARGET_APP_FLASK_DIR}")
        print(f"Target App Health URL: {cls.TARGET_APP_HEALTH_URL}")
        print(f"Test IDC: {cls.TEST_IDC}")
        print(f"Test Environment: {cls.TEST_ENV}")
        print(f"Flask Environment: {cls.FLASK_ENV}")
        print("==================================")


# Convenience functions
def get_pte_root() -> Path:
    """Get PTE project root directory"""
    return EnvironmentConfig.get_pte_root()


def get_target_app_root() -> Path:
    """Get target application root directory"""
    return EnvironmentConfig.get_target_app_root()


def get_target_app_flask_dir() -> Path:
    """Get target application Flask directory"""
    return EnvironmentConfig.get_target_app_flask_dir()


def get_target_app_health_url() -> str:
    """Get target application health check URL"""
    return EnvironmentConfig.get_target_app_health_url()


def validate_environment() -> bool:
    """Validate environment configuration"""
    return EnvironmentConfig.validate_paths()


def print_environment_config():
    """Print environment configuration"""
    EnvironmentConfig.print_config()
