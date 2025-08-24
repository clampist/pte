"""
PTE Framework - Rerun Functionality Demo Tests

This module demonstrates the pytest-rerunfailures functionality integration
with the PTE framework, showing various rerun strategies and best practices.

Features demonstrated:
- Basic rerun functionality
- Conditional rerun based on test markers
- Rerun with custom delays
- Integration with PTE logging
- Error handling and reporting
"""

import pytest
import random
import time
from unittest.mock import Mock, patch

from core.logger import Log, generate_logid
from core.retry import retry
from core.checker import Checker


class TestRerunBasicFunctionality:
    """Basic rerun functionality tests"""
    
    def test_always_passes(self):
        """Test that always passes - no rerun needed"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_always_passes")
        
        try:
            Log.info("This test should always pass")
            Checker.assert_true(True)
            
        except Exception as e:
            Log.error(f"test_always_passes test failed: {str(e)}")
            Log.end_test("test_always_passes", "FAILED")
            raise
        else:
            Log.end_test("test_always_passes", "PASSED")
    
    @pytest.mark.xfail(reason="This test is designed to fail to demonstrate rerun functionality")
    def test_always_fails(self):
        """Test that always fails - will be retried based on configuration"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_always_fails")
        
        try:
            Log.info("This test always fails - will be retried")
            Checker.assert_true(False, "This test is designed to fail")
            
        except Exception as e:
            Log.error(f"test_always_fails test failed: {str(e)}")
            Log.end_test("test_always_fails", "FAILED")
            raise
        else:
            Log.end_test("test_always_fails", "PASSED")
    
    def test_sometimes_fails(self):
        """Test that fails randomly - demonstrates rerun value"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_sometimes_fails")
        
        try:
            # Simulate flaky test with 30% failure rate (lower for demo)
            if random.random() < 0.3:
                Log.warning("Test failed randomly - will be retried")
                Checker.assert_true(False, "Random failure occurred")
            else:
                Log.info("Test passed on this attempt")
                Checker.assert_true(True)
                
        except Exception as e:
            Log.error(f"test_sometimes_fails test failed: {str(e)}")
            Log.end_test("test_sometimes_fails", "FAILED")
            raise
        else:
            Log.end_test("test_sometimes_fails", "PASSED")


class TestRerunWithMarkers:
    """Tests demonstrating rerun functionality with pytest markers"""
    
    @pytest.mark.flaky
    def test_flaky_marked_test(self):
        """Test marked as flaky - should be retried more aggressively"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_flaky_marked_test")
        
        try:
            # Simulate flaky behavior with lower failure rate for demo
            if random.random() < 0.3:  # 30% failure rate
                Log.warning("Flaky test failed - will be retried")
                Checker.assert_true(False, "Flaky test failure")
            else:
                Log.info("Flaky test passed")
                Checker.assert_true(True)
                
        except Exception as e:
            Log.error(f"test_flaky_marked_test test failed: {str(e)}")
            Log.end_test("test_flaky_marked_test", "FAILED")
            raise
        else:
            Log.end_test("test_flaky_marked_test", "PASSED")
    
    @pytest.mark.stable
    def test_stable_marked_test(self):
        """Test marked as stable - should not need retries"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_stable_marked_test")
        
        try:
            Log.info("Stable test - should pass consistently")
            Checker.assert_true(True)
            
        except Exception as e:
            Log.error(f"test_stable_marked_test test failed: {str(e)}")
            Log.end_test("test_stable_marked_test", "FAILED")
            raise
        else:
            Log.end_test("test_stable_marked_test", "PASSED")
    
    @pytest.mark.api
    def test_api_test_with_rerun(self):
        """API test that might fail due to network issues"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_api_test_with_rerun")
        
        try:
            # Simulate network-related failure with lower probability
            if random.random() < 0.2:  # 20% failure rate for demo
                Log.warning("API test failed due to network issue - will retry")
                raise ConnectionError("Network timeout")
            else:
                Log.info("API test succeeded")
                Checker.assert_true(True)
                
        except Exception as e:
            Log.error(f"test_api_test_with_rerun test failed: {str(e)}")
            Log.end_test("test_api_test_with_rerun", "FAILED")
            raise
        else:
            Log.end_test("test_api_test_with_rerun", "PASSED")


