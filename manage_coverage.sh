#!/bin/bash

# PTE Coverage Management Tool

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
    echo "PTE Coverage Management Tool"
    echo "==========================="
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --check-language    Check server language configuration"
    echo "  --collect-flask     Collect Flask application coverage"
    echo "  --run-tests TYPE    Run tests and collect coverage (TYPE: all, demo, business, real-api)"
    echo "  --generate-report TYPE  Generate coverage report (TYPE: main, flask)"
    echo "  --show-summary TYPE Show coverage summary (TYPE: main, flask)"
    echo "  --clean TYPE        Clean coverage data (TYPE: all, main, flask)"
    echo "  --open TYPE         Open coverage report in browser (TYPE: main, flask)"
    echo "  --help              Show this help information"
    echo ""
    echo "Examples:"
    echo "  $0 --check-language    # Check server language"
    echo "  $0 --run-tests demo    # Run Demo tests and collect coverage"
    echo "  $0 --run-tests all     # Run all tests and collect coverage"
    echo "  $0 --generate-report main  # Generate main project coverage report"
    echo "  $0 --generate-report flask # Generate Flask application coverage report"
    echo "  $0 --open main         # Open main project coverage report"
    echo "  $0 --open flask        # Open Flask application coverage report"
    echo ""
}

# Check server language
check_server_language() {
    print_info "Checking server language configuration..."
    python scripts/manage_coverage.py --check-language
}

# Collect Flask application coverage
collect_flask_coverage() {
    print_info "Collecting Flask application coverage..."
    python scripts/manage_coverage.py --collect-flask
}

# Run tests and collect coverage
run_tests_with_coverage() {
    local test_type=$1
    print_info "Running ${test_type} tests and collecting coverage..."
    python scripts/manage_coverage.py --run-tests "$test_type"
}

# Generate coverage report
generate_coverage_report() {
    local report_type=${1:-main}
    print_info "Generating ${report_type} coverage report..."
    python scripts/manage_coverage.py --generate-report "$report_type"
}

# Show coverage summary
show_coverage_summary() {
    local summary_type=${1:-main}
    print_info "Showing ${summary_type} coverage summary..."
    python scripts/manage_coverage.py --show-summary "$summary_type"
}

# Clean coverage data
clean_coverage_data() {
    local clean_type=${1:-all}
    print_info "Cleaning ${clean_type} coverage data..."
    python scripts/manage_coverage.py --clean "$clean_type"
}

# Open coverage report
open_coverage_report() {
    local report_type=${1:-main}
    print_info "Opening ${report_type} coverage report..."
    python scripts/manage_coverage.py --open "$report_type"
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
        --check-language)
            check_server_language
            ;;
        --collect-flask)
            collect_flask_coverage
            ;;
        --run-tests)
            if [ -z "$2" ]; then
                print_error "Please specify test type: all, demo, business, real-api"
                exit 1
            fi
            run_tests_with_coverage "$2"
            ;;
        --generate-report)
            if [ -z "$2" ]; then
                print_error "Please specify report type: main, flask"
                exit 1
            fi
            generate_coverage_report "$2"
            ;;
        --show-summary)
            if [ -z "$2" ]; then
                print_error "Please specify summary type: main, flask"
                exit 1
            fi
            show_coverage_summary "$2"
            ;;
        --clean)
            if [ -z "$2" ]; then
                print_error "Please specify clean type: all, main, flask"
                exit 1
            fi
            clean_coverage_data "$2"
            ;;
        --open)
            if [ -z "$2" ]; then
                print_error "Please specify report type: main, flask"
                exit 1
            fi
            open_coverage_report "$2"
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
