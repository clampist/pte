"""
Demo test examples for file logging functionality
"""
import pytest
from core.logger import Log, generate_logid


class TestFileLoggingDemo:
    """Demo test class for file logging functionality"""
    
    def test_basic_logging(self):
        """Test basic logging functionality"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_basic_logging")
        
        try:
            Log.info("This is an info log")
            Log.warning("This is a warning log")
            Log.error("This is an error log")
            Log.debug("This is a debug log")
            
            # Log structured data
            user_data = {
                "user_id": 12345,
                "username": "testuser",
                "email": "test@example.com"
            }
            Log.info("User data", user_data)
            
        except Exception as e:
            Log.error(f"test_basic_logging test failed: {str(e)}")
            Log.end_test("test_basic_logging", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_basic_logging", "PASSED")
    
    def test_api_logging(self):
        """Test API call logging"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_api_logging")
        
        try:
            # Simulate API call
            Log.api_call(
                method="POST",
                url="/api/users",
                status_code=201,
                response_time=0.5,
                request_data={"username": "newuser", "email": "new@example.com"},
                response_data={"user_id": 67890, "status": "created"}
            )
            
            # Simulate another API call
            Log.api_call(
                method="GET",
                url="/api/users/67890",
                status_code=200,
                response_time=0.2
            )
            
        except Exception as e:
            Log.error(f"test_api_logging test failed: {str(e)}")
            Log.end_test("test_api_logging", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_api_logging", "PASSED")
    
    def test_assertion_logging(self):
        """Test assertion logging"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_assertion_logging")
        
        try:
            # Successful assertion
            Log.assertion("Check user ID", True, 12345, 12345)
            Log.assertion("Check username", True, "testuser", "testuser")
            
            # Failed assertion
            Log.assertion("Check user age", False, 25, 30)
            Log.assertion("Check user email", False, "test@example.com", "wrong@example.com")
            
        except Exception as e:
            Log.error(f"test_assertion_logging test failed: {str(e)}")
            Log.end_test("test_assertion_logging", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_assertion_logging", "PASSED")
    
    def test_data_validation(self):
        """Test data validation logging"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_data_validation")
        
        try:
            # Successful data validation
            Log.data_validation("Username", "testuser", "testuser", True)
            Log.data_validation("Email format", "test@example.com", "test@example.com", True)
            
            # Failed data validation
            Log.data_validation("User age", 25, 30, False)
            Log.data_validation("User status", "active", "inactive", False)
            
        except Exception as e:
            Log.error(f"test_data_validation test failed: {str(e)}")
            Log.end_test("test_data_validation", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_data_validation", "PASSED")
    
    def test_step_logging(self):
        """Test step logging"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_step_logging")
        
        try:
            @Log.step("User registration step")
            def register_user():
                Log.info("Starting user registration process")
                
                @Log.step("Validate user information")
                def validate_user_info():
                    Log.info("Validating username and email")
                    return True
                
                @Log.step("Create user account")
                def create_account():
                    Log.info("Creating user account in database")
                    return {"user_id": 99999}
                
                # Execute steps
                validate_user_info()
                account = create_account()
                Log.info("User registration completed", account)
                return account
            
            # Execute registration process
            result = register_user()
            Log.info("Registration process execution completed", result)
            
        except Exception as e:
            Log.error(f"test_step_logging test failed: {str(e)}")
            Log.end_test("test_step_logging", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_step_logging", "PASSED")
    
    def test_error_handling(self):
        """Test error handling logging"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_error_handling")
        
        try:
            try:
                # Simulate an operation that might fail
                Log.info("Starting operation that might fail")
                
                # Simulate exception
                raise ValueError("This is a simulated error")
                
            except Exception as e:
                Log.error(f"Operation execution failed: {str(e)}")
                Log.info("Starting error recovery process")
                
                # Simulate error recovery
                Log.info("Error recovery completed")
            
        except Exception as e:
            Log.error(f"test_error_handling test failed: {str(e)}")
            Log.end_test("test_error_handling", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_error_handling", "PASSED")
    
    def test_performance_logging(self):
        """Test performance-related logging"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_performance_logging")
        
        try:
            import time
            
            Log.info("Starting performance test")
            
            # Simulate time-consuming operation
            start_time = time.time()
            time.sleep(0.1)  # Simulate 100ms operation
            end_time = time.time()
            
            duration = end_time - start_time
            Log.info(f"Operation duration: {duration:.3f} seconds")
            
            # Log performance metrics
            performance_data = {
                "operation": "data_processing",
                "duration_ms": duration * 1000,
                "status": "success"
            }
            Log.info("Performance metrics", performance_data)
            
        except Exception as e:
            Log.error(f"test_performance_logging test failed: {str(e)}")
            Log.end_test("test_performance_logging", "FAILED")
            raise
        else:
            # Final step: End test
            Log.end_test("test_performance_logging", "PASSED")


def test_standalone_function():
    """Standalone test function example"""
    # Step 1: Set LogID
    logid = generate_logid()
    Log.set_logid(logid)
    
    # Step 2: Start test
    Log.start_test("test_standalone_function")
    
    try:
        Log.info("Starting standalone function test")
        
        # Execute test logic
        Log.api_call("GET", "/api/health", 200, 0.1)
        Log.assertion("Health check", True, 200, 200)
        
        Log.info("Standalone function test completed")
        
    except Exception as e:
        Log.error(f"test_standalone_function test failed: {str(e)}")
        Log.end_test("test_standalone_function", "FAILED")
        raise
    else:
        # Final step: End test
        Log.end_test("test_standalone_function", "PASSED")


if __name__ == "__main__":
    # This file can be run directly for testing
    pytest.main([__file__, "-v"])