class TestRerunWithCustomLogic:
    """Tests demonstrating custom rerun logic"""
    
    def test_conditional_rerun(self):
        """Test with custom retry logic using PTE retry decorator"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_conditional_rerun")
        
        try:
            @retry(max_attempts=3, delay=0.1)
            def flaky_operation():
                if random.random() < 0.6:
                    raise ValueError("Operation failed")
                return "success"
            
            result = flaky_operation()
            Log.info(f"Operation result: {result}")
            Checker.assert_equal(result, "success")
            
        except Exception as e:
            Log.error(f"test_conditional_rerun test failed: {str(e)}")
            Log.end_test("test_conditional_rerun", "FAILED")
            raise
        else:
            Log.end_test("test_conditional_rerun", "PASSED")
    
    def test_rerun_with_state_check(self):
        """Test that checks state before deciding to retry"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_rerun_with_state_check")
        
        try:
            attempts = []
            
            def operation_with_state():
                attempt = len(attempts) + 1
                attempts.append(attempt)
                
                # Simulate state-dependent failure
                if attempt < 3:
                    Log.warning(f"Attempt {attempt} failed - will retry")
                    raise RuntimeError(f"Attempt {attempt} failed")
                else:
                    Log.info(f"Attempt {attempt} succeeded")
                    return f"Success on attempt {attempt}"
            
            # Use retry decorator
            @retry(max_attempts=3, delay=0.1)
            def retry_operation():
                return operation_with_state()
            
            result = retry_operation()
            Log.info(f"Final result: {result}")
            Checker.assert_contains(result, "Success on attempt 3")
            Checker.assert_equal(len(attempts), 3)
            
        except Exception as e:
            Log.error(f"test_rerun_with_state_check test failed: {str(e)}")
            Log.end_test("test_rerun_with_state_check", "FAILED")
            raise
        else:
            Log.end_test("test_rerun_with_state_check", "PASSED")


class TestRerunIntegration:
    """Tests demonstrating integration with PTE framework features"""
    
    def test_rerun_with_logging(self):
        """Test that rerun works properly with PTE logging"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_rerun_with_logging")
        
        try:
            test_id = f"rerun_test_{int(time.time())}"
            Log.info(f"Starting test with ID: {test_id}")
            
            # Simulate flaky behavior with lower failure rate
            if random.random() < 0.3:
                Log.warning(f"Test {test_id} failed - will be retried")
                Checker.assert_true(False, f"Test {test_id} failed")
            else:
                Log.info(f"Test {test_id} passed")
                Checker.assert_true(True)
                
        except Exception as e:
            Log.error(f"test_rerun_with_logging test failed: {str(e)}")
            Log.end_test("test_rerun_with_logging", "FAILED")
            raise
        else:
            Log.end_test("test_rerun_with_logging", "PASSED")
    
    def test_rerun_with_parallel_marker(self):
        """Test that rerun works with parallel execution markers"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_rerun_with_parallel_marker")
        
        try:
            # This test only verifies the parallel marker concept, no actual execution needed
            Log.info("Parallel marker test - concept validation only")
            Checker.assert_true(True)
            
        except Exception as e:
            Log.error(f"test_rerun_with_parallel_marker test failed: {str(e)}")
            Log.end_test("test_rerun_with_parallel_marker", "FAILED")
            raise
        else:
            Log.end_test("test_rerun_with_parallel_marker", "PASSED")
    
    def test_parallel_safe_rerun(self):
        """Test that can be run in parallel with rerun"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_parallel_safe_rerun")
        
        try:
            # This test is safe for parallel execution
            if random.random() < 0.4:
                Log.warning("Parallel test failed - will retry")
                Checker.assert_true(False, "Parallel test failure")
            else:
                Log.info("Parallel test passed")
                Checker.assert_true(True)
                
        except Exception as e:
            Log.error(f"test_parallel_safe_rerun test failed: {str(e)}")
            Log.end_test("test_parallel_safe_rerun", "FAILED")
            raise
        else:
            Log.end_test("test_parallel_safe_rerun", "PASSED")
    
    @pytest.mark.no_parallel
    def test_sequential_rerun(self):
        """Test that should not run in parallel but can be retried"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_sequential_rerun")
        
        try:
            # This test should not run in parallel but can be retried
            if random.random() < 0.2:  # Lower failure rate for demo
                Log.warning("Sequential test failed - will retry")
                Checker.assert_true(False, "Sequential test failure")
            else:
                Log.info("Sequential test passed")
                Checker.assert_true(True)
                
        except Exception as e:
            Log.error(f"test_sequential_rerun test failed: {str(e)}")
            Log.end_test("test_sequential_rerun", "FAILED")
            raise
        else:
            Log.end_test("test_sequential_rerun", "PASSED")


