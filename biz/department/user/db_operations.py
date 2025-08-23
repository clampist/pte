"""
User database operations - database-level operations for user module
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from config.settings import TestEnvironment
from core.db_checker import DatabaseConfig
from biz.department.user.db_checker import UserDBChecker


class UserDBOperations:
    """User database operations"""
    
    def __init__(self):
        """Initialize user database operations"""
        # Get MySQL configuration from current environment
        mysql_config = TestEnvironment.get_mysql_config()
        
        # Create database configuration
        db_config = DatabaseConfig(mysql_config)
        
        # Create database checker
        self.db_checker = UserDBChecker(db_config)
    
    def verify_user_created(self, user_id: int, expected_data: Dict[str, Any]) -> bool:
        """
        Verify that user was created in database
        
        Args:
            user_id: User ID
            expected_data: Expected user data
            
        Returns:
            True if user exists with expected data
        """
        try:
            # Get user from database
            user = self.db_checker.get_user_by_id(user_id)
            if not user:
                return False
            
            # Verify required fields
            if user.get('name') != expected_data.get('name'):
                return False
            
            if user.get('email') != expected_data.get('email'):
                return False
            
            # Verify optional fields if provided
            if 'age' in expected_data and user.get('age') != expected_data.get('age'):
                return False
            
            return True
            
        except Exception:
            return False
    
    def verify_user_updated(self, user_id: int, expected_data: Dict[str, Any]) -> bool:
        """
        Verify that user was updated in database
        
        Args:
            user_id: User ID
            expected_data: Expected updated user data
            
        Returns:
            True if user was updated with expected data
        """
        try:
            # Get user from database
            user = self.db_checker.get_user_by_id(user_id)
            if not user:
                return False
            
            # Verify updated fields
            for field, expected_value in expected_data.items():
                if field == 'updated_at':  # Skip timestamp fields
                    continue
                    
                if user.get(field) != expected_value:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def verify_user_deleted(self, user_id: int) -> bool:
        """
        Verify that user was deleted from database
        
        Args:
            user_id: User ID
            
        Returns:
            True if user was deleted
        """
        try:
            user = self.db_checker.get_user_by_id(user_id)
            return user is None
            
        except Exception:
            return False
    
    def verify_user_email_unique(self, email: str, exclude_user_id: int = None) -> bool:
        """
        Verify that user email is unique
        
        Args:
            email: User email
            exclude_user_id: User ID to exclude from check (for updates)
            
        Returns:
            True if email is unique
        """
        try:
            user = self.db_checker.get_user_by_email(email)
            if not user:
                return True
            
            # If exclude_user_id is provided, check if it's the same user
            if exclude_user_id and user.get('id') == exclude_user_id:
                return True
            
            return False
            
        except Exception:
            return False
    
    def get_user_count(self) -> int:
        """
        Get total user count
        
        Returns:
            Total number of users
        """
        return self.db_checker.get_user_count()
    
    def create_test_user(self, user_data: Dict[str, Any]) -> int:
        """
        Create test user in database
        
        Args:
            user_data: User data
            
        Returns:
            New user ID
        """
        # Add timestamps
        now = datetime.now()
        user_data['created_at'] = now
        user_data['updated_at'] = now
        
        return self.db_checker.create_user(user_data)
    
    def update_test_user(self, user_id: int, update_data: Dict[str, Any]) -> int:
        """
        Update test user in database
        
        Args:
            user_id: User ID
            update_data: Update data
            
        Returns:
            Number of affected rows
        """
        # Add updated timestamp
        update_data['updated_at'] = datetime.now()
        
        return self.db_checker.update_user(user_id, update_data)
    
    def delete_test_user(self, user_id: int) -> int:
        """
        Delete test user from database
        
        Args:
            user_id: User ID
            
        Returns:
            Number of affected rows
        """
        return self.db_checker.delete_user(user_id)
    
    def cleanup_test_users(self):
        """Clean up test users"""
        self.db_checker.cleanup_test_data("test@example.com")
    
    def assert_user_created(self, user_id: int, expected_data: Dict[str, Any], message: str = None):
        """
        Assert that user was created with expected data
        
        Args:
            user_id: User ID
            expected_data: Expected user data
            message: Custom error message
        """
        if not self.verify_user_created(user_id, expected_data):
            msg = message or f"User {user_id} was not created with expected data"
            raise AssertionError(msg)
    
    def assert_user_updated(self, user_id: int, expected_data: Dict[str, Any], message: str = None):
        """
        Assert that user was updated with expected data
        
        Args:
            user_id: User ID
            expected_data: Expected updated data
            message: Custom error message
        """
        if not self.verify_user_updated(user_id, expected_data):
            msg = message or f"User {user_id} was not updated with expected data"
            raise AssertionError(msg)
    
    def assert_user_deleted(self, user_id: int, message: str = None):
        """
        Assert that user was deleted
        
        Args:
            user_id: User ID
            message: Custom error message
        """
        if not self.verify_user_deleted(user_id):
            msg = message or f"User {user_id} was not deleted"
            raise AssertionError(msg)
    
    def assert_user_email_unique(self, email: str, exclude_user_id: int = None, message: str = None):
        """
        Assert that user email is unique
        
        Args:
            email: User email
            exclude_user_id: User ID to exclude from check
            message: Custom error message
        """
        if not self.verify_user_email_unique(email, exclude_user_id):
            msg = message or f"Email {email} is not unique"
            raise AssertionError(msg)
    
    def assert_user_count_increased(self, initial_count: int, message: str = None):
        """
        Assert that user count increased by 1
        
        Args:
            initial_count: Initial user count
            message: Custom error message
        """
        current_count = self.get_user_count()
        if current_count != initial_count + 1:
            msg = message or f"User count should be {initial_count + 1}, but is {current_count}"
            raise AssertionError(msg)
    
    def assert_user_count_decreased(self, initial_count: int, message: str = None):
        """
        Assert that user count decreased by 1
        
        Args:
            initial_count: Initial user count
            message: Custom error message
        """
        current_count = self.get_user_count()
        if current_count != initial_count - 1:
            msg = message or f"User count should be {initial_count - 1}, but is {current_count}"
            raise AssertionError(msg)
    
    def assert_user_count_unchanged(self, initial_count: int, message: str = None):
        """
        Assert that user count remained unchanged
        
        Args:
            initial_count: Initial user count
            message: Custom error message
        """
        current_count = self.get_user_count()
        if current_count != initial_count:
            msg = message or f"User count should be {initial_count}, but is {current_count}"
            raise AssertionError(msg)
