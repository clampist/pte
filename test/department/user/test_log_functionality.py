"""
PTE Logging Functionality Comprehensive Tests
Integrates all logging-related tests including LogID generation, log recording, attachment functionality, etc.
"""
import pytest
import allure
import os
from config.settings import TestEnvironment
from api.client import APIClient
from biz.department.user.operations import UserOperations
from data.department.user.test_data import UserTestData
from core.logger import Log, generate_logid
from core.checker import Checker


@allure.epic("PTE Framework")
@allure.feature("Log Functionality")
class TestLogFunctionality:
    """PTE Logging Functionality Comprehensive Test Class"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        os.environ['TEST_IDC'] = 'local_test'
        os.environ['TEST_ENV'] = 'local'
        
        # Initialize components
        self.api_client = APIClient()
        self.user_ops = UserOperations()
        self.test_data = UserTestData()
    
    @allure.story("Basic Log Functions")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_basic_log_functions(self):
        """Test basic logging functionality - info/warning/error/debug"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_basic_log_functions")
        
        try:
            # Test basic logging functionality
            Log.info("This is an info log")
            Log.warning("This is a warning log")
            Log.error("This is an error log")
            Log.debug("This is a debug log")
            
            # Test logging with data
            test_data = {
                "user_id": 12345,
                "username": "testuser",
                "email": "test@example.com"
            }
            Log.info("User data", test_data)
            
            # Test structured data
            Log.info("Structured data", {"key": "value", "number": 123})
            
            Log.info("Basic logging functionality test completed")
            
        except Exception as e:
            Log.error(f"Basic logging functionality test failed: {str(e)}")
            Log.end_test("test_basic_log_functions", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_basic_log_functions", "PASSED")
    
    @allure.story("LogID Management")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logid_management(self):
        """Test LogID management functionality"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_logid_management")
        
        try:
            # Test LogID generation and retrieval
            original_logid = Log.get_logid()
            Log.info(f"Current LogID: {original_logid}")
            
            # Verify LogID is not empty
            Checker.assert_not_none(original_logid, "LogID")
            Checker.assert_length_greater_than(original_logid, 0, "LogID")
            
            # Test LogID consistency
            current_logid = Log.get_logid()
            Checker.assert_equal(original_logid, current_logid, "LogID")
            
            # Test new LogID generation
            new_logid = generate_logid()
            Checker.assert_not_equal(new_logid, original_logid, "LogID")
            
            Log.info("LogID management functionality test completed")
            
        except Exception as e:
            Log.error(f"LogID management functionality test failed: {str(e)}")
            Log.end_test("test_logid_management", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_logid_management", "PASSED")
    
    @allure.story("API Call Logging")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_call_logging(self):
        """Test API call logging functionality"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_api_call_logging")
        
        try:
            # Test simple API call logging
            Log.api_call("GET", "/api/health", 200, 0.1)
            
            # Test complete API call logging
            test_data = {
                "user_id": 12345,
                "username": "testuser",
                "email": "test@example.com"
            }
            Log.api_call(
                method="POST",
                url="/api/users",
                status_code=201,
                response_time=0.5,
                request_data=test_data,
                response_data={"user_id": 12345, "status": "created"}
            )
            
            # Test API calls with different status codes
            Log.api_call("GET", "/api/users/999", 404, 0.2)
            Log.api_call("PUT", "/api/users/123", 500, 1.0)
            
            Log.info("API call logging functionality test completed")
            
        except Exception as e:
            Log.error(f"API call logging functionality test failed: {str(e)}")
            Log.end_test("test_api_call_logging", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_api_call_logging", "PASSED")
    
    @allure.story("Data Validation Logging")
    @allure.severity(allure.severity_level.NORMAL)
    def test_data_validation_logging(self):
        """Test data validation logging functionality"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_data_validation_logging")
        
        try:
            # Test successful data validation
            Log.data_validation("Username", "testuser", "testuser", True)
            Log.data_validation("User ID", 12345, 12345, True)
            Log.data_validation("Email format", "test@example.com", "test@example.com", True)
            
            # Test failed data validation
            Log.data_validation("User age", 25, 30, False)
            Log.data_validation("User status", "active", "inactive", False)
            Log.data_validation("Permission level", "admin", "user", False)
            
            # Test validation of different data types
            Log.data_validation("Boolean value", True, True, True)
            Log.data_validation("Float number", 3.14, 3.14, True)
            Log.data_validation("List length", 3, 5, False)
            
            Log.info("Data validation logging functionality test completed")
            
        except Exception as e:
            Log.error(f"Data validation logging functionality test failed: {str(e)}")
            Log.end_test("test_data_validation_logging", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_data_validation_logging", "PASSED")
    
    @allure.story("Assertion Logging")
    @allure.severity(allure.severity_level.NORMAL)
    def test_assertion_logging(self):
        """Test assertion logging functionality"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_assertion_logging")
        
        try:
            # Test successful assertions
            Log.assertion("Check user ID", True, 12345, 12345)
            Log.assertion("Check username", True, "testuser", "testuser")
            Log.assertion("Check status code", True, 200, 200)
            
            # Test failed assertions
            Log.assertion("Check user age", False, 25, 30)
            Log.assertion("Check user email", False, "test@example.com", "wrong@example.com")
            Log.assertion("Check response time", False, 0.5, 1.0)
            
            # Test different types of assertions
            Log.assertion("Boolean assertion", True, True, True)
            Log.assertion("String assertion", True, "success", "success")
            Log.assertion("Numeric assertion", True, 100, 100)
            
            Log.info("Assertion logging functionality test completed")
            
        except Exception as e:
            Log.error(f"Assertion logging functionality test failed: {str(e)}")
            Log.end_test("test_assertion_logging", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_assertion_logging", "PASSED")
    
    @allure.story("Step Decorator")
    @allure.severity(allure.severity_level.NORMAL)
    def test_step_decorator(self):
        """Test step decorator functionality"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_step_decorator")
        
        try:
            # Test step decorator
            @Log.step("User registration step")
            def register_user():
                Log.info("Starting user registration process")
                return {"user_id": 67890, "status": "registered"}
            
            @Log.step("User validation step")
            def validate_user():
                Log.info("Validating user information")
                return {"valid": True}
            
            @Log.step("User activation step")
            def activate_user():
                Log.info("Activating user account")
                return {"activated": True}
            
            # Execute steps
            register_result = register_user()
            Log.info("User registration completed", register_result)
            
            validate_result = validate_user()
            Log.info("User validation completed", validate_result)
            
            activate_result = activate_user()
            Log.info("User activation completed", activate_result)
            
            Log.info("Step decorator functionality test completed")
            
        except Exception as e:
            Log.error(f"Step decorator functionality test failed: {str(e)}")
            Log.end_test("test_step_decorator", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_step_decorator", "PASSED")
    
    @allure.story("LogID Attachment")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logid_attachment(self):
        """Test LogID attachment functionality"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_logid_attachment")
        
        try:
            Log.info("Starting LogID attachment functionality test")
            
            # Log test steps
            Log.info("Step 1: Prepare test data")
            test_data = {
                "user_id": 12345,
                "username": "testuser",
                "email": "test@example.com"
            }
            Log.info("Test data preparation completed", test_data)
            
            # Simulate API call
            Log.api_call(
                method="POST",
                url="/api/users",
                status_code=201,
                response_time=0.5,
                request_data=test_data,
                response_data={"user_id": 12345, "status": "created"}
            )
            
            # Data validation
            Log.data_validation("user_id", 12345, 12345, True)
            Log.data_validation("username", "testuser", "testuser", True)
            
            # Assertion
            Log.assertion("Check user creation success", True, 201, 201)
            
            Log.info("LogID attachment functionality test completed")
            
        except Exception as e:
            Log.error(f"LogID attachment functionality test failed: {str(e)}")
            Log.end_test("test_logid_attachment", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_logid_attachment", "PASSED")
    
    @allure.story("Headers with LogID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_headers_with_logid(self):
        """Test headers with LogID functionality"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_headers_with_logid")
        
        try:
            Log.info("Testing headers with LogID functionality")
            
            # Get headers with LogID
            headers = Log.get_headers_with_logid({
                'Authorization': 'Bearer token123',
                'Content-Type': 'application/json',
                'Custom-Header': 'value'
            })
            
            Log.info("Headers generation completed", {
                "headers": headers,
                "logid": Log.get_logid()
            })
            
            # Verify LogID in headers
            Checker.assert_contains(headers, 'logId')
            Checker.assert_equal(headers['logId'], Log.get_logid(), "logId in headers")
            
            # Verify other headers remain unchanged
            Checker.assert_equal(headers['Authorization'], 'Bearer token123', "Authorization header")
            Checker.assert_equal(headers['Content-Type'], 'application/json', "Content-Type header")
            Checker.assert_equal(headers['Custom-Header'], 'value', "Custom-Header")
            
            Log.info("Headers with LogID functionality test completed")
            
        except Exception as e:
            Log.error(f"Headers with LogID functionality test failed: {str(e)}")
            Log.end_test("test_headers_with_logid", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_headers_with_logid", "PASSED")
    
    @allure.story("Integration with Framework Components")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_framework_integration(self):
        """Test integration with framework components"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_framework_integration")
        
        try:
            Log.info("Testing integration with framework components")
            
            # Test integration with API client
            Log.info("Testing API client integration")
            response = self.api_client.get("/api/users")
            Log.info("API call completed", {
                "status_code": response.status_code,
                "url": "/api/users"
            })
            
            # Test integration with business operations
            Log.info("Testing business operations integration")
            result = self.user_ops.get_all_users()
            Log.info("Business operation completed", {
                "result_keys": list(result.keys()) if isinstance(result, dict) else "Not a dict"
            })
            
            # Test integration with test data
            Log.info("Testing data integration")
            user_data = self.test_data.VALID_USER_1
            Log.info("Test data retrieval completed", {"user_data": user_data})
            
            # Validate data
            Checker.assert_field_value(user_data, "name", "John Smith")
            Checker.assert_field_value(user_data, "email", "john.smith@example.com")
            Checker.assert_field_value(user_data, "age", 25)
            
            Log.info("Framework components integration test completed")
            
        except Exception as e:
            Log.error(f"Framework components integration test failed: {str(e)}")
            Log.end_test("test_framework_integration", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_framework_integration", "PASSED")


# Standalone test functions
def test_standalone_log_functionality():
    """Standalone logging functionality test"""
    # Step 1: Set LogID
    logid = generate_logid()
    Log.set_logid(logid)
    
    # Step 2: Start test
    Log.start_test("test_standalone_log_functionality")
    
    try:
        Log.info("Starting standalone logging functionality test")
        
        # Test basic logging
        Log.info("Info log in standalone test")
        Log.warning("Warning log in standalone test")
        
        # Test API call
        Log.api_call("GET", "/api/health", 200, 0.1)
        
        # Test assertion
        Log.assertion("Health check", True, 200, 200)
        
        # Test data validation
        Log.data_validation("Health status", "ok", "ok", True)
        
        Log.info("Standalone logging functionality test completed")
        
    except Exception as e:
        Log.error(f"Standalone logging functionality test failed: {str(e)}")
        Log.end_test("test_standalone_log_functionality", "FAILED")
        raise
    else:
        # Final step: End test
        Log.end_test("test_standalone_log_functionality", "PASSED")


def test_logid_consistency_across_calls():
    """Test LogID consistency across multiple calls"""
    # Step 1: Set LogID
    logid = generate_logid()
    Log.set_logid(logid)
    
    # Step 2: Start test
    Log.start_test("test_logid_consistency_across_calls")
    
    try:
        # Record initial LogID
        initial_logid = Log.get_logid()
        Log.info(f"Initial LogID: {initial_logid}")
        
        # Multiple calls to logging methods, verify LogID consistency
        for i in range(5):
            Log.info(f"Log call #{i+1}")
            current_logid = Log.get_logid()
            Checker.assert_equal(current_logid, initial_logid, f"LogID at call {i+1}")
        
        # Call different types of logging methods
        Log.warning("Warning log test")
        Checker.assert_equal(Log.get_logid(), initial_logid, "LogID after warning")
        
        Log.error("Error log test")
        Checker.assert_equal(Log.get_logid(), initial_logid, "LogID after error")
        
        Log.api_call("GET", "/test", 200, 0.1)
        Checker.assert_equal(Log.get_logid(), initial_logid, "LogID after API call")
        
        Log.assertion("Test assertion", True, "expected", "expected")
        Checker.assert_equal(Log.get_logid(), initial_logid, "LogID after assertion")
        
        Log.info("LogID consistency test completed")
        
    except Exception as e:
        Log.error(f"LogID consistency test failed: {str(e)}")
        Log.end_test("test_logid_consistency_across_calls", "FAILED")
        raise
    else:
        # Final step: End test
        Log.end_test("test_logid_consistency_across_calls", "PASSED")


if __name__ == "__main__":
    # This file can be run directly for testing
    pytest.main([__file__, "-v"])
