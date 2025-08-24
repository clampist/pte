#!/usr/bin/env python3
"""
Demo: Parallel Testing Support
This file demonstrates how to use parallel testing features in PTE Framework.
"""

import pytest
import time
import random
from core.logger import Log


class TestParallelDemo:
    """Demo class for parallel testing features"""
    
    def test_parallel_safe_operation(self):
        """This test is safe to run in parallel - no shared state"""
        Log.info("Running parallel-safe test")
        time.sleep(random.uniform(0.1, 0.3))  # Simulate some work
        assert True
        Log.info("Parallel-safe test completed")
    
    @pytest.mark.parallel
    def test_explicitly_parallel_safe(self):
        """This test is explicitly marked as safe for parallel execution"""
        Log.info("Running explicitly parallel-safe test")
        time.sleep(random.uniform(0.1, 0.3))
        assert True
        Log.info("Explicitly parallel-safe test completed")
    
    @pytest.mark.no_parallel
    def test_not_parallel_safe(self):
        """This test should not run in parallel - has shared state"""
        Log.info("Running non-parallel-safe test")
        time.sleep(random.uniform(0.1, 0.3))
        # This test might modify shared resources
        assert True
        Log.info("Non-parallel-safe test completed")
    
    def test_database_operation(self):
        """Database operations should typically not run in parallel"""
        Log.info("Running database operation test")
        time.sleep(random.uniform(0.2, 0.5))
        # Database operations should use no_parallel marker
        assert True
        Log.info("Database operation test completed")
    
    @pytest.mark.parallel
    def test_api_call_safe(self):
        """API calls can often be safely parallelized"""
        Log.info("Running API call test")
        time.sleep(random.uniform(0.1, 0.4))
        assert True
        Log.info("API call test completed")


class TestParallelPerformance:
    """Performance comparison tests for parallel execution"""
    
    @pytest.mark.parallel
    def test_fast_parallel_operation(self):
        """Fast operation suitable for parallel execution"""
        Log.info("Running fast parallel operation")
        time.sleep(0.1)
        assert True
        Log.info("Fast parallel operation completed")
    
    @pytest.mark.parallel
    def test_medium_parallel_operation(self):
        """Medium duration operation suitable for parallel execution"""
        Log.info("Running medium parallel operation")
        time.sleep(0.3)
        assert True
        Log.info("Medium parallel operation completed")
    
    @pytest.mark.no_parallel
    def test_slow_sequential_operation(self):
        """Slow operation that should run sequentially"""
        Log.info("Running slow sequential operation")
        time.sleep(0.8)
        assert True
        Log.info("Slow sequential operation completed")


class TestParallelMarkers:
    """Tests demonstrating different parallel markers"""
    
    @pytest.mark.parallel
    def test_with_parallel_marker(self):
        """Test with explicit parallel marker"""
        Log.info("Test with parallel marker")
        assert True
    
    @pytest.mark.no_parallel
    def test_with_no_parallel_marker(self):
        """Test with explicit no_parallel marker"""
        Log.info("Test with no_parallel marker")
        assert True
    
    def test_without_marker(self):
        """Test without any parallel marker - will be auto-detected"""
        Log.info("Test without parallel marker")
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
