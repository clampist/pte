"""
PTE Framework Enhanced Retry Module
Provides advanced retry functionality with multiple strategies and conditions
"""
import time
import functools
import inspect
import random
from typing import Optional, Callable, Any, Dict, List, Union, Type, Tuple
from enum import Enum
import logging
from datetime import datetime, timedelta

from .logger import Log


class RetryStrategy(Enum):
    """Retry strategies enumeration"""
    FIXED = "fixed"           # Fixed delay between retries
    EXPONENTIAL = "exponential"  # Exponential backoff
    LINEAR = "linear"         # Linear backoff
    RANDOM = "random"         # Random delay
    FIBONACCI = "fibonacci"   # Fibonacci backoff


class RetryCondition(Enum):
    """Retry condition types"""
    EXCEPTION = "exception"   # Retry on specific exceptions
    RESULT = "result"         # Retry based on return value
    TIMEOUT = "timeout"       # Retry on timeout
    CUSTOM = "custom"         # Custom condition function


class RetryConfig:
    """Configuration class for retry behavior"""
    
    def __init__(
        self,
        max_attempts: int = 3,
        delay: float = 1.0,
        max_delay: float = 60.0,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
        exceptions: Tuple[Type[Exception], ...] = (Exception,),
        timeout: Optional[float] = None,
        jitter: bool = True,
        jitter_factor: float = 0.1,
        log_retries: bool = True,
        log_level: str = "WARNING"
    ):
        self.max_attempts = max_attempts
        self.delay = delay
        self.max_delay = max_delay
        self.strategy = strategy
        self.exceptions = exceptions
        self.timeout = timeout
        self.jitter = jitter
        self.jitter_factor = jitter_factor
        self.log_retries = log_retries
        self.log_level = log_level


class RetryConditionChecker:
    """Helper class for checking retry conditions"""
    
    @staticmethod
    def check_exception_condition(exception: Exception, target_exceptions: Tuple[Type[Exception], ...]) -> bool:
        """Check if exception matches retry condition"""
        return isinstance(exception, target_exceptions)
    
    @staticmethod
    def check_result_condition(result: Any, condition_func: Callable[[Any], bool]) -> bool:
        """Check if result matches retry condition"""
        try:
            return condition_func(result)
        except Exception:
            return False
    
    @staticmethod
    def check_timeout_condition(start_time: float, timeout: float) -> bool:
        """Check if timeout condition is met"""
        return time.time() - start_time >= timeout


