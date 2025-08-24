"""
PTE Framework pytest configuration
Defines fixtures and configuration for all tests
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
    
    # Reset Log class state to ensure clean LogID
    Log._current_logid = None
    Log._logger_instance = None
    
    # Set LogID for the test
    Log.set_logid(logid)
    
    # Force recreation of logger instance with new LogID
    logger_instance = Log._get_logger()
    logger_instance.logid = logid
    
    # Add LogID attachment to Allure report
    logger_instance._add_logid_attachment("auto_generated")
    
    yield logid
    
    # Cleanup after test
    # Reset Log class state for next test
    Log._current_logid = None
    Log._logger_instance = None
