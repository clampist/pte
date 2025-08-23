"""
API client for HTTP requests with logid support
"""
import requests
import time
from typing import Dict, List, Optional, Any
from api.config import APIConfig
from core.logger import generate_logid


class APIClient:
    """Base API client with environment support"""

    def __init__(self, base_url: str = None, headers: Dict = None, env: str = None, logid: str = None):
        """
        Initialize API client
        
        Args:
            base_url: Base URL for API requests
            headers: Custom headers
            env: Environment name
            logid: Log ID for tracing
        """
        from config.settings import TestEnvironment
        
        # Get environment configuration
        self.env = env or TestEnvironment.get_current_env()
        self.host = base_url or TestEnvironment.get_host(self.env)
        self.default_headers = TestEnvironment.get_headers(self.env)
        
        # Generate or use provided logid
        self.logid = logid or generate_logid()
        
        # Add logid to headers
        self.default_headers['logId'] = self.logid
        
        # Merge custom headers if provided
        if headers:
            self.headers = {**self.default_headers, **headers}
        else:
            self.headers = self.default_headers
        
        # Initialize session
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Set timeout and retry configuration
        self.timeout = TestEnvironment.get_timeout(self.env)
        self.retry_count = TestEnvironment.get_retry_count(self.env)

    def get(self, endpoint: str, params: Dict = None, headers: Dict = None, logger=None) -> requests.Response:
        """GET request with logid support"""
        url = f"{self.host}{endpoint}"
        final_headers = {**self.headers, **(headers or {})}
        
        start_time = time.time()
        try:
            response = self.session.get(url, params=params, headers=final_headers, timeout=self.timeout)
            response_time = time.time() - start_time
            
            # Log API call using static Log class if no logger provided
            if logger:
                logger.api_call(
                    method="GET",
                    url=url,
                    status_code=response.status_code,
                    response_time=response_time,
                    request_data={"params": params, "headers": final_headers},
                    response_data={"status_code": response.status_code, "content": response.text[:1000]}
                )
            else:
                from core.logger import Log
                Log.api_call(
                    method="GET",
                    url=url,
                    status_code=response.status_code,
                    response_time=response_time,
                    request_data={"params": params, "headers": final_headers},
                    response_data={"status_code": response.status_code, "content": response.text[:1000]}
                )
            
            return response
        except Exception as e:
            response_time = time.time() - start_time
            if logger:
                logger.error(f"GET request failed: {url}", {
                    "error": str(e),
                    "logid": self.logid,
                    "response_time": response_time
                })
            else:
                from core.logger import Log
                Log.error(f"GET request failed: {url}", {
                    "error": str(e),
                    "logid": self.logid,
                    "response_time": response_time
                })
            raise

    def post(self, endpoint: str, data: Dict = None, json_data: Dict = None, headers: Dict = None, logger=None) -> requests.Response:
        """POST request with logid support"""
        url = f"{self.host}{endpoint}"
        final_headers = {**self.headers, **(headers or {})}
        
        start_time = time.time()
        try:
            if json_data:
                response = self.session.post(url, json=json_data, headers=final_headers, timeout=self.timeout)
            else:
                response = self.session.post(url, data=data, headers=final_headers, timeout=self.timeout)
            
            response_time = time.time() - start_time
            
            # Log API call if logger is provided
            if logger:
                logger.api_call(
                    method="POST",
                    url=url,
                    status_code=response.status_code,
                    response_time=response_time,
                    request_data={"data": data, "json_data": json_data, "headers": final_headers},
                    response_data={"status_code": response.status_code, "content": response.text[:1000]}
                )
            
            return response
        except Exception as e:
            response_time = time.time() - start_time
            if logger:
                logger.error(f"POST request failed: {url}", {
                    "error": str(e),
                    "logid": self.logid,
                    "response_time": response_time
                })
            raise

    def put(self, endpoint: str, data: Dict = None, json_data: Dict = None, headers: Dict = None, logger=None) -> requests.Response:
        """PUT request with logid support"""
        url = f"{self.host}{endpoint}"
        final_headers = {**self.headers, **(headers or {})}
        
        start_time = time.time()
        try:
            if json_data:
                response = self.session.put(url, json=json_data, headers=final_headers, timeout=self.timeout)
            else:
                response = self.session.put(url, data=data, headers=final_headers, timeout=self.timeout)
            
            response_time = time.time() - start_time
            
            # Log API call if logger is provided
            if logger:
                logger.api_call(
                    method="PUT",
                    url=url,
                    status_code=response.status_code,
                    response_time=response_time,
                    request_data={"data": data, "json_data": json_data, "headers": final_headers},
                    response_data={"status_code": response.status_code, "content": response.text[:1000]}
                )
            
            return response
        except Exception as e:
            response_time = time.time() - start_time
            if logger:
                logger.error(f"PUT request failed: {url}", {
                    "error": str(e),
                    "logid": self.logid,
                    "response_time": response_time
                })
            raise

    def delete(self, endpoint: str, headers: Dict = None, logger=None) -> requests.Response:
        """DELETE request with logid support"""
        url = f"{self.host}{endpoint}"
        final_headers = {**self.headers, **(headers or {})}
        
        start_time = time.time()
        try:
            response = self.session.delete(url, headers=final_headers, timeout=self.timeout)
            response_time = time.time() - start_time
            
            # Log API call if logger is provided
            if logger:
                logger.api_call(
                    method="DELETE",
                    url=url,
                    status_code=response.status_code,
                    response_time=response_time,
                    request_data={"headers": final_headers},
                    response_data={"status_code": response.status_code, "content": response.text[:1000]}
                )
            
            return response
        except Exception as e:
            response_time = time.time() - start_time
            if logger:
                logger.error(f"DELETE request failed: {url}", {
                    "error": str(e),
                    "logid": self.logid,
                    "response_time": response_time
                })
            raise

    def patch(self, endpoint: str, data: Dict = None, json_data: Dict = None, headers: Dict = None, logger=None) -> requests.Response:
        """PATCH request with logid support"""
        url = f"{self.host}{endpoint}"
        final_headers = {**self.headers, **(headers or {})}
        
        start_time = time.time()
        try:
            if json_data:
                response = self.session.patch(url, json=json_data, headers=final_headers, timeout=self.timeout)
            else:
                response = self.session.patch(url, data=data, headers=final_headers, timeout=self.timeout)
            
            response_time = time.time() - start_time
            
            # Log API call if logger is provided
            if logger:
                logger.api_call(
                    method="PATCH",
                    url=url,
                    status_code=response.status_code,
                    response_time=response_time,
                    request_data={"data": data, "json_data": json_data, "headers": final_headers},
                    response_data={"status_code": response.status_code, "content": response.text[:1000]}
                )
            
            return response
        except Exception as e:
            response_time = time.time() - start_time
            if logger:
                logger.error(f"PATCH request failed: {url}", {
                    "error": str(e),
                    "logid": self.logid,
                    "response_time": response_time
                })
            raise
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Get environment information"""
        from config.settings import TestEnvironment
        return {
            "environment": self.env,
            "host": self.host,
            "headers": self.headers,
            "timeout": self.timeout,
            "retry_count": self.retry_count,
            "idc": TestEnvironment.get_idc(),
            "logid": self.logid
        }


class TestAPIClient:
    """Test API client for testing purposes"""

    def __init__(self, base_url: str = None, headers: Dict = None, env: str = None):
        """
        Initialize test API client
        
        Args:
            base_url: Base URL for API requests
            headers: Custom headers
            env: Environment name
        """
        self.client = APIClient(base_url, headers, env)

    def get(self, endpoint: str, params: Dict = None, headers: Dict = None) -> requests.Response:
        """GET request using test client"""
        return self.client.get(endpoint, params=params, headers=headers)

    def post(self, endpoint: str, data: Dict = None, json_data: Dict = None, headers: Dict = None) -> requests.Response:
        """POST request using test client"""
        return self.client.post(endpoint, data=data, json_data=json_data, headers=headers)

    def put(self, endpoint: str, data: Dict = None, json_data: Dict = None, headers: Dict = None) -> requests.Response:
        """PUT request using test client"""
        return self.client.put(endpoint, data=data, json_data=json_data, headers=headers)

    def delete(self, endpoint: str, headers: Dict = None) -> requests.Response:
        """DELETE request using test client"""
        return self.client.delete(endpoint, headers=headers)

    def patch(self, endpoint: str, data: Dict = None, json_data: Dict = None, headers: Dict = None) -> requests.Response:
        """PATCH request using test client"""
        return self.client.patch(endpoint, data=data, json_data=json_data, headers=headers)
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Get environment information"""
        return self.client.get_environment_info()