class RetryDelayCalculator:
    """Helper class for calculating retry delays"""
    
    @staticmethod
    def calculate_delay(
        attempt: int,
        base_delay: float,
        max_delay: float,
        strategy: RetryStrategy,
        jitter: bool = True,
        jitter_factor: float = 0.1
    ) -> float:
        """Calculate delay for current attempt"""
        
        if strategy == RetryStrategy.FIXED:
            delay = base_delay
        elif strategy == RetryStrategy.EXPONENTIAL:
            delay = base_delay * (2 ** (attempt - 1))
        elif strategy == RetryStrategy.LINEAR:
            delay = base_delay * attempt
        elif strategy == RetryStrategy.RANDOM:
            delay = random.uniform(0, base_delay * (2 ** (attempt - 1)))
        elif strategy == RetryStrategy.FIBONACCI:
            delay = base_delay * RetryDelayCalculator._fibonacci(attempt)
        else:
            delay = base_delay
        
        # Apply jitter if enabled
        if jitter:
            jitter_amount = delay * jitter_factor
            delay += random.uniform(-jitter_amount, jitter_amount)
        
        # Ensure delay is within bounds
        delay = max(0, min(delay, max_delay))
        
        return delay
    
    @staticmethod
    def _fibonacci(n: int) -> int:
        """Calculate fibonacci number"""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    max_delay: float = 60.0,
    strategy: Union[RetryStrategy, str] = RetryStrategy.EXPONENTIAL,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    timeout: Optional[float] = None,
    jitter: bool = True,
    jitter_factor: float = 0.1,
    log_retries: bool = True,
    log_level: str = "WARNING"
):
    """
    Enhanced retry decorator with multiple strategies and conditions
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Base delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        strategy: Retry strategy (fixed, exponential, linear, random, fibonacci)
        exceptions: Tuple of exceptions to retry on
        timeout: Overall timeout for all attempts (seconds)
        jitter: Whether to add random jitter to delays
        jitter_factor: Jitter factor (0.0 to 1.0)
        log_retries: Whether to log retry attempts
        log_level: Log level for retry messages
    
    Examples:
        @retry(max_attempts=3, delay=2.0, strategy="exponential")
        def my_function():
            pass
            
        @retry(max_attempts=5, exceptions=(ValueError, TypeError))
        def another_function():
            pass
    """
    
    # Convert string strategy to enum
    if isinstance(strategy, str):
        try:
            strategy = RetryStrategy(strategy.lower())
        except ValueError:
            strategy = RetryStrategy.EXPONENTIAL
    
    config = RetryConfig(
        max_attempts=max_attempts,
        delay=delay,
        max_delay=max_delay,
        strategy=strategy,
        exceptions=exceptions,
        timeout=timeout,
        jitter=jitter,
        jitter_factor=jitter_factor,
        log_retries=log_retries,
        log_level=log_level
    )
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            last_exception = None
            
            for attempt in range(1, config.max_attempts + 1):
                try:
                    # Check timeout before attempt
                    if config.timeout and RetryConditionChecker.check_timeout_condition(start_time, config.timeout):
                        if config.log_retries:
                            Log.warning(f"Retry timeout reached after {config.timeout}s for {func.__name__}")
                        raise TimeoutError(f"Retry timeout reached after {config.timeout}s")
                    
                    # Execute function
                    result = func(*args, **kwargs)
                    
                    # Success - return result
                    if attempt > 1 and config.log_retries:
                        Log.info(f"Function {func.__name__} succeeded on attempt {attempt}")
                    return result
                    
                except config.exceptions as e:
                    last_exception = e
                    
                    # Check if we should retry
                    if attempt >= config.max_attempts:
                        if config.log_retries:
                            Log.error(f"Function {func.__name__} failed after {config.max_attempts} attempts. "
                                    f"Last exception: {type(e).__name__}: {str(e)}")
                        raise
                    
                    # Calculate delay
                    delay = RetryDelayCalculator.calculate_delay(
                        attempt, config.delay, config.max_delay, config.strategy,
                        config.jitter, config.jitter_factor
                    )
                    
                    # Log retry attempt
                    if config.log_retries:
                        log_message = (f"Function {func.__name__} failed on attempt {attempt}/{config.max_attempts}. "
                                     f"Retrying in {delay:.2f}s. Exception: {type(e).__name__}: {str(e)}")
                        if config.log_level.upper() == "DEBUG":
                            Log.debug(log_message)
                        elif config.log_level.upper() == "INFO":
                            Log.info(log_message)
                        else:
                            Log.warning(log_message)
                    
                    # Wait before retry
                    time.sleep(delay)
                    
                except Exception as e:
                    # Non-retryable exception
                    if config.log_retries:
                        Log.error(f"Function {func.__name__} failed with non-retryable exception: {type(e).__name__}: {str(e)}")
                    raise
            
            # This should never be reached, but just in case
            if last_exception:
                raise last_exception
        
        return wrapper
    
    return decorator


