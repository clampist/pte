#!/usr/bin/env python3
"""
Allure Report Generator
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


def check_allure_installed():
    """Check if Allure is installed"""
    try:
        result = subprocess.run(['allure', '--version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_allure():
    """Install Allure command line tool"""
    print("📦 Installing Allure command line tool...")
    
    # Check operating system
    import platform
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        try:
            subprocess.run(['brew', 'install', 'allure'], check=True)
            print("✅ Allure installation successful")
            return True
        except subprocess.CalledProcessError:
            print("❌ Installation via Homebrew failed, please install manually")
            return False
    elif system == "linux":
        try:
            # Install using snap
            subprocess.run(['sudo', 'snap', 'install', 'allure'], check=True)
            print("✅ Allure installation successful")
            return True
        except subprocess.CalledProcessError:
            print("❌ Installation via snap failed, please install manually")
            return False
    else:
        print("❌ Unsupported operating system, please install Allure manually")
        return False


def generate_report(results_dir, report_dir, clean=True):
    """Generate Allure report"""
    print(f"📊 Generating Allure report...")
    print(f"   Results directory: {results_dir}")
    print(f"   Report directory: {report_dir}")
    
    # Check if results directory exists
    if not os.path.exists(results_dir):
        print(f"❌ Results directory does not exist: {results_dir}")
        return False
    
    # Clean old report directory
    if clean and os.path.exists(report_dir):
        import shutil
        shutil.rmtree(report_dir)
        print(f"🧹 Cleaned old report directory: {report_dir}")
    
    # Generate report
    try:
        cmd = ['allure', 'generate', results_dir, '-o', report_dir, '--clean']
        print(f"Executing command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Allure report generation successful")
            return True
        else:
            print(f"❌ Allure report generation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return False


def open_report(report_dir):
    """Open Allure report"""
    if not os.path.exists(report_dir):
        print(f"❌ Report directory does not exist: {report_dir}")
        return False
    
    try:
        # Start Allure server
        cmd = ['allure', 'open', report_dir]
        print(f"🌐 Starting Allure report server...")
        print(f"Executing command: {' '.join(cmd)}")
        
        subprocess.run(cmd)
        return True
        
    except Exception as e:
        print(f"❌ Error opening report: {e}")
        return False


def serve_report(report_dir, host='localhost', port=8080):
    """Start Allure report server"""
    if not os.path.exists(report_dir):
        print(f"❌ Report directory does not exist: {report_dir}")
        return False
    
    try:
        cmd = ['allure', 'serve', report_dir, '--host', host, '--port', str(port)]
        print(f"🌐 Starting Allure report server...")
        print(f"   Address: http://{host}:{port}")
        print(f"Executing command: {' '.join(cmd)}")
        
        subprocess.run(cmd)
        return True
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False


def list_reports(reports_dir):
    """List available reports"""
    if not os.path.exists(reports_dir):
        print(f"❌ Report directory does not exist: {reports_dir}")
        return
    
    print(f"📋 Available reports list ({reports_dir}):")
    
    for item in os.listdir(reports_dir):
        item_path = os.path.join(reports_dir, item)
        if os.path.isdir(item_path):
            # Get report information
            try:
                stats_file = os.path.join(item_path, 'widgets', 'summary.json')
                if os.path.exists(stats_file):
                    import json
                    with open(stats_file, 'r') as f:
                        stats = json.load(f)
                    
                    total = stats.get('statistic', {}).get('total', 0)
                    passed = stats.get('statistic', {}).get('passed', 0)
                    failed = stats.get('statistic', {}).get('failed', 0)
                    
                    print(f"  📊 {item}: Total={total}, Passed={passed}, Failed={failed}")
                else:
                    print(f"  📊 {item}: Report generation in progress...")
            except:
                print(f"  📊 {item}: Failed to read report information")


def main():
    parser = argparse.ArgumentParser(description='Allure Test Report Generator')
    parser.add_argument('--generate', action='store_true', 
                       help='Generate Allure report')
    parser.add_argument('--open', action='store_true',
                       help='Open Allure report')
    parser.add_argument('--serve', action='store_true',
                       help='Start Allure report server')
    parser.add_argument('--list', action='store_true',
                       help='List available reports')
    parser.add_argument('--install', action='store_true',
                       help='Install Allure command line tool')
    parser.add_argument('--results-dir', default='./reports/allure-results',
                       help='Allure results directory (default: ./reports/allure-results)')
    parser.add_argument('--report-dir', default='./reports/allure-reports',
                       help='Allure report directory (default: ./reports/allure-reports)')
    parser.add_argument('--host', default='localhost',
                       help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=8080,
                       help='Server port (default: 8080)')
    parser.add_argument('--no-clean', action='store_true',
                       help='Do not clean old reports')
    
    args = parser.parse_args()
    
    # Check if Allure is installed
    if not check_allure_installed():
        print("❌ Allure command line tool not installed")
        if args.install:
            if install_allure():
                print("✅ Allure installation completed")
            else:
                print("❌ Allure installation failed")
                sys.exit(1)
        else:
            print("💡 Please run: python scripts/generate_allure_report.py --install")
            sys.exit(1)
    
    # Process commands
    if args.generate:
        generate_report(args.results_dir, args.report_dir, not args.no_clean)
    
    elif args.open:
        open_report(args.report_dir)
    
    elif args.serve:
        serve_report(args.report_dir, args.host, args.port)
    
    elif args.list:
        list_reports(args.report_dir)
    
    elif args.install:
        print("✅ Allure is installed")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
