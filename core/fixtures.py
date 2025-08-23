"""
Core test fixtures - encapsulates pytest fixtures
"""
import pytest
from typing import Any, Dict, List


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