def retry_with_condition(
    condition: Union[Callable[[Any], bool], Dict[str, Any]],
    max_attempts: int = 3,
    delay: float = 1.0,
    max_delay: float = 60.0,
    strategy: Union[RetryStrategy, str] = RetryStrategy.EXPONENTIAL,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    timeout: Optional[float] = None,
    jitter: bool = True,
    jitter_factor: float = 0.1,
    log_retries: bool = True,
    log_level: str = "WARNING"
):
    """
    Retry decorator with custom condition checking
    
    Args:
        condition: Condition function or dict with condition rules
        max_attempts: Maximum number of retry attempts
        delay: Base delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        strategy: Retry strategy
        exceptions: Tuple of exceptions to retry on
        timeout: Overall timeout for all attempts (seconds)
        jitter: Whether to add random jitter to delays
        jitter_factor: Jitter factor (0.0 to 1.0)
        log_retries: Whether to log retry attempts
        log_level: Log level for retry messages
    
    Examples:
        # Using condition function
        @retry_with_condition(lambda result: result is None)
        def my_function():
            pass
            
        # Using condition dict
        @retry_with_condition({"status": "pending", "code": 200})
        def api_call():
            pass
            
        # Using condition dict with operators
        @retry_with_condition({"count": {"operator": "lt", "value": 5}})
        def count_items():
            pass
    """
    
    # Convert string strategy to enum
    if isinstance(strategy, str):
        try:
            strategy = RetryStrategy(strategy.lower())
        except ValueError:
            strategy = RetryStrategy.EXPONENTIAL
    
    config = RetryConfig(
        max_attempts=max_attempts,
        delay=delay,
        max_delay=max_delay,
        strategy=strategy,
        exceptions=exceptions,
        timeout=timeout,
        jitter=jitter,
        jitter_factor=jitter_factor,
        log_retries=log_retries,
        log_level=log_level
    )
    
    def create_condition_checker(condition):
        """Create condition checker function"""
        if callable(condition):
            return condition
        
        if isinstance(condition, dict):
            def dict_condition_checker(result):
                if not isinstance(result, dict):
                    return False
                
                for key, expected_value in condition.items():
                    if key not in result:
                        return False
                    
                    actual_value = result[key]
                    
                    if isinstance(expected_value, dict) and "operator" in expected_value:
                        # Handle operators
                        operator = expected_value["operator"]
                        value = expected_value["value"]
                        
                        if operator == "eq" and actual_value != value:
                            return False
                        elif operator == "ne" and actual_value == value:
                            return False
                        elif operator == "gt" and actual_value <= value:
                            return False
                        elif operator == "gte" and actual_value < value:
                            return False
                        elif operator == "lt" and actual_value >= value:
                            return False
                        elif operator == "lte" and actual_value > value:
                            return False
                        elif operator == "in" and actual_value not in value:
                            return False
                        elif operator == "not_in" and actual_value in value:
                            return False
                        elif operator == "contains" and value not in str(actual_value):
                            return False
                        elif operator == "not_contains" and value in str(actual_value):
                            return False
                        elif operator == "not_empty" and (actual_value is None or len(actual_value) == 0):
                            return False
                    else:
                        # Direct comparison
                        if actual_value != expected_value:
                            return False
                
                return True
            
            return dict_condition_checker
        
        # Default condition (always retry)
        return lambda result: True
    
    condition_checker = create_condition_checker(condition)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            last_exception = None
            
            for attempt in range(1, config.max_attempts + 1):
                try:
                    # Check timeout before attempt
                    if config.timeout and RetryConditionChecker.check_timeout_condition(start_time, config.timeout):
                        if config.log_retries:
                            Log.warning(f"Retry timeout reached after {config.timeout}s for {func.__name__}")
                        raise TimeoutError(f"Retry timeout reached after {config.timeout}s")
                    
                    # Execute function
                    result = func(*args, **kwargs)
                    
                    # Check condition
                    if condition_checker(result):
                        # Condition satisfied, return result
                        if attempt > 1 and config.log_retries:
                            Log.info(f"Function {func.__name__} condition satisfied on attempt {attempt}")
                        return result
                    else:
                        # Condition not met, retry needed
                        if attempt >= config.max_attempts:
                            if config.log_retries:
                                Log.error(f"Function {func.__name__} condition not satisfied after {config.max_attempts} attempts. "
                                        f"Last result: {result}")
                            return result
                        
                        # Calculate delay
                        delay = RetryDelayCalculator.calculate_delay(
                            attempt, config.delay, config.max_delay, config.strategy,
                            config.jitter, config.jitter_factor
                        )
                        
                        # Log retry attempt
                        if config.log_retries:
                            log_message = (f"Function {func.__name__} condition not satisfied on attempt {attempt}/{config.max_attempts}. "
                                         f"Retrying in {delay:.2f}s. Result: {result}")
                            if config.log_level.upper() == "DEBUG":
                                Log.debug(log_message)
                            elif config.log_level.upper() == "INFO":
                                Log.info(log_message)
                            else:
                                Log.warning(log_message)
                        
                        # Wait before retry
                        time.sleep(delay)
                    
                except config.exceptions as e:
                    last_exception = e
                    
                    # Check if we should retry
                    if attempt >= config.max_attempts:
                        if config.log_retries:
                            Log.error(f"Function {func.__name__} failed after {config.max_attempts} attempts. "
                                    f"Last exception: {type(e).__name__}: {str(e)}")
                        raise
                    
                    # Calculate delay
                    delay = RetryDelayCalculator.calculate_delay(
                        attempt, config.delay, config.max_delay, config.strategy,
                        config.jitter, config.jitter_factor
                    )
                    
                    # Log retry attempt
                    if config.log_retries:
                        log_message = (f"Function {func.__name__} failed on attempt {attempt}/{config.max_attempts}. "
                                     f"Retrying in {delay:.2f}s. Exception: {type(e).__name__}: {str(e)}")
                        if config.log_level.upper() == "DEBUG":
                            Log.debug(log_message)
                        elif config.log_level.upper() == "INFO":
                            Log.info(log_message)
                        else:
                            Log.warning(log_message)
                    
                    # Wait before retry
                    time.sleep(delay)
                    
                except Exception as e:
                    # Non-retryable exception
                    if config.log_retries:
                        Log.error(f"Function {func.__name__} failed with non-retryable exception: {type(e).__name__}: {str(e)}")
                    raise
            
            # This should never be reached, but just in case
            if last_exception:
                raise last_exception
        
        return wrapper
    
    return decorator