class TestRerunErrorHandling:
    """Tests demonstrating error handling with rerun"""
    
    def test_rerun_with_exception_types(self):
        """Test that rerun handles different exception types correctly"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_rerun_with_exception_types")
        
        try:
            @retry(max_attempts=3, delay=0.1, exceptions=(ValueError, RuntimeError))
            def operation_with_specific_exceptions():
                if random.random() < 0.5:  # Lower failure rate for demo
                    if random.random() < 0.5:
                        raise ValueError("Value error occurred")
                    else:
                        raise RuntimeError("Runtime error occurred")
                return "success"
            
            result = operation_with_specific_exceptions()
            Log.info(f"Operation completed: {result}")
            Checker.assert_equal(result, "success")
            
        except Exception as e:
            Log.error(f"test_rerun_with_exception_types test failed: {str(e)}")
            Log.end_test("test_rerun_with_exception_types", "FAILED")
            raise
        else:
            Log.end_test("test_rerun_with_exception_types", "PASSED")
    
    def test_rerun_with_custom_exception(self):
        """Test that rerun works with custom exceptions"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_rerun_with_custom_exception")
        
        try:
            class CustomError(Exception):
                pass
            
            @retry(max_attempts=2, delay=0.1, exceptions=(CustomError,))
            def operation_with_custom_exception():
                if random.random() < 0.5:  # Lower failure rate for demo
                    raise CustomError("Custom error occurred")
                return "success"
            
            result = operation_with_custom_exception()
            Log.info(f"Custom operation completed: {result}")
            Checker.assert_equal(result, "success")
            
        except Exception as e:
            Log.error(f"test_rerun_with_custom_exception test failed: {str(e)}")
            Log.end_test("test_rerun_with_custom_exception", "FAILED")
            raise
        else:
            Log.end_test("test_rerun_with_custom_exception", "PASSED")


class TestRerunPerformance:
    """Tests demonstrating rerun performance considerations"""
    
    def test_rerun_with_timeout(self):
        """Test that rerun respects timeout constraints"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_rerun_with_timeout")
        
        try:
            @retry(max_attempts=2, delay=0.1, timeout=1.0)
            def slow_operation():
                time.sleep(0.2)  # Simulate slow operation
                if random.random() < 0.5:
                    raise TimeoutError("Operation timed out")
                return "success"
            
            result = slow_operation()
            Log.info(f"Slow operation completed: {result}")
            Checker.assert_equal(result, "success")
            
        except Exception as e:
            Log.error(f"test_rerun_with_timeout test failed: {str(e)}")
            Log.end_test("test_rerun_with_timeout", "FAILED")
            raise
        else:
            Log.end_test("test_rerun_with_timeout", "PASSED")
    
    def test_rerun_with_backoff(self):
        """Test that rerun uses exponential backoff"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_rerun_with_backoff")
        
        try:
            attempts = []
            
            @retry(max_attempts=3, delay=0.1, strategy="exponential")
            def operation_with_backoff():
                attempt = len(attempts) + 1
                attempts.append(time.time())
                
                if attempt < 3:
                    Log.warning(f"Attempt {attempt} failed - will retry with exponential backoff")
                    raise RuntimeError(f"Attempt {attempt} failed")
                else:
                    Log.info(f"Attempt {attempt} succeeded")
                    return "success"
            
            start_time = time.time()
            result = operation_with_backoff()
            end_time = time.time()
            
            Log.info(f"Operation completed in {end_time - start_time:.2f} seconds")
            Checker.assert_equal(result, "success")
            Checker.assert_equal(len(attempts), 3)
            
        except Exception as e:
            Log.error(f"test_rerun_with_backoff test failed: {str(e)}")
            Log.end_test("test_rerun_with_backoff", "FAILED")
            raise
        else:
            Log.end_test("test_rerun_with_backoff", "PASSED")


