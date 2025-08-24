# PTE Framework Installation Guide

## Overview

This guide provides comprehensive installation instructions for the PTE Framework, covering all supported platforms and installation scenarios.

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.6 or higher
- **Docker**: For MySQL environment (optional but recommended)
- **Git**: For cloning the repository
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Disk Space**: Minimum 2GB free space

### Python Environment

The framework requires Python 3.6 or higher. We recommend using a virtual environment:

```bash
# Check Python version
python --version

# Create virtual environment (using venv)
python -m venv pte_env
source pte_env/bin/activate  # Linux/macOS
# or
pte_env\Scripts\activate     # Windows

# Or using pyenv (recommended)
pyenv install 3.12.11
pyenv virtualenv 3.12.11 pte
pyenv activate pte
```

## Installation Methods

### Method 1: Standard Installation (Recommended)

#### 1. Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd pte

# Or download and extract if you have the source code
```

#### 2. Install Python Dependencies

```bash
# Activate your Python environment
pyenv activate pte  # or your preferred method

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pytest, requests, yaml; print('Dependencies installed successfully')"
```

#### 3. Install PTE Command (Optional)

```bash
# Install pte command to system PATH
./install_pte.sh --install

# Reload shell configuration
source ~/.zshrc  # or ~/.bashrc, ~/.bash_profile

# Verify installation
pte help
```

#### 4. Set Up Database Environment

```bash
# Start MySQL container
docker run --name mysql57 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql:5.7

# Wait for MySQL to start (usually 30-60 seconds)
sleep 30

# Verify MySQL environment
python scripts/test_mysql_docker.py
```

#### 5. Verify Installation

```bash
# Validate configuration files
python config_manager.py validate

# View current configuration
python config_manager.py show-idc local_test

# Run a simple test
pte demo
```

### Method 2: Development Installation

For developers who want to contribute to the framework:

```bash
# Clone the repository
git clone <repository-url>
cd pte

# Create and activate virtual environment
pyenv virtualenv 3.12.11 pte-dev
pyenv activate pte-dev

# Install dependencies in development mode
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Install pre-commit hooks
pre-commit install

# Set up development database
docker run --name mysql57-dev -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql:5.7
```

### Method 3: Docker Installation

For containerized environments:

```bash
# Create Dockerfile for PTE
cat > Dockerfile << 'EOF'
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install PTE command
RUN chmod +x install_pte.sh && ./install_pte.sh --install

# Expose ports
EXPOSE 3306

# Default command
CMD ["pte", "help"]
EOF

# Build Docker image
docker build -t pte-framework .

# Run PTE in container
docker run -it --rm pte-framework pte demo
```

## Configuration Setup

### 1. Environment Configuration

Create or modify the environment configuration:

```yaml
# config/env.yaml
idc: "local_test"  # Current IDC to test
env: "local"       # Current environment tag to test
```

### 2. Local Test Configuration

Configure the local testing environment:

```yaml
# config/local_test.yaml
host: "http://localhost:5001"
timeout: 30
retry_count: 3
default_headers:
  Content-Type: "application/json"
  Accept: "application/json"
  User-Agent: "Universal-Test-Framework/1.0"

database:
  mysql:
    host: "127.0.0.1"
    port: 3306
    username: "root"
    password: "password"
    database: "pte"
    charset: "utf8mb4"
    pool_size: 5
    max_overflow: 10
    pool_timeout: 30
    pool_recycle: 3600
```

### 3. Common Configuration

Set up logging and other common settings:

```yaml
# config/common.yaml
logging:
  enable_file_logging: true
  
  file:
    directory: "logs"
    filename_format: "pte_{datetime}_{testcase}_{logid}_{level}.log"
    level: "INFO"
    format: "[{timestamp}] [{level}] [{logid}] [{caller}] {message}"
    rotate_by_date: true
    separate_by_level: false
    retention_days: 30
    max_size_mb: 100
    enable_compression: false
  
  console:
    enabled: true
    level: "ERROR"
    format: "[{timestamp}] [{level}] [{logid}] [{caller}] {message}"
  
  allure:
    enabled: true
    level: "INFO"
    show_detailed_data: true
```

## Database Setup

### MySQL Setup

#### Option 1: Docker MySQL (Recommended)

```bash
# Start MySQL container
docker run --name mysql57 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql:5.7

# Wait for MySQL to be ready
docker logs mysql57 | grep "ready for connections"

# Verify connection
python scripts/test_mysql_docker.py
```

#### Option 2: Local MySQL Installation

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install mysql-server

# macOS (using Homebrew)
brew install mysql
brew services start mysql

# Windows
# Download and install MySQL from https://dev.mysql.com/downloads/

# Create database and user
mysql -u root -p
CREATE DATABASE pte;
CREATE USER 'root'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON pte.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Option 3: Cloud MySQL

For cloud environments (AWS RDS, Google Cloud SQL, etc.):

```yaml
# config/cloud_mysql.yaml
database:
  mysql:
    host: "your-cloud-mysql-host"
    port: 3306
    username: "your_username"
    password: "your_password"
    database: "pte"
    charset: "utf8mb4"
    ssl_mode: "REQUIRED"