# Convenience decorators for common use cases
def retry_on_exception(
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    max_attempts: int = 3,
    delay: float = 1.0,
    max_delay: float = 60.0,
    strategy: Union[RetryStrategy, str] = RetryStrategy.EXPONENTIAL,
    timeout: Optional[float] = None,
    jitter: bool = True,
    jitter_factor: float = 0.1,
    log_retries: bool = True,
    log_level: str = "WARNING"
):
    """Simple retry decorator for exception handling"""
    return retry(
        max_attempts=max_attempts,
        delay=delay,
        max_delay=max_delay,
        strategy=strategy,
        exceptions=exceptions,
        timeout=timeout,
        jitter=jitter,
        jitter_factor=jitter_factor,
        log_retries=log_retries,
        log_level=log_level
    )


def retry_on_timeout(
    timeout: float = 30.0,
    max_attempts: int = 3,
    delay: float = 1.0,
    max_delay: float = 60.0,
    strategy: Union[RetryStrategy, str] = RetryStrategy.EXPONENTIAL,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    jitter: bool = True,
    jitter_factor: float = 0.1,
    log_retries: bool = True,
    log_level: str = "WARNING"
):
    """Retry decorator with timeout"""
    return retry(
        max_attempts=max_attempts,
        delay=delay,
        max_delay=max_delay,
        strategy=strategy,
        exceptions=exceptions,
        timeout=timeout,
        jitter=jitter,
        jitter_factor=jitter_factor,
        log_retries=log_retries,
        log_level=log_level
    )


def retry_until_success(
    max_attempts: int = 5,
    delay: float = 2.0,
    max_delay: float = 60.0,
    strategy: Union[RetryStrategy, str] = RetryStrategy.EXPONENTIAL,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    timeout: Optional[float] = None,
    jitter: bool = True,
    jitter_factor: float = 0.1,
    log_retries: bool = True,
    log_level: str = "WARNING"
):
    """Retry until success with exponential backoff"""
    return retry(
        max_attempts=max_attempts,
        delay=delay,
        max_delay=max_delay,
        strategy=strategy,
        exceptions=exceptions,
        timeout=timeout,
        jitter=jitter,
        jitter_factor=jitter_factor,
        log_retries=log_retries,
        log_level=log_level
    )


def retry_on_false(
    max_attempts: int = 3,
    delay: float = 1.0,
    max_delay: float = 60.0,
    strategy: Union[RetryStrategy, str] = RetryStrategy.EXPONENTIAL,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    timeout: Optional[float] = None,
    jitter: bool = True,
    jitter_factor: float = 0.1,
    log_retries: bool = True,
    log_level: str = "WARNING"
):
    """Retry when function returns False"""
    return retry_with_condition(
        lambda result: result is not False,
        max_attempts=max_attempts,
        delay=delay,
        max_delay=max_delay,
        strategy=strategy,
        exceptions=exceptions,
        timeout=timeout,
        jitter=jitter,
        jitter_factor=jitter_factor,
        log_retries=log_retries,
        log_level=log_level
    )


def retry_on_none(
    max_attempts: int = 3,
    delay: float = 1.0,
    max_delay: float = 60.0,
    strategy: Union[RetryStrategy, str] = RetryStrategy.EXPONENTIAL,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    timeout: Optional[float] = None,
    jitter: bool = True,
    jitter_factor: float = 0.1,
    log_retries: bool = True,
    log_level: str = "WARNING"
):
    """Retry when function returns None"""
    return retry_with_condition(
        lambda result: result is not None,
        max_attempts=max_attempts,
        delay=delay,
        max_delay=max_delay,
        strategy=strategy,
        exceptions=exceptions,
        timeout=timeout,
        jitter=jitter,
        jitter_factor=jitter_factor,
        log_retries=log_retries,
        log_level=log_level
    )


def retry_on_empty(
    max_attempts: int = 3,
    delay: float = 1.0,
    max_delay: float = 60.0,
    strategy: Union[RetryStrategy, str] = RetryStrategy.EXPONENTIAL,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    timeout: Optional[float] = None,
    jitter: bool = True,
    jitter_factor: float = 0.1,
    log_retries: bool = True,
    log_level: str = "WARNING"
):
    """Retry when function returns empty result (None, empty list, empty dict, empty string)"""
    def is_not_empty(result):
        if result is None:
            return False
        if isinstance(result, (list, dict, str)) and len(result) == 0:
            return False
        return True
    
    return retry_with_condition(
        is_not_empty,
        max_attempts=max_attempts,
        delay=delay,
        max_delay=max_delay,
        strategy=strategy,
        exceptions=exceptions,
        timeout=timeout,
        jitter=jitter,
        jitter_factor=jitter_factor,
        log_retries=log_retries,
        log_level=log_level
    )
