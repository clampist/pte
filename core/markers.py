"""
Core test markers - encapsulates pytest markers
"""
import pytest


# Custom markers for different test types
@pytest.mark.slow
def slow_test():
    """Marker for slow tests"""
    pass


@pytest.mark.integration
def integration_test():
    """Marker for integration tests"""
    pass


@pytest.mark.unit
def unit_test():
    """Marker for unit tests"""
    pass


@pytest.mark.api
def api_test():
    """Marker for API tests"""
    pass


@pytest.mark.smoke
def smoke_test():
    """Marker for smoke tests"""
    pass


@pytest.mark.regression
def regression_test():
    """Marker for regression tests"""
    pass


# Helper functions for test categorization
def is_slow_test(func):
    """Check if test is marked as slow"""
    return hasattr(func, 'pytestmark') and any(
        mark.name == 'slow' for mark in func.pytestmark
    )


def is_integration_test(func):
    """Check if test is marked as integration"""
    return hasattr(func, 'pytestmark') and any(
        mark.name == 'integration' for mark in func.pytestmark
    )


def is_unit_test(func):
    """Check if test is marked as unit"""
    return hasattr(func, 'pytestmark') and any(
        mark.name == 'unit' for mark in func.pytestmark
    )
