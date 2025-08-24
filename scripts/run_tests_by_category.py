#!/usr/bin/env python3
"""
PTE Framework Test Runner by Category
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_pytest(test_path, verbose=True, markers=None, parallel_workers=None):
    """Run pytest tests"""
    cmd = ['pytest', test_path]
    
    if verbose:
        cmd.append('-v')
    
    if markers:
        cmd.extend(['-m', markers])
    
    if parallel_workers:
        cmd.extend(['-n', str(parallel_workers)])
        print(f"Running tests in parallel with {parallel_workers} workers")
    
    print(f"Executing command: {' '.join(cmd)}")
    print("-" * 50)
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode


def run_demo_tests(verbose=True, parallel_workers=None):
    """Run framework Demo tests"""
    print("🚀 Running PTE Framework Demo Tests")
    print("=" * 50)
    
    demo_tests = [
        'test/department/user/demo_framework_structure.py',
        'test/department/user/demo_config_management.py',
        'test/department/user/demo_database_features.py',
        'test/department/user/demo_parallel_testing.py'
    ]
    
    total_failed = 0
    
    for test_file in demo_tests:
        if os.path.exists(test_file):
            print(f"\n📋 Running: {test_file}")
            failed = run_pytest(test_file, verbose, parallel_workers=parallel_workers)
            total_failed += failed
        else:
            print(f"❌ File does not exist: {test_file}")
            total_failed += 1
    
    return total_failed


def run_business_tests(verbose=True, parallel_workers=None):
    """Run business Case tests"""
    print("💼 Running Business Case Tests")
    print("=" * 50)
    
    business_tests = [
        'test/department/user/business_user_management.py'
    ]
    
    total_failed = 0
    
    for test_file in business_tests:
        if os.path.exists(test_file):
            print(f"\n📋 Running: {test_file}")
            failed = run_pytest(test_file, verbose, parallel_workers=parallel_workers)
            total_failed += failed
        else:
            print(f"❌ File does not exist: {test_file}")
            total_failed += 1
    
    return total_failed


def run_all_tests(verbose=True, parallel_workers=None):
    """Run all tests"""
    print("🎯 Running All PTE Framework Tests")
    print("=" * 50)
    
    # Run Demo tests
    demo_failed = run_demo_tests(verbose, parallel_workers)
    
    print("\n" + "=" * 50)
    
    # Run business tests
    business_failed = run_business_tests(verbose, parallel_workers)
    
    total_failed = demo_failed + business_failed
    
    print("\n" + "=" * 50)
    print(f"📊 Test Summary:")
    print(f"   Demo tests failed: {demo_failed}")
    print(f"   Business tests failed: {business_failed}")
    print(f"   Total failures: {total_failed}")
    
    return total_failed


def run_specific_test(test_file, verbose=True, parallel_workers=None):
    """Run specific test file"""
    print(f"🎯 Running specific test: {test_file}")
    print("=" * 50)
    
    if os.path.exists(test_file):
        failed = run_pytest(test_file, verbose, parallel_workers=parallel_workers)
        return failed
    else:
        print(f"❌ File does not exist: {test_file}")
        return 1


def list_available_tests():
    """List available test files"""
    print("📋 Available Test Files")
    print("=" * 50)
    
    test_dir = Path('test/department/user')
    
    if test_dir.exists():
        print("\n🚀 Framework Demo Tests:")
        for test_file in test_dir.glob('demo_*.py'):
            print(f"   - {test_file}")
        
        print("\n💼 Business Case Tests:")
        for test_file in test_dir.glob('business_*.py'):
            print(f"   - {test_file}")
        
        print("\n📚 Other Files:")
        for test_file in test_dir.glob('*.py'):
            if not test_file.name.startswith(('demo_', 'business_')):
                print(f"   - {test_file}")
    else:
        print(f"❌ Test directory does not exist: {test_dir}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='PTE Framework Test Runner')
    parser.add_argument('--demo', action='store_true', help='Run framework Demo tests')
    parser.add_argument('--business', action='store_true', help='Run business Case tests')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--file', type=str, help='Run specific test file')
    parser.add_argument('--list', action='store_true', help='List available test files')
    parser.add_argument('--quiet', action='store_true', help='Quiet mode, do not show detailed output')
    parser.add_argument('--parallel', type=int, help='Number of parallel workers for test execution')
    
    args = parser.parse_args()
    
    verbose = not args.quiet
    parallel_workers = args.parallel
    
    # Set test environment
    os.environ['TEST_IDC'] = 'local_test'
    os.environ['TEST_ENV'] = 'local'
    
    if args.list:
        list_available_tests()
        return 0
    
    elif args.demo:
        failed = run_demo_tests(verbose, parallel_workers)
        return failed
    
    elif args.business:
        failed = run_business_tests(verbose, parallel_workers)
        return failed
    
    elif args.all:
        failed = run_all_tests(verbose, parallel_workers)
        return failed
    
    elif args.file:
        failed = run_specific_test(args.file, verbose, parallel_workers)
        return failed
    
    else:
        # Default to running all tests
        print("🎯 Default: Running all PTE Framework tests")
        failed = run_all_tests(verbose, parallel_workers)
        return failed


if __name__ == "__main__":
    sys.exit(main())