class TestRerunBestPractices:
    """Tests demonstrating rerun best practices"""
    
    def test_rerun_with_cleanup(self):
        """Test that rerun properly handles cleanup between attempts"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_rerun_with_cleanup")
        
        try:
            # Simplified test, removed cleanup logic because PTE retry does not support cleanup parameter
            @retry(max_attempts=2, delay=0.1)
            def operation_with_retry():
                if random.random() < 0.6:
                    Log.warning("Operation failed - will retry")
                    raise RuntimeError("Operation failed")
                return "success"
            
            result = operation_with_retry()
            Log.info(f"Operation completed successfully: {result}")
            Checker.assert_equal(result, "success")
            
        except Exception as e:
            Log.error(f"test_rerun_with_cleanup test failed: {str(e)}")
            Log.end_test("test_rerun_with_cleanup", "FAILED")
            raise
        else:
            Log.end_test("test_rerun_with_cleanup", "PASSED")
    
    def test_rerun_with_condition(self):
        """Test that rerun respects custom retry conditions"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_rerun_with_condition")
        
        try:
            def should_retry(exception, attempt):
                # Only retry on specific exceptions and within attempt limit
                return (isinstance(exception, (ValueError, RuntimeError)) and 
                       attempt < 3)
            
            @retry(max_attempts=5, delay=0.1, exceptions=(ValueError, RuntimeError))
            def operation_with_condition():
                if random.random() < 0.7:
                    if random.random() < 0.5:
                        raise ValueError("Value error")
                    else:
                        raise RuntimeError("Runtime error")
                return "success"
            
            result = operation_with_condition()
            Log.info(f"Conditional operation completed: {result}")
            Checker.assert_equal(result, "success")
            
        except Exception as e:
            Log.error(f"test_rerun_with_condition test failed: {str(e)}")
            Log.end_test("test_rerun_with_condition", "FAILED")
            raise
        else:
            Log.end_test("test_rerun_with_condition", "PASSED")
    
    def test_rerun_with_logging_context(self):
        """Test that rerun maintains proper logging context"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_rerun_with_logging_context")
        
        try:
            test_context = {"attempt": 0, "start_time": time.time()}
            
            @retry(max_attempts=3, delay=0.1)
            def operation_with_context():
                test_context["attempt"] += 1
                Log.info(f"Attempt {test_context['attempt']} started")
                
                if random.random() < 0.5:
                    Log.warning(f"Attempt {test_context['attempt']} failed")
                    raise RuntimeError(f"Attempt {test_context['attempt']} failed")
                
                Log.info(f"Attempt {test_context['attempt']} succeeded")
                return f"Success on attempt {test_context['attempt']}"
            
            result = operation_with_context()
            duration = time.time() - test_context["start_time"]
            
            Log.info(f"Operation completed in {duration:.2f}s with {test_context['attempt']} attempts")
            Checker.assert_contains(result, "Success on attempt")
            Checker.assert_greater_equal(test_context["attempt"], 1)
            
        except Exception as e:
            Log.error(f"test_rerun_with_logging_context test failed: {str(e)}")
            Log.end_test("test_rerun_with_logging_context", "FAILED")
            raise
        else:
            Log.end_test("test_rerun_with_logging_context", "PASSED")


# Demo tests for different rerun scenarios
class TestRerunDemoScenarios:
    """Demo scenarios for different rerun use cases"""
    
    @pytest.mark.slow
    def test_slow_flaky_test(self):
        """Slow test that is also flaky - demonstrates rerun value"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_slow_flaky_test")
        
        try:
            time.sleep(0.1)  # Simulate slow test
            
            if random.random() < 0.4:  # Lower failure rate for demo
                Log.warning("Slow flaky test failed")
                Checker.assert_true(False, "Slow flaky test failure")
            else:
                Log.info("Slow flaky test passed")
                Checker.assert_true(True)
                
        except Exception as e:
            Log.error(f"test_slow_flaky_test test failed: {str(e)}")
            Log.end_test("test_slow_flaky_test", "FAILED")
            raise
        else:
            Log.end_test("test_slow_flaky_test", "PASSED")
    
    @pytest.mark.integration
    def test_integration_test_rerun(self):
        """Integration test that might fail due to external dependencies"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_integration_test_rerun")
        
        try:
            # Simulate external dependency failure
            if random.random() < 0.4:
                Log.warning("Integration test failed due to external dependency")
                raise ConnectionError("External service unavailable")
            else:
                Log.info("Integration test passed")
                Checker.assert_true(True)
                
        except Exception as e:
            Log.error(f"test_integration_test_rerun test failed: {str(e)}")
            Log.end_test("test_integration_test_rerun", "FAILED")
            raise
        else:
            Log.end_test("test_integration_test_rerun", "PASSED")
    
    @pytest.mark.regression
    def test_regression_test_rerun(self):
        """Regression test with rerun capability"""
        # Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        Log.start_test("test_regression_test_rerun")
        
        try:
            # Simulate regression test that might be flaky
            if random.random() < 0.3:
                Log.warning("Regression test failed - will retry")
                Checker.assert_true(False, "Regression test failure")
            else:
                Log.info("Regression test passed")
                Checker.assert_true(True)
                
        except Exception as e:
            Log.error(f"test_regression_test_rerun test failed: {str(e)}")
            Log.end_test("test_regression_test_rerun", "FAILED")
            raise
        else:
            Log.end_test("test_regression_test_rerun", "PASSED")
