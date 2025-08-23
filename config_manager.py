#!/usr/bin/env python3
"""
Configuration management tool
Usage: python config_manager.py [command] [options]
"""

import argparse
import sys
import os
from pathlib import Path
from config.settings import TestEnvironment, ConfigLoader


def list_environments():
    """List all available environments"""
    current_idc = TestEnvironment.get_current_idc()
    current_env = TestEnvironment.get_current_env()
    
    print(f"=== Available Environment List ({current_idc.upper()}) ===")
    
    environments = TestEnvironment.list_environments()
    available_idcs = TestEnvironment.list_available_idcs()
    
    print("\nEnvironment Configuration:")
    for env, description in environments.items():
        current = " (current)" if env == current_env else ""
        print(f"  {env}{current}: {description}")
    
    print("\nAvailable IDC List:")
    for idc, description in available_idcs.items():
        current = " (current)" if idc == current_idc else ""
        print(f"  {idc}{current}: {description}")
    
    print(f"\nCurrent IDC: {current_idc}")
    print(f"Current Environment: {current_env}")
    print(f"Environment Variable: TEST_IDC={os.getenv('TEST_IDC', 'Not set')}")
    print(f"Environment Variable: TEST_ENV={os.getenv('TEST_ENV', 'Not set')}")


def show_environment(env_name):
    """Show detailed environment configuration"""
    try:
        config = TestEnvironment.get_config(env_name)
        
        print(f"=== Environment Configuration: {env_name} ===")
        print(f"Description: {config.get('description', 'No description')}")
        print(f"Host: {config['host']}")
        print(f"Timeout: {config['timeout']} seconds")
        print(f"Retry Count: {config['retry_count']}")
        print("Headers:")
        for key, value in config['headers'].items():
            print(f"  {key}: {value}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def show_current_environment():
    """Show current environment configuration"""
    current_env = TestEnvironment.get_current_env()
    show_environment(current_env)


def show_idc(idc_name):
    """Show IDC configuration"""
    try:
        config_loader = ConfigLoader(idc_name)
        idc_config = config_loader.get_idc_config()
        
        print(f"=== IDC Configuration: {idc_name} ===")
        print(f"Host: {idc_config.get('host', 'Not configured')}")
        print(f"Default Timeout: {idc_config.get('timeout', 'Not configured')} seconds")
        print(f"Default Retry Count: {idc_config.get('retry_count', 'Not configured')}")
        print("Default Headers:")
        for key, value in idc_config.get('default_headers', {}).items():
            print(f"  {key}: {value}")
        
        # Show database configuration
        db_config = idc_config.get('database', {})
        if db_config:
            print("\nDatabase Configuration:")
            for db_type, db_info in db_config.items():
                print(f"  {db_type}:")
                print(f"    Host: {db_info.get('host', 'Not configured')}")
                print(f"    Port: {db_info.get('port', 'Not configured')}")
                print(f"    Database: {db_info.get('database', 'Not configured')}")
                print(f"    Username: {db_info.get('username', 'Not configured')}")
                print(f"    Pool Size: {db_info.get('pool_size', 'Not configured')}")
                print(f"    Description: {db_info.get('description', 'Not configured')}")
        
        # Show environments in this IDC
        environments = config_loader.get_environments()
        print(f"\nEnvironment Count: {len(environments)}")
        for env, config in environments.items():
            print(f"  {env}: {config.get('description', 'No description')}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def validate_config():
    """Validate configuration file"""
    try:
        current_idc = TestEnvironment.get_current_idc()
        config_loader = ConfigLoader(current_idc)
        
        print(f"=== Configuration Validation ({current_idc.upper()}) ===")
        print("✅ Environment configuration file loaded successfully")
        
        # Validate env.yaml
        env_config = config_loader.get_env_config()
        if "idc" not in env_config:
            print("❌ env.yaml missing idc configuration")
            return False
        
        if "env" not in env_config:
            print("❌ env.yaml missing env configuration")
            return False
        
        print("✅ env.yaml configuration complete")
        
        # Validate IDC configuration
        idc_config = config_loader.get_idc_config()
        required_idc_fields = ["host", "timeout", "retry_count", "environments"]
        missing_fields = [field for field in required_idc_fields if field not in idc_config]
        
        if missing_fields:
            print(f"❌ IDC configuration missing fields: {missing_fields}")
            return False
        
        print(f"✅ IDC configuration complete")
        
        # Validate environments
        environments = config_loader.get_environments()
        if not environments:
            print("❌ No environment configuration found")
            return False
        
        print(f"✅ Found {len(environments)} environment configurations")
        
        # Validate each environment
        for env_name, env_config in environments.items():
            required_fields = ["timeout", "retry_count", "headers"]
            missing_fields = [field for field in required_fields if field not in env_config]
            
            if missing_fields:
                print(f"❌ Environment '{env_name}' missing fields: {missing_fields}")
                return False
            
            print(f"✅ Environment '{env_name}' configuration complete")
        
        # Validate test config
        test_config = config_loader.get_test_config()
        if not test_config:
            print("❌ No test configuration found")
            return False
        
        print("✅ Test configuration complete")
        
        print(f"\n🎉 All configuration validation passed! ({current_idc.upper()})")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False


def reload_config():
    """Reload configuration from file"""
    try:
        TestEnvironment.reload_config()
        print("✅ Configuration reloaded successfully")
    except Exception as e:
        print(f"❌ Configuration reload failed: {e}")
        sys.exit(1)


def switch_idc(idc_name):
    """Switch IDC"""
    available_idcs = TestEnvironment.list_available_idcs()
    
    if idc_name not in available_idcs:
        print(f"Error: Invalid IDC '{idc_name}'")
        print(f"Valid IDCs: {list(available_idcs.keys())}")
        sys.exit(1)
    
    # Set environment variable
    os.environ["TEST_IDC"] = idc_name
    print(f"✅ Switched to {idc_name.upper()} IDC")
    print(f"Environment Variable: TEST_IDC={idc_name}")
    print(f"Description: {available_idcs[idc_name]}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Configuration Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example Usage:
  python config_manager.py list                    # List all environments
  python config_manager.py show prod               # Show prod environment configuration
  python config_manager.py show-idc aws_offline    # Show AWS offline IDC configuration
  python config_manager.py current                 # Show current environment configuration
  python config_manager.py validate                # Validate configuration files
  python config_manager.py reload                  # Reload configuration
  python config_manager.py switch-idc aws_online   # Switch to AWS online IDC
        """
    )
    
    parser.add_argument(
        "command",
        choices=["list", "show", "show-idc", "current", "validate", "reload", "switch-idc"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "name",
        nargs="?",
        help="Environment name or IDC name (for show, show-idc, switch-idc commands)"
    )
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_environments()
    elif args.command == "show":
        if not args.name:
            print("Error: show command requires environment name")
            sys.exit(1)
        show_environment(args.name)
    elif args.command == "show-idc":
        if not args.name:
            print("Error: show-idc command requires IDC name")
            sys.exit(1)
        show_idc(args.name)
    elif args.command == "current":
        show_current_environment()
    elif args.command == "validate":
        success = validate_config()
        sys.exit(0 if success else 1)
    elif args.command == "reload":
        reload_config()
    elif args.command == "switch-idc":
        if not args.name:
            print("Error: switch-idc command requires IDC name")
            sys.exit(1)
        switch_idc(args.name)


if __name__ == "__main__":
    main()
