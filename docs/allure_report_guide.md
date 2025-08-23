# Allure Test Report Usage Guide

This document introduces how to use Allure test report functionality in the PTE framework.

## 📋 Table of Contents

- [Install Allure](#install-allure)
- [Generate Reports](#generate-reports)
- [View Reports](#view-reports)
- [Report Features](#report-features)
- [Best Practices](#best-practices)

## 🚀 Install Allure

### 1. Install Python Dependencies
```bash
pip install allure-pytest==2.13.2
```

### 2. Install Allure Command Line Tool
```bash
# Automatic installation (recommended)
./generate_report.sh --install

# Manual installation
# macOS
brew install allure

# Linux
sudo snap install allure

# Windows
# Download and install Allure command line tool
```

## 📊 Generate Reports

### 1. Run Tests and Generate Results
```bash
# Run all tests
./run_tests.sh --all

# Run specific tests
./run_tests.sh --demo
./run_tests.sh --business
./run_tests.sh --real-api
```

### 2. Generate Allure Reports
```bash
# Generate report
./generate_report.sh --generate

# Run tests and generate report (one-step completion)
./generate_report.sh --run-and-report
```

## 🌐 View Reports

### 1. Open Report
```bash
# Open report in browser
./generate_report.sh --open
```

### 2. Start Report Server
```bash
# Start local server
./generate_report.sh --serve

# Specify host and port
python scripts/generate_allure_report.py --serve --host 0.0.0.0 --port 8080
```

### 3. View Report List
```bash
# List available reports
./generate_report.sh --list
```

## 📈 Report Features

### 1. Test Overview
- **Overview**: Display overall test execution status
- **Trends**: Display historical trends of test results
- **Statistics**: Display number of passed, failed, and skipped tests

### 2. Test Details
- **Steps**: Display detailed execution steps of tests
- **Attachments**: Display screenshots, logs, and other attachments during testing
- **Environment**: Display test environment information

### 3. Classification Views
- **Epic**: View tests by epic classification
- **Feature**: View tests by feature classification
- **Story**: View tests by user story classification
- **Severity**: View tests by severity level classification

### 4. Timeline
- **Timeline**: Display test execution timeline
- **Duration**: Display execution time for each test

## 🎯 Using Allure in Tests

### 1. Basic Decorators
```python
import allure

@allure.epic("PTE Framework")
@allure.feature("User Management")
class TestUserManagement:
    
    @allure.story("User Registration")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_registration(self):
        """Test user registration functionality"""
        with allure.step("Prepare test data"):
            # Prepare data
            pass
        
        with allure.step("Execute registration operation"):
            # Execute registration
            pass
        
        with allure.step("Verify registration result"):
            # Verify result
            pass
```

### 2. Dynamic Descriptions
```python
@allure.description("""
This is a detailed test description
Can contain multiple lines of content
Explaining the purpose and steps of the test
""")
def test_with_description(self):
    pass
```

### 3. Add Attachments
```python
import allure

def test_with_attachment(self):
    # Add text attachment
    allure.attach("Test Data", "This is test data content", allure.attachment_type.TEXT)
    
    # Add HTML attachment
    allure.attach("<h1>Test Result</h1>", "Test Result", allure.attachment_type.HTML)
    
    # Add image attachment
    with open("screenshot.png", "rb") as f:
        allure.attach(f.read(), "Screenshot", allure.attachment_type.PNG)
```

### 4. Links and Tags
```python
@allure.link("https://example.com", name="Related Documentation")
@allure.issue("BUG-123", name="Related Bug")
@allure.testcase("TC-456", name="Test Case")
def test_with_links(self):
    pass
```

## 📁 Report Directory Structure

```
reports/
├── allure-results/          # Allure result files
│   ├── *.json              # Test result data
│   ├── *.xml               # Test result XML
│   └── attachments/        # Test attachments
└── allure-reports/         # Generated HTML reports
    ├── index.html          # Report homepage
    ├── widgets/            # Report components
    └── data/               # Report data
```

## 🔧 Configuration Options

### 1. pytest.ini Configuration
```ini
[pytest]
addopts = 
    --alluredir=./reports/allure-results
    -v
    --tb=short
```

### 2. Environment Variables
```bash
# Set Allure results directory
export ALLURE_RESULTS_DIR=./reports/allure-results

# Set Allure report directory
export ALLURE_REPORT_DIR=./reports/allure-reports
```

## 🎨 Customize Reports

### 1. Custom Styles
```bash
# Create custom style files
mkdir -p reports/allure-results/plugins/custom-logo-plugin/static
# Add custom CSS and images
```

### 2. Environment Information
```bash
# Create environment information file
echo "Browser=Chrome
Version=1.0.0
Environment=Test" > reports/allure-results/environment.properties
```

## 🚨 Troubleshooting

### 1. Common Issues

**Issue**: Allure command line tool not found
```bash
# Solution
./generate_report.sh --install
```

**Issue**: Report generation failed
```bash
# Check if results directory exists
ls -la reports/allure-results/

# Clean and regenerate
./generate_report.sh --clean
./run_tests.sh --all
./generate_report.sh --generate
```

**Issue**: Report cannot be opened
```bash
# Check if port is occupied
lsof -i :8080

# Use different port
./generate_report.sh --serve --port 8081
```

### 2. Log Viewing
```bash
# View Allure logs
tail -f ~/.allure/allure.log
```

## 📚 Best Practices

### 1. Test Organization
- Use meaningful Epic, Feature, Story classifications
- Add clear descriptions for each test
- Use appropriate severity levels

### 2. Step Management
- Break tests into clear steps
- Each step has a clear purpose
- Add necessary validations in steps

### 3. Attachment Management
- Add screenshots for failed tests
- Save important test data
- Record environment information

### 4. Report Maintenance
- Regularly clean old reports
- Save important historical reports
- Configure automatic report generation

## 🔗 Related Links

- [Allure Official Documentation](https://docs.qameta.io/allure/)
- [Allure GitHub](https://github.com/allure-framework/allure2)
- [Allure Python Plugin](https://github.com/allure-framework/allure-python)
