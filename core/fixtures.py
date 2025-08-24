"""
PTE Framework Core Fixtures
Provides common fixtures for test automation
"""
import pytest
from core.logger import Log, generate_logid


@pytest.fixture(autouse=True)
def auto_logid():
    """
    Automatically generate and set LogID for each test case.
    This fixture runs automatically for every test without explicit declaration.
    """
    # Generate unique LogID for this test case
    logid = generate_logid()
    
    # Set LogID for the test
    Log.set_logid(logid)
    
    # Add LogID attachment to Allure report
    Log._get_logger()._add_logid_attachment("auto_generated")
    
    yield logid
    
    # Cleanup after test (if needed)
    # Currently no cleanup needed as LogID is automatically managed


@pytest.fixture(scope="session")
def base_url():
    """Base URL fixture"""
    return "http://localhost:8080"


@pytest.fixture(scope="function")
def headers():
    """Default headers fixture"""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


@pytest.fixture(scope="function")
def auth_headers():
    """Authentication headers fixture"""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer test-token"
    }


@pytest.fixture(scope="function")
def sample_data():
    """Sample data fixture"""
    return {
        "name": "Test Data",
        "value": "test_value"
    }


@pytest.fixture(scope="function")
def sample_list_data():
    """Sample list data fixture"""
    return [
        {"id": 1, "name": "Project 1"},
        {"id": 2, "name": "Project 2"},
        {"id": 3, "name": "Project 3"}
    ]
