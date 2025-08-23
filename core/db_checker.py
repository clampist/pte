"""
Database checker base class for database operations and assertions
"""
import pymysql
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from contextlib import contextmanager


class DatabaseConfig:
    """Database configuration"""
    
    def __init__(self, config: Dict[str, Any]):
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 3306)
        self.username = config.get("username", "root")
        self.password = config.get("password", "")
        self.database = config.get("database", "")
        self.charset = config.get("charset", "utf8mb4")
        self.pool_size = config.get("pool_size", 10)
        self.max_overflow = config.get("max_overflow", 20)
        self.pool_timeout = config.get("pool_timeout", 30)
        self.pool_recycle = config.get("pool_recycle", 3600)
        self.description = config.get("description", "")


class BaseDBChecker(ABC):
    """Base database checker class"""
    
    def __init__(self, db_config: DatabaseConfig):
        """
        Initialize database checker
        
        Args:
            db_config: Database configuration
        """
        self.db_config = db_config
        self.connection = None
    
    @contextmanager
    def get_connection(self):
        """Get database connection context manager"""
        connection = None
        try:
            connection = pymysql.connect(
                host=self.db_config.host,
                port=self.db_config.port,
                user=self.db_config.username,
                password=self.db_config.password,
                database=self.db_config.database,
                charset=self.db_config.charset,
                autocommit=True
            )
            yield connection
        except Exception as e:
            raise Exception(f"Database connection failed: {e}")
        finally:
            if connection:
                connection.close()
    
    def execute_query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute SQL query and return results
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            List of dictionaries containing query results
        """
        with self.get_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
    
    def execute_update(self, sql: str, params: Optional[tuple] = None) -> int:
        """
        Execute SQL update/insert/delete and return affected rows
        
        Args:
            sql: SQL statement
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                affected_rows = cursor.execute(sql, params)
                connection.commit()
                return affected_rows
    
    def execute_insert(self, sql: str, params: Optional[tuple] = None) -> int:
        """
        Execute SQL insert and return last insert ID
        
        Args:
            sql: SQL statement
            params: Query parameters
            
        Returns:
            Last insert ID
        """
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                last_id = connection.insert_id()
                connection.commit()
                return last_id
    
    def execute_many(self, sql: str, params_list: List[tuple]) -> int:
        """
        Execute multiple SQL statements
        
        Args:
            sql: SQL statement template
            params_list: List of parameter tuples
            
        Returns:
            Number of affected rows
        """
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                affected_rows = cursor.executemany(sql, params_list)
                connection.commit()
                return affected_rows
    
    def get_table_count(self, table_name: str, where_clause: str = "") -> int:
        """
        Get record count from table
        
        Args:
            table_name: Table name
            where_clause: WHERE clause (optional)
            
        Returns:
            Record count
        """
        sql = f"SELECT COUNT(*) as count FROM {table_name}"
        if where_clause:
            sql += f" WHERE {where_clause}"
        
        result = self.execute_query(sql)
        return result[0]["count"] if result else 0
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if table exists
        
        Args:
            table_name: Table name
            
        Returns:
            True if table exists, False otherwise
        """
        sql = """
        SELECT COUNT(*) as count 
        FROM information_schema.tables 
        WHERE table_schema = %s AND table_name = %s
        """
        result = self.execute_query(sql, (self.db_config.database, table_name))
        return result[0]["count"] > 0 if result else False
    
    def column_exists(self, table_name: str, column_name: str) -> bool:
        """
        Check if column exists in table
        
        Args:
            table_name: Table name
            column_name: Column name
            
        Returns:
            True if column exists, False otherwise
        """
        sql = """
        SELECT COUNT(*) as count 
        FROM information_schema.columns 
        WHERE table_schema = %s AND table_name = %s AND column_name = %s
        """
        result = self.execute_query(sql, (self.db_config.database, table_name, column_name))
        return result[0]["count"] > 0 if result else False
    
    def get_table_structure(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get table structure
        
        Args:
            table_name: Table name
            
        Returns:
            List of column information dictionaries
        """
        sql = f"DESCRIBE {table_name}"
        return self.execute_query(sql)
    
    def assert_table_exists(self, table_name: str, message: str = None):
        """
        Assert that table exists
        
        Args:
            table_name: Table name
            message: Custom error message
        """
        if not self.table_exists(table_name):
            msg = message or f"Table '{table_name}' does not exist"
            raise AssertionError(msg)
    
    def assert_table_not_exists(self, table_name: str, message: str = None):
        """
        Assert that table does not exist
        
        Args:
            table_name: Table name
            message: Custom error message
        """
        if self.table_exists(table_name):
            msg = message or f"Table '{table_name}' should not exist"
            raise AssertionError(msg)
    
    def assert_column_exists(self, table_name: str, column_name: str, message: str = None):
        """
        Assert that column exists in table
        
        Args:
            table_name: Table name
            column_name: Column name
            message: Custom error message
        """
        if not self.column_exists(table_name, column_name):
            msg = message or f"Column '{column_name}' does not exist in table '{table_name}'"
            raise AssertionError(msg)
    
    def assert_column_not_exists(self, table_name: str, column_name: str, message: str = None):
        """
        Assert that column does not exist in table
        
        Args:
            table_name: Table name
            column_name: Column name
            message: Custom error message
        """
        if self.column_exists(table_name, column_name):
            msg = message or f"Column '{column_name}' should not exist in table '{table_name}'"
            raise AssertionError(msg)
    
    def assert_record_count(self, table_name: str, expected_count: int, where_clause: str = "", message: str = None):
        """
        Assert record count in table
        
        Args:
            table_name: Table name
            expected_count: Expected record count
            where_clause: WHERE clause (optional)
            message: Custom error message
        """
        actual_count = self.get_table_count(table_name, where_clause)
        if actual_count != expected_count:
            msg = message or f"Expected {expected_count} records in table '{table_name}', but found {actual_count}"
            raise AssertionError(msg)
    
    def assert_record_exists(self, table_name: str, where_clause: str, message: str = None):
        """
        Assert that record exists in table
        
        Args:
            table_name: Table name
            where_clause: WHERE clause
            message: Custom error message
        """
        count = self.get_table_count(table_name, where_clause)
        if count == 0:
            msg = message or f"No record found in table '{table_name}' with condition: {where_clause}"
            raise AssertionError(msg)
    
    def assert_record_not_exists(self, table_name: str, where_clause: str, message: str = None):
        """
        Assert that record does not exist in table
        
        Args:
            table_name: Table name
            where_clause: WHERE clause
            message: Custom error message
        """
        count = self.get_table_count(table_name, where_clause)
        if count > 0:
            msg = message or f"Record should not exist in table '{table_name}' with condition: {where_clause}"
            raise AssertionError(msg)
    
    def assert_field_value(self, table_name: str, field_name: str, expected_value: Any, where_clause: str, message: str = None):
        """
        Assert field value in table
        
        Args:
            table_name: Table name
            field_name: Field name
            expected_value: Expected field value
            where_clause: WHERE clause
            message: Custom error message
        """
        sql = f"SELECT {field_name} FROM {table_name} WHERE {where_clause}"
        result = self.execute_query(sql)
        
        if not result:
            msg = message or f"No record found in table '{table_name}' with condition: {where_clause}"
            raise AssertionError(msg)
        
        actual_value = result[0][field_name]
        if actual_value != expected_value:
            msg = message or f"Expected {field_name} = {expected_value}, but found {actual_value}"
            raise AssertionError(msg)
    
    @abstractmethod
    def build_query(self, **kwargs) -> str:
        """
        Build SQL query based on parameters
        
        Args:
            **kwargs: Query parameters
            
        Returns:
            SQL query string
        """
        pass
    
    @abstractmethod
    def build_insert(self, table_name: str, data: Dict[str, Any]) -> str:
        """
        Build INSERT SQL statement
        
        Args:
            table_name: Table name
            data: Data to insert
            
        Returns:
            INSERT SQL statement
        """
        pass
    
    @abstractmethod
    def build_update(self, table_name: str, data: Dict[str, Any], where_clause: str) -> str:
        """
        Build UPDATE SQL statement
        
        Args:
            table_name: Table name
            data: Data to update
            where_clause: WHERE clause
            
        Returns:
            UPDATE SQL statement
        """
        pass
    
    @abstractmethod
    def build_delete(self, table_name: str, where_clause: str) -> str:
        """
        Build DELETE SQL statement
        
        Args:
            table_name: Table name
            where_clause: WHERE clause
            
        Returns:
            DELETE SQL statement
        """
        pass
