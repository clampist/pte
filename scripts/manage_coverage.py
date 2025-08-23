#!/usr/bin/env python3
"""
Coverage Management Script
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Dict, Any, Optional


class CoverageManager:
    """Coverage management for different environments"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.reports_dir = self.project_root / "reports"
        self.coverage_dir = self.reports_dir / "coverage-html"
        self.coverage_xml = self.reports_dir / "coverage.xml"
        self.coverage_data = self.project_root / ".coverage"
        
        # Import environment configuration
        sys.path.insert(0, str(self.project_root))
        from config.environment import get_target_app_flask_dir
        
        # Flask app coverage paths (now in separate project)
        self.flask_app_dir = get_target_app_flask_dir()
        self.flask_coverage_dir = self.reports_dir / "flask-coverage-html"
        self.flask_coverage_xml = self.reports_dir / "flask-coverage.xml"
        self.flask_coverage_data = self.flask_app_dir / ".coverage"
        
        # Ensure reports directory exists
        self.reports_dir.mkdir(exist_ok=True)
    
    def check_server_language(self) -> str:
        """Check server language from configuration"""
        try:
            # Import here to avoid circular imports
            sys.path.insert(0, str(self.project_root))
            from config.settings import TestEnvironment
            return TestEnvironment.get_server_language()
        except ImportError:
            return "python"  # Default to python
    
    def check_flask_environment(self) -> bool:
        """Check if Flask environment exists"""
        try:
            result = subprocess.run(['pyenv', 'virtualenvs'], 
                                  capture_output=True, text=True)
            return 'flask' in result.stdout
        except:
            return False
    
    def collect_flask_coverage(self) -> bool:
        """Collect coverage from Flask application"""
        print("📊 Collecting Flask application coverage...")
        
        if not self.check_flask_environment():
            print("❌ Flask virtual environment does not exist")
            return False
        
        if not self.flask_app_dir.exists():
            print(f"❌ Flask application directory does not exist, please check path: {self.flask_app_dir}")
            return False
        
        try:
            # Change to flask_app directory for coverage collection
            original_cwd = os.getcwd()
            os.chdir(self.flask_app_dir)
            
            # Start Flask app with coverage
            cmd = [
                'bash', '-c',
                'eval "$(pyenv init -)" && pyenv shell flask && '
                'coverage run --source=flask_app app_with_mysql.py'
            ]
            
            print(f"Executing command: {' '.join(cmd)}")
            print("⚠️  Please manually stop Flask application to complete coverage collection")
            
            # Start Flask app in background
            process = subprocess.Popen(cmd)
            
            print("✅ Flask application started, collecting coverage...")
            print("💡 After running tests, please stop Flask application to complete coverage collection")
            print(f"📁 Coverage data will be saved at: {self.flask_coverage_data}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Flask application: {e}")
            return False
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
    
    def generate_coverage_report(self, report_type: str = "main") -> bool:
        """Generate coverage report"""
        print(f"📊 Generating {report_type} coverage report...")
        
        try:
            if report_type == "flask":
                # Generate Flask app coverage report
                if not self.flask_coverage_data.exists():
                    print("❌ Flask coverage data does not exist, please run Flask application first")
                    return False
                
                # Change to flask_app directory
                original_cwd = os.getcwd()
                os.chdir(self.flask_app_dir)
                
                try:
                    # Generate HTML report
                    cmd = ['coverage', 'html', '-d', str(self.flask_coverage_dir)]
                    result = subprocess.run(cmd, check=True)
                    
                    # Generate XML report
                    cmd = ['coverage', 'xml', '-o', str(self.flask_coverage_xml)]
                    result = subprocess.run(cmd, check=True)
                    
                    # Show summary
                    cmd = ['coverage', 'report']
                    result = subprocess.run(cmd, check=True)
                    
                    print("✅ Flask coverage report generation successful")
                    print(f"📁 HTML report: {self.flask_coverage_dir}")
                    print(f"📄 XML report: {self.flask_coverage_xml}")
                    
                    return True
                    
                finally:
                    os.chdir(original_cwd)
            else:
                # Generate main project coverage report
                if not self.coverage_data.exists():
                    print("❌ Main project coverage data does not exist, please run tests first")
                    return False
                
                # Generate HTML report
                cmd = ['coverage', 'html', '-d', str(self.coverage_dir)]
                result = subprocess.run(cmd, check=True)
                
                # Generate XML report
                cmd = ['coverage', 'xml', '-o', str(self.coverage_xml)]
                result = subprocess.run(cmd, check=True)
                
                # Show summary
                cmd = ['coverage', 'report']
                result = subprocess.run(cmd, check=True)
                
                print("✅ Main project coverage report generation successful")
                print(f"📁 HTML report: {self.coverage_dir}")
                print(f"📄 XML report: {self.coverage_xml}")
                
                return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to generate coverage report: {e}")
            return False
    
    def run_tests_with_coverage(self, test_type: str = "all") -> bool:
        """Run tests with coverage"""
        print(f"🧪 Running {test_type} tests and collecting coverage...")
        
        try:
            # Run tests with coverage
            cmd = [
                'bash', '-c',
                'eval "$(pyenv init -)" && pyenv shell pte && '
                f'pytest --cov=. --cov-report=html:{self.coverage_dir} '
                f'--cov-report=xml:{self.coverage_xml} --cov-report=term-missing'
            ]
            
            if test_type == "demo":
                cmd[-1] += ' test/department/user/demo_*.py'
            elif test_type == "business":
                cmd[-1] += ' test/department/user/business_*.py'
            elif test_type == "real-api":
                cmd[-1] += ' test/department/user/business_real_api_tests.py'
            
            print(f"Executing command: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True)
            
            print("✅ Tests completed, coverage report generated")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Test execution failed: {e}")
            return False
    
    def show_coverage_summary(self, summary_type: str = "main") -> bool:
        """Show coverage summary"""
        print(f"📊 {summary_type} coverage summary:")
        
        try:
            if summary_type == "flask":
                if not self.flask_coverage_data.exists():
                    print("❌ Flask coverage data does not exist")
                    return False
                
                # Change to flask_app directory
                original_cwd = os.getcwd()
                os.chdir(self.flask_app_dir)
                
                try:
                    cmd = ['coverage', 'report']
                    result = subprocess.run(cmd, check=True)
                    return True
                finally:
                    os.chdir(original_cwd)
            else:
                if not self.coverage_data.exists():
                    print("❌ Main project coverage data does not exist")
                    return False
                
                cmd = ['coverage', 'report']
                result = subprocess.run(cmd, check=True)
                return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to get coverage summary: {e}")
            return False
    
    def clean_coverage_data(self, clean_type: str = "all") -> bool:
        """Clean coverage data"""
        print(f"🧹 Cleaning {clean_type} coverage data...")
        
        try:
            if clean_type in ["all", "main"]:
                # Remove main project coverage files
                if self.coverage_data.exists():
                    self.coverage_data.unlink()
                
                # Also check reports directory
                reports_coverage_data = self.reports_dir / ".coverage"
                if reports_coverage_data.exists():
                    reports_coverage_data.unlink()
                
                if self.coverage_xml.exists():
                    self.coverage_xml.unlink()
                
                # Remove coverage directory
                if self.coverage_dir.exists():
                    import shutil
                    shutil.rmtree(self.coverage_dir)
            
            if clean_type in ["all", "flask"]:
                # Remove Flask app coverage files
                if self.flask_coverage_data.exists():
                    self.flask_coverage_data.unlink()
                
                if self.flask_coverage_xml.exists():
                    self.flask_coverage_xml.unlink()
                
                # Remove Flask coverage directory
                if self.flask_coverage_dir.exists():
                    import shutil
                    shutil.rmtree(self.flask_coverage_dir)
            
            print("✅ Coverage data cleanup completed")
            return True
            
        except Exception as e:
            print(f"❌ Failed to clean coverage data: {e}")
            return False
    
    def open_coverage_report(self, report_type: str = "main") -> bool:
        """Open coverage report in browser"""
        print(f"🌐 Opening {report_type} coverage report...")
        
        try:
            if report_type == "flask":
                index_file = self.flask_coverage_dir / "index.html"
            else:
                index_file = self.coverage_dir / "index.html"
            
            if not index_file.exists():
                print(f"❌ {report_type} coverage report does not exist, please generate report first")
                return False
            
            # Open in browser
            import webbrowser
            webbrowser.open(f"file://{index_file.absolute()}")
            
            print(f"✅ {report_type} coverage report opened in browser")
            return True
            
        except Exception as e:
            print(f"❌ Failed to open coverage report: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Coverage Management Tool')
    parser.add_argument('--collect-flask', action='store_true',
                       help='Collect coverage from Flask application')
    parser.add_argument('--run-tests', choices=['all', 'demo', 'business', 'real-api'],
                       help='Run tests with coverage')
    parser.add_argument('--generate-report', choices=['main', 'flask'],
                       help='Generate coverage report (main or flask)')
    parser.add_argument('--show-summary', choices=['main', 'flask'],
                       help='Show coverage summary (main or flask)')
    parser.add_argument('--clean', choices=['all', 'main', 'flask'],
                       help='Clean coverage data (all, main, or flask)')
    parser.add_argument('--open', choices=['main', 'flask'],
                       help='Open coverage report in browser (main or flask)')
    parser.add_argument('--check-language', action='store_true',
                       help='Check server language configuration')
    
    args = parser.parse_args()
    
    manager = CoverageManager()
    
    if args.check_language:
        language = manager.check_server_language()
        print(f"🌐 Server language: {language}")
        if language == "python":
            print("✅ Supports coverage collection")
        else:
            print("⚠️  Current language does not support coverage collection")
    
    elif args.collect_flask:
        manager.collect_flask_coverage()
    
    elif args.run_tests:
        manager.run_tests_with_coverage(args.run_tests)
    
    elif args.generate_report:
        manager.generate_coverage_report(args.generate_report)
    
    elif args.show_summary:
        manager.show_coverage_summary(args.show_summary)
    
    elif args.clean:
        manager.clean_coverage_data(args.clean)
    
    elif args.open:
        manager.open_coverage_report(args.open)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