```

### Database Initialization

```bash
# Initialize database schema
python scripts/init_database.py

# Verify database setup
python scripts/test_db_connection.py
```

## Tool Installation

### Allure Reports

```bash
# Install Allure command line tool
./generate_report.sh --install

# Verify installation
allure --version
```

### Coverage Tools

```bash
# Install coverage tools
pip install pytest-cov coverage

# Verify installation
python -c "import pytest_cov, coverage; print('Coverage tools installed')"
```

## Platform-Specific Instructions

### Linux Installation

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv git docker.io

# CentOS/RHEL
sudo yum install -y python3 python3-pip git docker

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### macOS Installation

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.12 git docker

# Install pyenv (recommended)
brew install pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

### Windows Installation

```bash
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install dependencies
choco install python git docker-desktop

# Install pyenv-win
pip install pyenv-win
echo $env:USERPROFILE\.pyenv\pyenv-win\bin >> $env:USERPROFILE\.pyenv\pyenv-win\shims >> $env:PATH
```

## Verification and Testing

### 1. Basic Verification

```bash
# Check Python environment
python --version
pip list

# Check PTE command
pte help

# Check configuration
python config_manager.py current
python config_manager.py validate
```

### 2. Database Verification

```bash
# Test database connection
pte db-test

# Verify MySQL environment
pte mysql-verify

# Test database operations
python scripts/test_db_connection.py
```

### 3. Framework Verification

```bash
# Run framework demo tests
pte demo

# Run business tests
pte business

# Run all tests
pte all

# Run tests in parallel
pte all --parallel
```

### 4. Reporting Verification

```bash
# Generate Allure report
./generate_report.sh --generate

# Open Allure report
./generate_report.sh --open

# Generate coverage report
./manage_coverage.sh --run-tests all
./manage_coverage.sh --generate-report main
./manage_coverage.sh --open main
```

## Troubleshooting

### Common Installation Issues

#### 1. Python Version Issues

```bash
# Check Python version
python --version

# If version is too old, upgrade Python
# Ubuntu/Debian
sudo apt-get install python3.12

# macOS
brew install python@3.12

# Windows
# Download from https://www.python.org/downloads/
```

#### 2. Dependency Installation Issues

```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Install dependencies one by one
pip install pytest
pip install requests
pip install PyYAML
# ... continue with other dependencies
```

#### 3. Docker Issues

```bash
# Check Docker status
docker --version
docker ps

# Start Docker service
sudo systemctl start docker  # Linux
# or start Docker Desktop on macOS/Windows

# Check Docker permissions
sudo usermod -aG docker $USER
newgrp docker
```

#### 4. Database Connection Issues

```bash
# Check MySQL container
docker ps | grep mysql

# Check MySQL logs
docker logs mysql57

# Restart MySQL container
docker restart mysql57

# Check MySQL connection
mysql -h 127.0.0.1 -P 3306 -u root -ppassword -e "SELECT 1"
```

#### 5. Configuration Issues

```bash
# Validate configuration files
python config_manager.py validate

# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('config/env.yaml'))"

# Check file permissions
ls -la config/
chmod 644 config/*.yaml
```

### Getting Help

```bash
# Show command help
pte help
./run_tests.sh --help
./generate_report.sh --help
./manage_coverage.sh --help

# Check installation status
./install_pte.sh --status

# View logs
tail -f logs/pte_*.log

# Check system information
python scripts/system_info.py  # If available
```

## Uninstallation

### Remove PTE Command

```bash
# Uninstall pte command
./install_pte.sh --uninstall

# Remove from PATH manually if needed
# Edit ~/.zshrc, ~/.bashrc, or ~/.bash_profile
# Remove the line that adds PTE to PATH
```

### Remove Dependencies

```bash
# Remove Python packages
pip uninstall -r requirements.txt

# Remove virtual environment
deactivate  # If using virtual environment
rm -rf pte_env/  # or your environment directory

# Remove pyenv environment
pyenv uninstall pte
```

### Remove Database

```bash
# Stop and remove MySQL container
docker stop mysql57
docker rm mysql57

# Remove MySQL data volume (optional)
docker volume rm $(docker volume ls -q | grep mysql)
```

### Remove Configuration

```bash
# Remove configuration files
rm -rf config/
rm -rf logs/
rm -rf reports/

# Remove project directory
cd ..
rm -rf pte/
```

## Next Steps

After successful installation:

1. **Read the Quick Start Guide**: [01_quick_start.md](01_quick_start.md)
2. **Explore the User Guide**: [02_user_guide.md](02_user_guide.md)
3. **Understand the Architecture**: [03_architecture_guide.md](03_architecture_guide.md)
4. **Write Your First Test**: Follow the examples in the user guide
5. **Customize Configuration**: Modify configuration files for your environment
6. **Join the Community**: Contribute to the framework development
