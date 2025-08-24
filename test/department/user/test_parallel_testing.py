#!/usr/bin/env python3
"""
Demo: Parallel Testing Support
This file demonstrates how to use parallel testing features in PTE Framework.
"""

import pytest
import time
import random
from core.logger import Log, generate_logid


class TestParallelDemo:
    """Demo class for parallel testing features"""
    
    def test_parallel_safe_operation(self):
        """This test is safe to run in parallel - no shared state"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_parallel_safe_operation")
        
        # Test logic
        Log.info("Running parallel-safe test")
        time.sleep(random.uniform(0.1, 0.3))  # Simulate some work
        assert True
        Log.info("Parallel-safe test completed")
        
        # Final step: End test
        Log.end_test("test_parallel_safe_operation", "PASSED")
    
    @pytest.mark.parallel
    def test_explicitly_parallel_safe(self):
        """This test is explicitly marked as safe for parallel execution"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_explicitly_parallel_safe")
        
        # Test logic
        Log.info("Running explicitly parallel-safe test")
        time.sleep(random.uniform(0.1, 0.3))
        assert True
        Log.info("Explicitly parallel-safe test completed")
        
        # Final step: End test
        Log.end_test("test_explicitly_parallel_safe", "PASSED")
    
    @pytest.mark.no_parallel
    def test_not_parallel_safe(self):
        """This test should not run in parallel - has shared state"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_not_parallel_safe")
        
        # Test logic
        Log.info("Running non-parallel-safe test")
        time.sleep(random.uniform(0.1, 0.3))
        # This test might modify shared resources
        assert True
        Log.info("Non-parallel-safe test completed")
        
        # Final step: End test
        Log.end_test("test_not_parallel_safe", "PASSED")
    
    def test_database_operation(self):
        """Database operations should typically not run in parallel"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_database_operation")
        
        # Test logic
        Log.info("Running database operation test")
        time.sleep(random.uniform(0.2, 0.5))
        # Database operations should use no_parallel marker
        assert True
        Log.info("Database operation test completed")
        
        # Final step: End test
        Log.end_test("test_database_operation", "PASSED")
    
    @pytest.mark.parallel
    def test_api_call_safe(self):
        """API calls can often be safely parallelized"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_api_call_safe")
        
        # Test logic
        Log.info("Running API call test")
        time.sleep(random.uniform(0.1, 0.4))
        assert True
        Log.info("API call test completed")
        
        # Final step: End test
        Log.end_test("test_api_call_safe", "PASSED")


class TestParallelPerformance:
    """Performance comparison tests for parallel execution"""
    
    @pytest.mark.parallel
    def test_fast_parallel_operation(self):
        """Fast operation suitable for parallel execution"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_fast_parallel_operation")
        
        # Test logic
        Log.info("Running fast parallel operation")
        time.sleep(0.1)
        assert True
        Log.info("Fast parallel operation completed")
        
        # Final step: End test
        Log.end_test("test_fast_parallel_operation", "PASSED")
    
    @pytest.mark.parallel
    def test_medium_parallel_operation(self):
        """Medium duration operation suitable for parallel execution"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_medium_parallel_operation")
        
        # Test logic
        Log.info("Running medium parallel operation")
        time.sleep(0.3)
        assert True
        Log.info("Medium parallel operation completed")
        
        # Final step: End test
        Log.end_test("test_medium_parallel_operation", "PASSED")
    
    @pytest.mark.no_parallel
    def test_slow_sequential_operation(self):
        """Slow operation that should run sequentially"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_slow_sequential_operation")
        
        # Test logic
        Log.info("Running slow sequential operation")
        time.sleep(0.8)
        assert True
        Log.info("Slow sequential operation completed")
        
        # Final step: End test
        Log.end_test("test_slow_sequential_operation", "PASSED")


class TestParallelMarkers:
    """Tests demonstrating different parallel markers"""
    
    @pytest.mark.parallel
    def test_with_parallel_marker(self):
        """Test with explicit parallel marker"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_with_parallel_marker")
        
        # Test logic
        Log.info("Test with parallel marker")
        assert True
        
        # Final step: End test
        Log.end_test("test_with_parallel_marker", "PASSED")
    
    @pytest.mark.no_parallel
    def test_with_no_parallel_marker(self):
        """Test with explicit no_parallel marker"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_with_no_parallel_marker")
        
        # Test logic
        Log.info("Test with no_parallel marker")
        assert True
        
        # Final step: End test
        Log.end_test("test_with_no_parallel_marker", "PASSED")
    
    def test_without_marker(self):
        """Test without any parallel marker"""
        # Step 1: Set LogID
        logid = generate_logid()
        Log.set_logid(logid)
        
        # Step 2: Start test
        Log.start_test("test_without_marker")
        
        # Test logic
        Log.info("Test without any parallel marker")
        assert True
        
        # Final step: End test
        Log.end_test("test_without_marker", "PASSED")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
