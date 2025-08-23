"""
Demo: Static Log Class Usage
Shows how to use the simplified Log.info(), Log.warn(), Log.error() interface
"""
import pytest
import allure
import os
from config.settings import TestEnvironment
from api.client import APIClient
from biz.department.user.operations import UserOperations
from data.department.user.test_data import UserTestData
from core.logger import Log


@allure.epic("PTE Framework")
@allure.feature("Static Log Usage")
class TestStaticLogUsage:
    """Demo of static Log class usage across all layers"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment with automatic LogID"""
        # Setup environment
        os.environ['TEST_IDC'] = 'local_test'
        os.environ['TEST_ENV'] = 'local'
        
        # Initialize components (no need to pass logger)
        self.api_client = APIClient()
        self.user_ops = UserOperations()
        self.test_data = UserTestData()
        
        # Log setup completion using static Log class
        Log.info("Test environment setup completed", {
            "environment": TestEnvironment.get_current_env(),
            "host": TestEnvironment.get_host()
        })
    
    @allure.story("Simple Log Usage")
    @allure.severity(allure.severity_level.NORMAL)
    def test_simple_log_usage(self):
        """Test simple logging with static Log class"""
        Log.start_test("test_simple_log_usage")
        
        try:
            # Simple info logging
            Log.info("Starting simple log usage test")
            
            # Warning logging
            Log.warning("This is a warning message")
            
            # Error logging
            Log.error("This is an error message")
            
            # Debug logging
            Log.debug("This is a debug message")
            
            # Assertion logging
            Log.assertion("Simple assertion test", True, "True", True)
            
            Log.info("Simple log usage test completed successfully")
            Log.end_test("test_simple_log_usage", "PASSED")
            
        except Exception as e:
            Log.error(f"Simple log usage test failed: {str(e)}")
            Log.end_test("test_simple_log_usage", "FAILED")
            raise
    
    @allure.story("API Client with Static Log")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_client_with_static_log(self):
        """Test API client usage with automatic logging"""
        Log.start_test("test_api_client_with_static_log")
        
        try:
            Log.info("Testing API client with automatic logging")
            
            # API calls will automatically log using static Log class
            # No need to pass logger parameter
            response = self.api_client.get("/api/users")
            
            Log.info("API call completed", {
                "status_code": response.status_code,
                "url": "/api/users"
            })
            
            Log.end_test("test_api_client_with_static_log", "PASSED")
            
        except Exception as e:
            Log.error(f"API client test failed: {str(e)}")
            Log.end_test("test_api_client_with_static_log", "FAILED")
            raise
    
    @allure.story("Business Operations with Static Log")
    @allure.severity(allure.severity_level.NORMAL)
    def test_business_operations_with_static_log(self):
        """Test business operations with automatic logging"""
        Log.start_test("test_business_operations_with_static_log")
        
        try:
            Log.info("Testing business operations with automatic logging")
            
            # Business operations will automatically log using static Log class
            # No need to pass logger parameter
            result = self.user_ops.get_all_users()
            
            Log.info("Business operation completed", {
                "result_keys": list(result.keys()) if isinstance(result, dict) else "Not a dict"
            })
            
            Log.end_test("test_business_operations_with_static_log", "PASSED")
            
        except Exception as e:
            Log.error(f"Business operations test failed: {str(e)}")
            Log.end_test("test_business_operations_with_static_log", "FAILED")
            raise
    
    @allure.story("Data Validation with Static Log")
    @allure.severity(allure.severity_level.NORMAL)
    def test_data_validation_with_static_log(self):
        """Test data validation logging with static Log class"""
        Log.start_test("test_data_validation_with_static_log")
        
        try:
            Log.info("Testing data validation with static Log")
            
            # Test data validation logging
            test_data = {"name": "John", "age": 30}
            
            Log.data_validation("name", "string", type(test_data["name"]).__name__, isinstance(test_data["name"], str))
            Log.data_validation("age", "integer", type(test_data["age"]).__name__, isinstance(test_data["age"], int))
            Log.data_validation("email", "string", "None", False)  # Simulate failed validation
            
            Log.info("Data validation test completed")
            Log.end_test("test_data_validation_with_static_log", "PASSED")
            
        except Exception as e:
            Log.error(f"Data validation test failed: {str(e)}")
            Log.end_test("test_data_validation_with_static_log", "FAILED")
            raise
    
    @allure.story("Headers with LogID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_headers_with_logid(self):
        """Test getting headers with LogID using static Log class"""
        Log.start_test("test_headers_with_logid")
        
        try:
            Log.info("Testing headers with LogID")
            
            # Get headers with current LogID
            headers = Log.get_headers_with_logid({
                'Authorization': 'Bearer token123',
                'Custom-Header': 'value'
            })
            
            Log.info("Headers generated", {
                "headers": headers,
                "logid": Log.get_logid()
            })
            
            # Verify LogID is in headers
            assert 'logId' in headers
            assert headers['logId'] == Log.get_logid()
            
            Log.info("Headers test completed successfully")
            Log.end_test("test_headers_with_logid", "PASSED")
            
        except Exception as e:
            Log.error(f"Headers test failed: {str(e)}")
            Log.end_test("test_headers_with_logid", "FAILED")
            raise
    
    @allure.story("End-to-End Workflow with Static Log")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_end_to_end_workflow_with_static_log(self):
        """Test complete workflow using static Log class"""
        Log.start_test("test_end_to_end_workflow_with_static_log")
        
        try:
            Log.info("Starting end-to-end workflow test")
            
            # Step 1: Prepare data
            user_data = self.test_data.VALID_USER_1
            Log.info("Test data prepared", {"user_data": user_data})
            
            # Step 2: Simulate API call (would be real in actual implementation)
            Log.api_call("POST", "/api/users", status_code=201, response_time=0.5)
            
            # Step 3: Validate response
            Log.assertion("Response validation", True)
            
            # Step 4: Business logic
            Log.info("Processing business logic")
            
            # Step 5: Final validation
            Log.data_validation("user_creation", "success", "success", True)
            
            Log.info("End-to-end workflow test completed successfully")
            Log.end_test("test_end_to_end_workflow_with_static_log", "PASSED")
            
        except Exception as e:
            Log.error(f"End-to-end workflow test failed: {str(e)}")
            Log.end_test("test_end_to_end_workflow_with_static_log", "FAILED")
            raise


# Example usage in app layer
class UserAppService:
    """Example app layer service using static Log"""
    
    def create_user(self, user_data):
        """Create user with automatic logging"""
        Log.info("Creating user in app layer", {"user_data": user_data})
        
        try:
            # Business logic here
            result = {"id": 1, "status": "created"}
            
            Log.info("User created successfully", {"result": result})
            return result
            
        except Exception as e:
            Log.error("User creation failed", {"error": str(e)})
            raise


# Example usage in biz layer
class UserBizService:
    """Example biz layer service using static Log"""
    
    def process_user_data(self, user_data):
        """Process user data with automatic logging"""
        Log.info("Processing user data in biz layer", {"user_data": user_data})
        
        try:
            # Business logic here
            processed_data = {"processed": True, "data": user_data}
            
            Log.info("User data processed successfully", {"processed_data": processed_data})
            return processed_data
            
        except Exception as e:
            Log.error("User data processing failed", {"error": str(e)})
            raise
