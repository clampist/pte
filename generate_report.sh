#!/bin/bash

# PTE Framework Allure Report Generator

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
    echo "PTE Framework Allure Report Generator"
    echo "===================================="
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --generate      Generate Allure report"
    echo "  --open          Open Allure report"
    echo "  --serve         Start Allure report server"
    echo "  --list          List available reports"
    echo "  --install       Install Allure command line tool"
    echo "  --clean         Clean old reports"
    echo "  --help          Show this help information"
    echo ""
    echo "Examples:"
    echo "  $0 --generate   # Generate Allure report"
    echo "  $0 --open       # Open Allure report"
    echo "  $0 --serve      # Start report server"
    echo "  $0 --install    # Install Allure tool"
    echo ""
}

# Setup environment
setup_environment() {
    print_info "Setting up environment..."
    
    # Ensure Python environment is activated
    if command -v pyenv >/dev/null 2>&1; then
        print_info "Activating Python environment..."
        eval "$(pyenv init -)"
        pyenv activate pte
        print_success "Python environment activation completed"
    fi
    
    print_success "Environment setup completed"
}

# Generate report
generate_report() {
    print_info "Generating Allure report..."
    python scripts/generate_allure_report.py --generate
    print_success "Allure report generation completed"
}

# Open report
open_report() {
    print_info "Opening Allure report..."
    python scripts/generate_allure_report.py --open
}

# Start report server
serve_report() {
    print_info "Starting Allure report server..."
    python scripts/generate_allure_report.py --serve
}

# List reports
list_reports() {
    print_info "Listing available reports..."
    python scripts/generate_allure_report.py --list
}

# Install Allure
install_allure() {
    print_info "Installing Allure command line tool..."
    python scripts/generate_allure_report.py --install
}

# Clean reports
clean_reports() {
    print_info "Cleaning old reports..."
    
    if [ -d "./reports/allure-results" ]; then
        rm -rf ./reports/allure-results/*
        print_success "Results directory cleanup completed"
    fi
    
    if [ -d "./reports/allure-reports" ]; then
        rm -rf ./reports/allure-reports/*
        print_success "Reports directory cleanup completed"
    fi
}

# Run tests and generate report
run_tests_and_report() {
    print_info "Running tests and generating report..."
    
    # Run all tests
    ./run_tests.sh --all
    
    # Generate report
    generate_report
    
    print_success "Test execution and report generation completed"
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
        --generate)
            generate_report
            ;;
        --open)
            open_report
            ;;
        --serve)
            serve_report
            ;;
        --list)
            list_reports
            ;;
        --install)
            install_allure
            ;;
        --clean)
            clean_reports
            ;;
        --run-and-report)
            run_tests_and_report
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
