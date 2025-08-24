# PTE - Universal Backend Testing Framework

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/Pytest-6.2+-green.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/Documentation-4%20Guides-brightgreen.svg)](docs/)

A modern, pytest-based universal backend testing framework that supports testing Java, Go, Python and other Web systems. Features layered architecture design, flexible configuration management, comprehensive logging, and database integration.

## ✨ Key Features

- 🏗️ **Layered Architecture**: Clear separation of concerns with core, API, business, and test layers
- 🔧 **Flexible Configuration**: YAML-based configuration supporting multiple environments and IDCs
- 📊 **Comprehensive Logging**: Automatic LogID generation with end-to-end tracing
- 🗄️ **Database Integration**: Complete database testing support with connection pooling
- ⚡ **Parallel Testing**: Built-in support for parallel test execution
- 📈 **Rich Reporting**: Allure reports and code coverage analysis
- 🎯 **Test Classification**: Separation of framework demo and business case tests
- 🛠️ **Command Line Interface**: Easy-to-use `pte` command for test execution

## 📚 Documentation

- **[Quick Start Guide](docs/01_quick_start.md)** - Get up and running in minutes
- **[User Guide](docs/02_user_guide.md)** - Comprehensive usage instructions
- **[Architecture Guide](docs/03_architecture_guide.md)** - Design principles and system architecture
- **[Installation Guide](docs/04_installation_guide.md)** - Detailed installation instructions

## 🏗️ Architecture

### Layered Architecture Design

The PTE Framework follows a clear layered architecture design:

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Layer (test/)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Business Logic Layer (biz/)            │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │           API Interface Layer (api/)        │   │   │
│  │  │  ┌─────────────────────────────────────┐   │   │   │
│  │  │  │         Core Framework Layer        │   │   │   │
│  │  │  │              (core/)                │   │   │   │
│  │  │  └─────────────────────────────────────┘   │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

- **Core Layer (`core/`)**: Universal framework functionality, data validation, logging, database operations
- **API Layer (`api/`)**: HTTP client wrapper with LogID support and request/response handling
- **Business Layer (`biz/`)**: Business logic operations and database integration
- **Test Layer (`test/`)**: Test case writing using business layer functionality

### Project Structure

```
pte/
├── config/              # Configuration management
│   ├── env.yaml         # Environment management
│   ├── common.yaml      # Common settings
│   ├── local_test.yaml  # Local environment
│   └── settings.py      # Configuration manager
├── core/                # Core framework layer
│   ├── checker.py       # Universal data validator
│   ├── logger.py        # Logging system
│   ├── db_checker.py    # Database operations
│   └── fixtures.py      # Test fixtures
├── api/                 # API interface layer
│   ├── client.py        # HTTP client wrapper
│   └── config.py        # API configuration
├── biz/                 # Business logic layer
│   └── department/      # Business modules
├── test/                # Test case layer
│   └── department/      # Test modules
├── scripts/             # Utility scripts
└── docs/                # Documentation
```

### Data Flow Architecture

#### Test Execution Flow
```
Test Case → Business Operations → API Client → HTTP Request → Target System
    ↓              ↓                ↓            ↓              ↓
  Logging → Business Logging → API Logging → Request Logging → Response Logging
```

#### Configuration Flow
```
Environment Variables → Config Manager → IDC Config → Common Config → Default Values
        ↓                    ↓              ↓            ↓              ↓
    Override Values → Merged Configuration → Framework Components
```

#### Logging Flow
```
Test Execution → Log Class → File Logger → Allure Reporter → Console Output
      ↓            ↓           ↓            ↓              ↓
   LogID → Structured Log → File Output → Allure Report → Console Display
```

## 🚀 Getting Started

1. **Install the Framework**: Follow the [Installation Guide](docs/04_installation_guide.md)
2. **Quick Start**: Read the [Quick Start Guide](docs/01_quick_start.md)
3. **Learn Usage**: Explore the [User Guide](docs/02_user_guide.md)
4. **Understand Architecture**: Review the [Architecture Guide](docs/03_architecture_guide.md)
5. **Write Your Tests**: Start with the examples in the user guide

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check our comprehensive [documentation](docs/)
- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/your-repo/discussions)

---

**PTE Framework** - Universal Backend Testing Made Simple 🚀
