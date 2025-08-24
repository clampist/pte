#!/bin/bash

# PTE Framework Test Runner - Enhanced Version

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
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

print_command() {
    echo -e "${PURPLE}[COMMAND]${NC} $1"
}

print_header() {
    echo -e "${CYAN}$1${NC}"
}

# Show help information
show_help() {
    echo "PTE Framework Test Runner - Enhanced Version"
    echo "============================================"
    echo ""
    echo "Usage: pte [command] [options]"
    echo ""
    echo "Commands:"
    echo "  run <path>           Run tests at specified path"
    echo "  demo                 Run framework Demo tests"
    echo "  business             Run business Case tests"
    echo "  all                  Run all tests"
    echo "  real-api             Run real API tests"
    echo "  db-test              Run database connection test"
    echo "  mysql-verify         Verify Docker MySQL environment"
    echo "  help                 Show this help information"
    echo ""
    echo "Parallel Testing Options:"
    echo "  --parallel           Run tests in parallel (auto-detect CPU cores)"
    echo "  --parallel=N         Run tests with N parallel workers"
    echo "  --no-parallel        Disable parallel execution (default)"
    echo ""
    echo "Examples:"
    echo "  pte run test/department/user                    # Run all tests in user directory"
    echo "  pte run test/department/user --parallel        # Run tests in parallel"
    echo "  pte run test/department/user --parallel=4      # Run with 4 parallel workers"
    echo "  pte run test/department/user/demo_*.py         # Run all demo tests"
    echo "  pte run test/department/user/business_*.py     # Run all business tests"
    echo "  pte run test/department/user/demo_framework_structure.py::TestFrameworkStructureDemo::test_api_client_demo"
    echo "  pte run test/department/user -m \"not slow\"    # Run tests with pytest markers"
    echo "  pte run test/department/user -k \"api\"         # Run tests matching pattern"
    echo "  pte run test/department/user -v --tb=short     # Run with pytest options"
    echo "  pte demo                                          # Run demo tests"
    echo "  pte business                                      # Run business tests"
    echo "  pte all                                           # Run all tests"
    echo ""
    echo "Pytest Options:"
    echo "  All standard pytest options are supported:"
    echo "  -v, --verbose       Increase verbosity"
    echo "  -k EXPRESSION       Only run tests matching the substring expression"
    echo "  -m MARKERS          Only run tests matching given mark expression"
    echo "  --tb=style          Traceback style (auto/long/short/line/native/no)"
    echo "  --maxfail=num       Exit after first num failures or errors"
    echo "  --lf, --last-failed Run only the tests that failed at the last run"
    echo "  --ff, --failed-first Run all tests but run the last failures first"
    echo "  -x, --exitfirst     Exit instantly on first error or failed test"
    echo "  --pdb               Start the interactive Python debugger on errors"
    echo "  --durations=N       Show N slowest test durations (N=0 for all)"
    echo ""
    echo "Parallel Testing Notes:"
    echo "  - Use @pytest.mark.parallel to mark tests safe for parallel execution"
    echo "  - Use @pytest.mark.no_parallel to mark tests that should not run in parallel"
    echo "  - Tests without parallel markers will be auto-detected for safety"
    echo "  - Database tests and tests with shared state should use no_parallel marker"
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

# Run tests with pytest
run_pytest() {
    local test_path="$1"
    shift  # Remove first argument, keep remaining as pytest options
    
    print_header "🚀 Running PTE Framework Tests"
    print_info "Test path: $test_path"
    
    # Parse parallel options
    local parallel_workers=""
    local pytest_options=()
    
    # Process arguments to extract parallel options
    while [ $# -gt 0 ]; do
        case "$1" in
            --parallel)
                # Auto-detect CPU cores
                if command -v nproc >/dev/null 2>&1; then
                    parallel_workers="$(nproc)"
                elif command -v sysctl >/dev/null 2>&1; then
                    parallel_workers="$(sysctl -n hw.ncpu)"
                else
                    parallel_workers="4"  # Default fallback
                fi
                print_info "Auto-detected parallel workers: $parallel_workers"
                shift
                ;;
            --parallel=*)
                parallel_workers="${1#--parallel=}"
                print_info "Using parallel workers: $parallel_workers"
                shift
                ;;
            --no-parallel)
                parallel_workers=""
                print_info "Parallel execution disabled"
                shift
                ;;
            *)
                pytest_options+=("$1")
                shift
                ;;
        esac
    done
    
    # Handle different path types and validate existence
    local actual_path="$test_path"
    
    # Check if it's a pattern with wildcards
    if [[ "$test_path" == *"*"* ]] || [[ "$test_path" == *"?"* ]]; then
        print_info "Path type: Pattern (pytest will expand wildcards)"
        # Check if pattern matches any files
        if ! ls $test_path >/dev/null 2>&1; then
            print_error "No files match pattern: $test_path"
            exit 1
        fi
    elif [ -d "$test_path" ]; then
        print_info "Path type: Directory (converting to wildcard pattern for better discovery)"
        # Convert directory to wildcard pattern for better test discovery
        actual_path="$test_path/*.py"
    elif [ -f "$test_path" ]; then
        print_info "Path type: File"
    elif [[ "$test_path" == *"::"* ]]; then
        print_info "Path type: Specific test (pytest will handle)"
        # Extract file path from test specification
        local file_path="${test_path%%::*}"
        if [ ! -f "$file_path" ]; then
            print_error "Test file does not exist: $file_path"
            exit 1
        fi
    else
        print_error "Test path does not exist: $test_path"
        exit 1
    fi
    
    if [ ${#pytest_options[@]} -gt 0 ]; then
        print_info "Pytest options: ${pytest_options[*]}"
    fi
    
    # Build and execute pytest command
    if [[ "$actual_path" == *"*"* ]] || [[ "$actual_path" == *"?"* ]]; then
        # For patterns, let shell expand the wildcards
        local cmd="pytest $actual_path"
        
        # Add parallel option if specified
        if [ -n "$parallel_workers" ]; then
            cmd="$cmd -n $parallel_workers"
            print_info "Running tests in parallel with $parallel_workers workers"
        fi
        
        # Add pytest options if provided
        if [ ${#pytest_options[@]} -gt 0 ]; then
            cmd="$cmd ${pytest_options[*]}"
        fi
        
        # Add default options if no specific options provided
        if [ ${#pytest_options[@]} -eq 0 ]; then
            cmd="$cmd -v"
        fi
        
        print_command "Executing: $cmd"
        echo ""
        eval "$cmd"
    else
        # For regular paths, quote to handle spaces
        local cmd="pytest \"$actual_path\""
        
        # Add parallel option if specified
        if [ -n "$parallel_workers" ]; then
            cmd="$cmd -n $parallel_workers"
            print_info "Running tests in parallel with $parallel_workers workers"
        fi
        
        # Add pytest options if provided
        if [ ${#pytest_options[@]} -gt 0 ]; then
            cmd="$cmd ${pytest_options[*]}"
        fi
        
        # Add default options if no specific options provided
        if [ ${#pytest_options[@]} -eq 0 ]; then
            cmd="$cmd -v"
        fi
        
        print_command "Executing: $cmd"
        echo ""
        
        # Execute pytest
        eval "$cmd"
    fi
    
    local exit_code=$?
    
    echo ""
    if [ $exit_code -eq 0 ]; then
        print_success "Tests completed successfully"
    else
        print_error "Tests failed with exit code: $exit_code"
    fi
    
    return $exit_code
}

# Run framework Demo tests
run_demo_tests() {
    local parallel_workers=""
    
    # Check for parallel options
    while [ $# -gt 0 ]; do
        case "$1" in
            --parallel)
                if command -v nproc >/dev/null 2>&1; then
                    parallel_workers="$(nproc)"
                elif command -v sysctl >/dev/null 2>&1; then
                    parallel_workers="$(sysctl -n hw.ncpu)"
                else
                    parallel_workers="4"
                fi
                print_info "Auto-detected parallel workers: $parallel_workers"
                shift
                ;;
            --parallel=*)
                parallel_workers="${1#--parallel=}"
                print_info "Using parallel workers: $parallel_workers"
                shift
                ;;
            --no-parallel)
                parallel_workers=""
                print_info "Parallel execution disabled"
                shift
                ;;
            *)
                shift
                ;;
        esac
    done
    
    print_header "🚀 Running PTE Framework Demo Tests"
    
    if [ -n "$parallel_workers" ]; then
        print_info "Running demo tests in parallel with $parallel_workers workers"
        python scripts/run_tests_by_category.py --demo --parallel=$parallel_workers
    else
        python scripts/run_tests_by_category.py --demo
    fi
    
    print_success "Framework Demo tests completed"
}

# Run business Case tests
run_business_tests() {
    local parallel_workers=""
    
    # Check for parallel options
    while [ $# -gt 0 ]; do
        case "$1" in
            --parallel)
                if command -v nproc >/dev/null 2>&1; then
                    parallel_workers="$(nproc)"
                elif command -v sysctl >/dev/null 2>&1; then
                    parallel_workers="$(sysctl -n hw.ncpu)"
                else
                    parallel_workers="4"
                fi
                print_info "Auto-detected parallel workers: $parallel_workers"
                shift
                ;;
            --parallel=*)
                parallel_workers="${1#--parallel=}"
                print_info "Using parallel workers: $parallel_workers"
                shift
                ;;
            --no-parallel)
                parallel_workers=""
                print_info "Parallel execution disabled"
                shift
                ;;
            *)
                shift
                ;;
        esac
    done
    
    print_header "💼 Running Business Case Tests"
    
    if [ -n "$parallel_workers" ]; then
        print_info "Running business tests in parallel with $parallel_workers workers"
        python scripts/run_tests_by_category.py --business --parallel=$parallel_workers
    else
        python scripts/run_tests_by_category.py --business
    fi
    
    print_success "Business Case tests completed"
}

# Run real API tests
run_real_api_tests() {
    print_header "🌐 Running Real API Tests"
    
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
    pytest test/department/user/business_real_api_tests.py -v
    print_success "Real API tests completed"
}

# Run all tests
run_all_tests() {
    local parallel_workers=""
    
    # Check for parallel options
    while [ $# -gt 0 ]; do
        case "$1" in
            --parallel)
                if command -v nproc >/dev/null 2>&1; then
                    parallel_workers="$(nproc)"
                elif command -v sysctl >/dev/null 2>&1; then
                    parallel_workers="$(sysctl -n hw.ncpu)"
                else
                    parallel_workers="4"
                fi
                print_info "Auto-detected parallel workers: $parallel_workers"
                shift
                ;;
            --parallel=*)
                parallel_workers="${1#--parallel=}"
                print_info "Using parallel workers: $parallel_workers"
                shift
                ;;
            --no-parallel)
                parallel_workers=""
                print_info "Parallel execution disabled"
                shift
                ;;
            *)
                shift
                ;;
        esac
    done
    
    print_header "🎯 Running All PTE Framework Tests"
    
    if [ -n "$parallel_workers" ]; then
        print_info "Running all tests in parallel with $parallel_workers workers"
        python scripts/run_tests_by_category.py --all --parallel=$parallel_workers
    else
        python scripts/run_tests_by_category.py --all
    fi
    
    print_success "All tests completed"
}

# Run database connection test
run_db_test() {
    print_header "🗄️ Running Database Connection Test"
    python scripts/test_db_connection.py local_test local
    print_success "Database connection test completed"
}

# Verify Docker MySQL environment
verify_mysql() {
    print_header "🐳 Verifying Docker MySQL Environment"
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

    # Process command
    case "$1" in
        run)
            if [ $# -lt 2 ]; then
                print_error "No test path specified for 'run' command"
                show_help
                exit 1
            fi
            shift  # Remove 'run' command
            local test_path="$1"
            shift  # Remove test path, keep remaining as pytest options
            run_pytest "$test_path" "$@"
            ;;
        demo)
            shift  # Remove 'demo' command
            run_demo_tests "$@"
            ;;
        business)
            shift  # Remove 'business' command
            run_business_tests "$@"
            ;;
        real-api)
            run_real_api_tests
            ;;
        all)
            shift  # Remove 'all' command
            run_all_tests "$@"
            ;;
        db-test)
            run_db_test
            ;;
        mysql-verify)
            verify_mysql
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
