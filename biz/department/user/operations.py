"""
User business operations encapsulation
Supports real HTTP requests and test clients
"""
import requests
import json
import time
from typing import Dict, List, Any, Optional
from config.settings import TestEnvironment
from core.checker import DataChecker
from biz.department.user.checker import UserDataChecker


class UserOperations:
    """User business operations class"""
    
    def __init__(self, env: str = None, custom_headers: Dict[str, str] = None):
        """
        Initialize user operations
        
        Args:
            env: Environment name, if None use current environment
            custom_headers: Custom request headers
        """
        self.env = env or TestEnvironment.get_current_env()
        self.config = TestEnvironment.get_config(self.env)
        self.base_url = self.config.get('host', 'http://localhost:5001')
        self.timeout = self.config.get('timeout', 30)
        self.retry_count = self.config.get('retry_count', 3)
        
        # Merge default headers and custom headers
        self.headers = self.config.get('headers', {}).copy()
        if custom_headers:
            self.headers.update(custom_headers)
        
        # Ensure Content-Type is set
        if 'Content-Type' not in self.headers:
            self.headers['Content-Type'] = 'application/json'
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, 
                     params: Dict = None, expected_status: int = 200) -> Dict:
        """
        Send HTTP request
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request data
            params: Query parameters
            expected_status: Expected status code
            
        Returns:
            Response data
        """
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.retry_count):
            start_time = time.time()
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data,
                    params=params,
                    timeout=self.timeout
                )
                
                response_time = time.time() - start_time
                
                # Log API call using static Log class
                from core.logger import Log
                Log.api_call(
                    method=method,
                    url=url,
                    status_code=response.status_code,
                    response_time=response_time,
                    request_data={"data": data, "params": params, "headers": self.headers},
                    response_data={"status_code": response.status_code, "content": response.text[:1000]}
                )
                
                # Check status code
                if response.status_code == expected_status:
                    return response.json() if response.content else {}
                else:
                    # If not the last attempt, continue retrying
                    if attempt < self.retry_count - 1:
                        from core.logger import Log
                        Log.warning(f"Request failed with status {response.status_code}, retrying... (attempt {attempt + 1}/{self.retry_count})")
                        continue
                    
                    # Last attempt, return error information
                    error_data = response.json() if response.content else {}
                    error_data['status_code'] = response.status_code
                    return error_data
                    
            except requests.exceptions.RequestException as e:
                response_time = time.time() - start_time
                from core.logger import Log
                Log.error(f"Request failed: {str(e)}", {
                    "error": str(e),
                    "response_time": response_time,
                    "attempt": attempt + 1
                })
                
                if attempt < self.retry_count - 1:
                    continue
                else:
                    return {"error": f"Request failed: {str(e)}", "status_code": 500}
        
        return {"error": "Request failed, maximum retry count reached", "status_code": 500}
    
    def get_all_users(self) -> Dict[str, Any]:
        """
        Get all users
        
        Returns:
            Dictionary containing user list and count
        """
        result = self._make_request('GET', '/api/users')
        
        # Validate response data
        if 'users' in result:
            DataChecker.assert_list_data(result['users'], "users")
            DataChecker.assert_int_data(result['count'], "count")
        
        return result
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User data dictionary, returns None if not exists
        """
        result = self._make_request('GET', f'/api/users/{user_id}', expected_status=200)
        
        if 'error' in result:
            return None
        
        # Validate user data
        UserDataChecker.assert_user_data(result)
        return result
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create new user
        
        Args:
            user_data: User data
            
        Returns:
            Newly created user data, returns None if failed
        """
        # Validate input data
        UserDataChecker.assert_user_create_data(user_data)
        
        result = self._make_request('POST', '/api/users', data=user_data, expected_status=201)
        
        if 'error' in result:
            return None
        
        # Validate returned user data
        UserDataChecker.assert_user_data(result)
        return result
    
    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update user information
        
        Args:
            user_id: User ID
            update_data: Data to update
            
        Returns:
            Updated user data, returns None if failed
        """
        # Validate input data
        UserDataChecker.assert_user_update_data(update_data)
        
        result = self._make_request('PUT', f'/api/users/{user_id}', data=update_data)
        
        if 'error' in result:
            return None
        
        # Validate returned user data
        UserDataChecker.assert_user_data(result)
        return result
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete user
        
        Args:
            user_id: User ID
            
        Returns:
            Whether deletion was successful
        """
        result = self._make_request('DELETE', f'/api/users/{user_id}')
        
        return 'error' not in result
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email (by getting all users then filtering)
        
        Args:
            email: Email address
            
        Returns:
            User data, returns None if not exists
        """
        all_users = self.get_all_users()
        
        if 'users' in all_users:
            for user in all_users['users']:
                if user.get('email') == email:
                    return user
        
        return None
    
    def search_users_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Search users by name
        
        Args:
            name: Name keyword
            
        Returns:
            List of matching users
        """
        all_users = self.get_all_users()
        
        if 'users' in all_users:
            return [user for user in all_users['users'] 
                   if name.lower() in user.get('name', '').lower()]
        
        return []
    
    def get_users_by_age_range(self, min_age: int, max_age: int) -> List[Dict[str, Any]]:
        """
        Get users by age range
        
        Args:
            min_age: Minimum age
            max_age: Maximum age
            
        Returns:
            List of matching users
        """
        all_users = self.get_all_users()
        
        if 'users' in all_users:
            return [user for user in all_users['users'] 
                   if min_age <= user.get('age', 0) <= max_age]
        
        return []
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get application health status
        
        Returns:
            Health status information
        """
        return self._make_request('GET', '/api/health')
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics information
        
        Returns:
            Statistics information
        """
        return self._make_request('GET', '/api/stats')
    
    def is_app_healthy(self) -> bool:
        """
        Check if application is healthy
        
        Returns:
            Whether healthy
        """
        try:
            health_data = self.get_health_status()
            return health_data.get('status') == 'healthy'
        except:
            return False
    
    def get_environment_info(self) -> Dict[str, Any]:
        """
        Get environment information
        
        Returns:
            Environment information
        """
        return {
            "environment": self.env,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "retry_count": self.retry_count,
            "headers": self.headers
        }
    
    def test_connection(self) -> bool:
        """
        Test connection
        
        Returns:
            Whether connection is successful
        """
        try:
            result = self._make_request('GET', '/')
            return 'message' in result
        except:
            return False
    
    def cleanup_test_data(self, test_email_pattern: str = "test@") -> int:
        """
        Clean up test data
        
        Args:
            test_email_pattern: Test email pattern
            
        Returns:
            Number of cleaned records
        """
        all_users = self.get_all_users()
        cleaned_count = 0
        
        if 'users' in all_users:
            for user in all_users['users']:
                if test_email_pattern in user.get('email', ''):
                    if self.delete_user(user['id']):
                        cleaned_count += 1
        
        return cleaned_count
