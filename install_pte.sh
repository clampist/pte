#!/bin/bash

# PTE Framework Installation Script
# This script installs the pte command to make it available system-wide

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
    echo "PTE Framework Installation Script"
    echo "================================="
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --install            Install pte command to system PATH"
    echo "  --uninstall          Remove pte command from system PATH"
    echo "  --status             Show installation status"
    echo "  --help               Show this help information"
    echo ""
    echo "Examples:"
    echo "  $0 --install         # Install pte command"
    echo "  $0 --uninstall       # Remove pte command"
    echo "  $0 --status          # Check installation status"
    echo ""
}

# Get the directory where this script is located
get_script_dir() {
    cd "$(dirname "${BASH_SOURCE[0]}")" && pwd
}

# Install pte command
install_pte() {
    print_info "Installing PTE Framework command..."
    
    local script_dir=$(get_script_dir)
    local user_bin_dir="$HOME/.local/bin"
    
    # Create user bin directory if it doesn't exist
    if [ ! -d "$user_bin_dir" ]; then
        print_info "Creating directory: $user_bin_dir"
        mkdir -p "$user_bin_dir"
    fi
    
    # Create symbolic links
    print_info "Creating symbolic links..."
    ln -sf "$script_dir/pte" "$user_bin_dir/pte"
    ln -sf "$script_dir/pte.sh" "$user_bin_dir/pte.sh"
    
    # Add to PATH if not already there
    local profile_file=""
    if [ -n "$ZSH_VERSION" ]; then
        profile_file="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        profile_file="$HOME/.bashrc"
    else
        profile_file="$HOME/.profile"
    fi
    
    if [ -f "$profile_file" ]; then
        if ! grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$profile_file"; then
            print_info "Adding PATH to $profile_file"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$profile_file"
        else
            print_info "PATH already configured in $profile_file"
        fi
    fi
    
    print_success "PTE Framework installed successfully!"
    print_info "Please run 'source $profile_file' or restart your terminal to use 'pte' command"
    print_info "You can now use: pte all --parallel"
}

# Uninstall pte command
uninstall_pte() {
    print_info "Uninstalling PTE Framework command..."
    
    local user_bin_dir="$HOME/.local/bin"
    
    # Remove symbolic links
    if [ -L "$user_bin_dir/pte" ]; then
        rm "$user_bin_dir/pte"
        print_info "Removed: $user_bin_dir/pte"
    fi
    
    if [ -L "$user_bin_dir/pte.sh" ]; then
        rm "$user_bin_dir/pte.sh"
        print_info "Removed: $user_bin_dir/pte.sh"
    fi
    
    # Remove from PATH
    local profile_file=""
    if [ -n "$ZSH_VERSION" ]; then
        profile_file="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        profile_file="$HOME/.bashrc"
    else
        profile_file="$HOME/.profile"
    fi
    
    if [ -f "$profile_file" ]; then
        if grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$profile_file"; then
            print_info "Removing PATH from $profile_file"
            sed -i.bak '/export PATH="$HOME\/.local\/bin:$PATH"/d' "$profile_file"
        fi
    fi
    
    print_success "PTE Framework uninstalled successfully!"
    print_info "Please run 'source $profile_file' or restart your terminal"
}

# Show installation status
show_status() {
    echo "=== PTE Framework Installation Status ==="
    
    local user_bin_dir="$HOME/.local/bin"
    
    # Check if pte command is available
    if command -v pte >/dev/null 2>&1; then
        local pte_path=$(which pte)
        print_success "pte command found at: $pte_path"
    else
        print_error "pte command not found in PATH"
    fi
    
    # Check symbolic links
    echo ""
    echo "Symbolic Links:"
    if [ -L "$user_bin_dir/pte" ]; then
        local target=$(readlink "$user_bin_dir/pte")
        print_success "pte -> $target"
    else
        print_error "pte link not found"
    fi
    
    if [ -L "$user_bin_dir/pte.sh" ]; then
        local target=$(readlink "$user_bin_dir/pte.sh")
        print_success "pte.sh -> $target"
    else
        print_error "pte.sh link not found"
    fi
    
    # Check PATH configuration
    echo ""
    echo "PATH Configuration:"
    local profile_file=""
    if [ -n "$ZSH_VERSION" ]; then
        profile_file="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        profile_file="$HOME/.bashrc"
    else
        profile_file="$HOME/.profile"
    fi
    
    if [ -f "$profile_file" ]; then
        if grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$profile_file"; then
            print_success "PATH configured in $profile_file"
        else
            print_error "PATH not configured in $profile_file"
        fi
    else
        print_error "Profile file not found: $profile_file"
    fi
    
    echo "========================================"
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
        --install)
            install_pte
            ;;
        --uninstall)
            uninstall_pte
            ;;
        --status)
            show_status
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
