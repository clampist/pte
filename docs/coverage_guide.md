# Code Coverage Usage Guide

This document introduces how to use code coverage functionality in the PTE framework.

## 📋 Table of Contents

- [Coverage Feature Overview](#coverage-feature-overview)
- [Environment Configuration](#environment-configuration)
- [Coverage Collection](#coverage-collection)
- [Report Generation](#report-generation)
- [Best Practices](#best-practices)

## 🎯 Coverage Feature Overview

### 1. Supported Languages
- **Python**: Currently the only server language that supports coverage collection
- **Other Languages**: Future versions will support Java, Go, and other languages

### 2. Coverage Types
- **Statement Coverage**: Code statement execution coverage
- **Branch Coverage**: Conditional branch execution coverage
- **Function Coverage**: Function call coverage

### 3. Report Formats
- **HTML Reports**: Detailed interactive coverage reports
- **XML Reports**: XML format reports for CI/CD integration
- **Terminal Reports**: Coverage summaries in command line

## 🚀 Environment Configuration

### 1. Server Language Configuration
```yaml
# config/env.yaml
server_language: "python"  # Currently supports: python
```

### 2. Dependency Installation
```bash
# Main project environment (pte)
pip install pytest-cov==4.1.0

# Flask application environment (flask)
pip install coverage==7.4.1
```

### 3. Configuration Files
```ini
# pytest.ini
addopts = 
    --cov=.
    --cov-report=html:./reports/coverage-html
    --cov-report=xml:./reports/coverage.xml
    --cov-report=term-missing
```

## 📊 Coverage Collection

### 1. Check Server Language
```bash
# Check current server language configuration
./manage_coverage.sh --check-language
```

### 2. Run Tests and Collect Coverage
```bash
# Run Demo tests and collect coverage
./manage_coverage.sh --run-tests demo

# Run business tests and collect coverage
./manage_coverage.sh --run-tests business

# Run real API tests and collect coverage
./manage_coverage.sh --run-tests real-api

# Run all tests and collect coverage
./manage_coverage.sh --run-tests all
```

### 3. Collect Flask Application Coverage
```bash
# Start Flask application and collect coverage
./manage_coverage.sh --collect-flask

# Stop Flask application after running tests
# Coverage data will be automatically saved
```

## 📈 Report Generation

### 1. Generate Coverage Reports
```bash
# Generate HTML and XML reports
./manage_coverage.sh --generate-report
```

### 2. View Coverage Summary
```bash
# Display coverage summary in terminal
./manage_coverage.sh --show-summary
```

### 3. Open Coverage Reports
```bash
# Open HTML report in browser
./manage_coverage.sh --open
```

### 4. Clean Coverage Data
```bash
# Clean coverage data files
./manage_coverage.sh --clean
```

## 📁 Report File Structure

```
pte/                               # PTE Testing Framework
├── .coveragerc                    # Main project coverage configuration
├── .coverage                      # Main project coverage data
└── reports/
    ├── coverage-html/            # Main project HTML coverage report
    ├── coverage.xml              # Main project XML coverage report
    ├── flask-coverage-html/      # Target application HTML coverage report
    └── flask-coverage.xml        # Target application XML coverage report

pte_target/                        # Target application (independent project)
├── flask_app/
│   ├── .coveragerc               # Target application coverage configuration
│   └── .coverage                 # Target application coverage data
```

## 🎨 Coverage Report Interpretation

### 1. Coverage Metrics
- **Stmts**: Total number of statements
- **Miss**: Number of uncovered statements
- **Cover**: Coverage percentage
- **Missing**: Line numbers of uncovered statements

### 2. Color Indicators
- **Green**: High coverage (80%+)
- **Yellow**: Medium coverage (50-80%)
- **Red**: Low coverage (<50%)

### 3. File Classification
- **PTE Framework Core Code**: api/, biz/, core/, config/
- **PTE Framework Test Code**: test/
- **PTE Framework Data Code**: data/
- **Target Application Code**: $PTE_TARGET_ROOT/flask_app/ (independent coverage collection)

## 🔧 Advanced Configuration

### 1. Coverage Exclusion Configuration
```ini
# Main project .coveragerc
[run]
source = .
omit = 
    */tests/*
    */test_*
    */flask_app/*
    */__pycache__/*
    */reports/*
    */docs/*
    */scripts/*

# Target application $PTE_TARGET_ROOT/flask_app/.coveragerc
[run]
source = flask_app
omit = 
    */__pycache__/*
    */test_*
    */tests/*
```

### 2. Exclude Specific Code
```python
# Use pragma comments in code to exclude
if debug:  # pragma: no cover
    print("Debug info")
```

### 3. Custom Coverage Collection
```bash
# Manually collect main project coverage
coverage run --source=. pytest test/department/user/demo_*.py

# Manually collect target application coverage
cd $PTE_TARGET_ROOT/flask_app
coverage run --source=flask_app app_with_mysql.py

# Generate PTE framework report
coverage html -d ../../pte/reports/coverage-html
coverage xml -o ../../pte/reports/coverage.xml

# Generate target application report
coverage html -d ../../pte/reports/flask-coverage-html
coverage xml -o ../../pte/reports/flask-coverage.xml
```

## 📚 Best Practices

### 1. Coverage Targets
- **Core Business Logic**: 90%+
- **Tools and Scripts**: 80%+
- **Test Code**: No coverage requirement
- **Configuration and Documentation**: No coverage requirement

### 2. Collection Strategy
- **Development Phase**: Run tests for relevant modules
- **Integration Testing**: Run complete test suites
- **CI/CD**: Automatically collect and report coverage

### 3. Report Management
- **Regular Cleanup**: Clean old coverage data
- **Version Control**: Include coverage reports in version control
- **Team Sharing**: Regularly share coverage reports

### 4. Quality Improvement
- **Identify Blind Spots**: Identify untested code based on coverage reports
- **Refactor Tests**: Add tests for low-coverage modules
- **Code Review**: Use coverage as a metric in code reviews

## 🚨 Troubleshooting

### 1. Common Issues

**Issue**: Coverage data does not exist
```bash
# Solution
./manage_coverage.sh --run-tests all
```

**Issue**: Coverage report generation failed
```bash
# Solution
./manage_coverage.sh --clean
./manage_coverage.sh --run-tests all
```

**Issue**: Server language not supported
```bash
# Check configuration
./manage_coverage.sh --check-language

# Modify configuration
# Edit config/env.yaml, set server_language: "python"
```

### 2. Performance Optimization
- **Incremental Collection**: Only collect coverage for changed files
- **Parallel Collection**: Collect coverage in parallel across multiple environments
- **Caching Mechanism**: Cache coverage data to improve performance

## 🔗 Related Documentation

- [PTE Framework Usage Guide](../README.md)
- [Flask Environment Management Guide](./flask_environment_guide.md)
- [Allure Report Usage Guide](./allure_report_guide.md)
- [Script Responsibilities Description](./script_responsibilities.md)
