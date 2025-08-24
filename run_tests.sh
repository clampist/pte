#!/bin/bash

# PTE Framework Test Runner

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    echo "PTE Framework Test Runner"
    echo "========================"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --demo          Run framework Demo tests"
    echo "  --business      Run business Case tests"
    echo "  --real-api      Run real API tests (requires Flask app to be started first)"
    echo "  --all           Run all tests"
    echo "  --db-test       Run database connection test"
    echo "  --mysql-verify  Verify Docker MySQL environment"
    echo "  --help          Show this help information"
    echo ""
    echo "Examples:"
    echo "  $0 --demo       # Run framework Demo tests"
    echo "  $0 --business   # Run business Case tests"
    echo "  $0 --real-api   # Run real API tests"
    echo ""
    echo "Note: Before running real API tests, please start Flask app using ./start_flask.sh"
    echo ""
}

# Setup test environment
setup_environment() {
    print_info "Setting up test environment..."
    export TEST_IDC=local_test
    export TEST_ENV=local
    
    # Ensure Python environment is activated
    if command -v pyenv >/dev/null 2>&1; then
        print_info "Activating Python environment..."
        eval "$(pyenv init -)"
        pyenv activate pte
        print_success "Python environment activation completed"
    fi
    
    print_success "Test environment setup completed"
}

# Run framework Demo tests
run_demo_tests() {
    print_info "Running framework Demo tests..."
    python scripts/run_tests_by_category.py --demo
    print_success "Framework Demo tests completed"
}

# Run business Case tests
run_business_tests() {
    print_info "Running business Case tests..."
    python scripts/run_tests_by_category.py --business
    print_success "Business Case tests completed"
}

# Run real API tests
run_real_api_tests() {
    print_info "Running real API tests..."
    
    # Check if target application is running
    # Check if target application is running
    TARGET_APP_HOST=${TARGET_APP_HOST:-localhost}
    TARGET_APP_PORT=${TARGET_APP_PORT:-5001}
    HEALTH_URL="http://${TARGET_APP_HOST}:${TARGET_APP_PORT}/api/health"
    
    if ! curl -s "$HEALTH_URL" > /dev/null 2>&1; then
        print_error "Target application is not running!"
        print_info "Please start target application first:"
        print_info "cd \$PTE_TARGET_ROOT && ./start_flask.sh"
        print_info "Or set environment variable: export PTE_TARGET_ROOT=/path/to/target/app"
        exit 1
    fi
    
    # Run real API tests
    pytest test/department/user/test_business_real_api_tests.py -v
    print_success "Real API tests completed"
}

# Run all tests
run_all_tests() {
    print_info "Running all tests..."
    python scripts/run_tests_by_category.py --all
    print_success "All tests completed"
}

# Run database connection test
run_db_test() {
    print_info "Running database connection test..."
    python scripts/test_db_connection.py local_test local
    print_success "Database connection test completed"
}

# Verify Docker MySQL environment
verify_mysql() {
    print_info "Verifying Docker MySQL environment..."
    python scripts/test_mysql_docker.py
    print_success "Docker MySQL environment verification completed"
}

# Main function
main() {
    # Check parameters
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi

    # Setup environment
    setup_environment

    # Process parameters
    case "$1" in
        --demo)
            run_demo_tests
            ;;
        --business)
            run_business_tests
            ;;
        --real-api)
            run_real_api_tests
            ;;
        --all)
            run_all_tests
            ;;
        --db-test)
            run_db_test
            ;;
        --mysql-verify)
            verify_mysql
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
