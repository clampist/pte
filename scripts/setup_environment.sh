#!/bin/bash

# PTE Environment Setup Script
# Setup environment variables for PTE framework

set -e

# Color definitions
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Show help information
show_help() {
    echo "PTE Environment Setup Script"
    echo "============================"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --set-target PATH    Set target application root path"
    echo "  --set-host HOST      Set target application host (default: localhost)"
    echo "  --set-port PORT      Set target application port (default: 5001)"
    echo "  --show               Show current environment configuration"
    echo "  --validate           Validate environment configuration"
    echo "  --help               Show this help information"
    echo ""
    echo "Examples:"
    echo "  $0 --set-target /path/to/target/app"
    echo "  $0 --set-host 192.168.1.100"
    echo "  $0 --set-port 8080"
    echo "  $0 --show"
    echo "  $0 --validate"
    echo ""
}

# Set target application root path
set_target_root() {
    local target_path="$1"
    
    if [ -z "$target_path" ]; then
        print_error "Target path is required"
        exit 1
    fi
    
    if [ ! -d "$target_path" ]; then
        print_error "Target path does not exist: $target_path"
        exit 1
    fi
    
    # Check if flask_app directory exists
    if [ ! -d "$target_path/flask_app" ]; then
        print_warning "Flask app directory not found: $target_path/flask_app"
        print_info "This might be expected if the target app has a different structure"
    fi
    
    export PTE_TARGET_ROOT="$target_path"
    print_success "Set PTE_TARGET_ROOT to: $target_path"
    
    # Save to shell profile
    save_to_profile "PTE_TARGET_ROOT" "$target_path"
}

# Set target application host
set_target_host() {
    local host="$1"
    
    if [ -z "$host" ]; then
        print_error "Host is required"
        exit 1
    fi
    
    export TARGET_APP_HOST="$host"
    print_success "Set TARGET_APP_HOST to: $host"
    
    # Save to shell profile
    save_to_profile "TARGET_APP_HOST" "$host"
}

# Set target application port
set_target_port() {
    local port="$1"
    
    if [ -z "$port" ]; then
        print_error "Port is required"
        exit 1
    fi
    
    # Validate port number
    if ! [[ "$port" =~ ^[0-9]+$ ]] || [ "$port" -lt 1 ] || [ "$port" -gt 65535 ]; then
        print_error "Invalid port number: $port (must be 1-65535)"
        exit 1
    fi
    
    export TARGET_APP_PORT="$port"
    print_success "Set TARGET_APP_PORT to: $port"
    
    # Save to shell profile
    save_to_profile "TARGET_APP_PORT" "$port"
}

# Save environment variable to shell profile
save_to_profile() {
    local var_name="$1"
    local var_value="$2"
    local profile_file=""
    
    # Determine shell profile file
    if [ -n "$ZSH_VERSION" ]; then
        profile_file="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        profile_file="$HOME/.bashrc"
    else
        profile_file="$HOME/.profile"
    fi
    
    # Remove existing export line
    if [ -f "$profile_file" ]; then
        sed -i.bak "/export $var_name=/d" "$profile_file"
    fi
    
    # Add new export line
    echo "export $var_name=\"$var_value\"" >> "$profile_file"
    
    print_info "Saved $var_name to $profile_file"
    print_info "Please run 'source $profile_file' to apply changes"
}

# Show current environment configuration
show_config() {
    echo "=== Current Environment Configuration ==="
    echo "PTE_TARGET_ROOT: ${PTE_TARGET_ROOT:-Not set (using default)}"
    echo "TARGET_APP_HOST: ${TARGET_APP_HOST:-localhost}"
    echo "TARGET_APP_PORT: ${TARGET_APP_PORT:-5001}"
    echo "TEST_IDC: ${TEST_IDC:-local_test}"
    echo "TEST_ENV: ${TEST_ENV:-local}"
    echo "========================================"
    
    # Show calculated paths
    local target_root="${PTE_TARGET_ROOT:-$(pwd)/../pte_target}"
    echo ""
    echo "=== Calculated Paths ==="
    echo "Target App Root: $target_root"
    echo "Target App Flask Dir: $target_root/flask_app"
    echo "Health Check URL: http://${TARGET_APP_HOST:-localhost}:${TARGET_APP_PORT:-5001}/api/health"
    echo "========================"
}

# Validate environment configuration
validate_config() {
    print_info "Validating environment configuration..."
    
    local target_root="${PTE_TARGET_ROOT:-$(pwd)/../pte_target}"
    local flask_dir="$target_root/flask_app"
    
    # Check target root
    if [ ! -d "$target_root" ]; then
        print_error "Target app root does not exist: $target_root"
        print_info "Set it using: $0 --set-target /path/to/target/app"
        return 1
    else
        print_success "Target app root exists: $target_root"
    fi
    
    # Check flask app directory
    if [ ! -d "$flask_dir" ]; then
        print_warning "Flask app directory not found: $flask_dir"
        print_info "This might be expected if the target app has a different structure"
    else
        print_success "Flask app directory exists: $flask_dir"
    fi
    
    # Check if target app is running
    local health_url="http://${TARGET_APP_HOST:-localhost}:${TARGET_APP_PORT:-5001}/api/health"
    if curl -s "$health_url" > /dev/null 2>&1; then
        print_success "Target application is running: $health_url"
    else
        print_warning "Target application is not running: $health_url"
        print_info "Start it using: cd $target_root && ./start_flask.sh"
    fi
    
    print_success "Environment validation completed"
}

# Main function
main() {
    # Check parameters
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi
    
    # Process parameters
    case "$1" in
        --set-target)
            set_target_root "$2"
            ;;
        --set-host)
            set_target_host "$2"
            ;;
        --set-port)
            set_target_port "$2"
            ;;
        --show)
            show_config
            ;;
        --validate)
            validate_config
            ;;
        --help)
            show_help
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
