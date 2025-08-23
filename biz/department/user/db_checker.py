"""
User database checker for user-related database operations
"""
from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine, text, Table, MetaData, Column, String, Integer, DateTime
from sqlalchemy.sql import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from core.db_checker import BaseDBChecker, DatabaseConfig


class UserDBChecker(BaseDBChecker):
    """User database checker with SQLAlchemy SQL building"""
    
    def __init__(self, db_config: DatabaseConfig):
        """
        Initialize user database checker
        
        Args:
            db_config: Database configuration
        """
        super().__init__(db_config)
        
        # Create SQLAlchemy engine
        connection_string = (
            f"mysql+pymysql://{db_config.username}:{db_config.password}"
            f"@{db_config.host}:{db_config.port}/{db_config.database}"
            f"?charset={db_config.charset}"
        )
        self.engine = create_engine(connection_string)
        
        # Define user table metadata
        self.metadata = MetaData()
        self.users_table = Table(
            'users',
            self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('name', String(100), nullable=False),
            Column('email', String(100), nullable=False, unique=True),
            Column('age', Integer, nullable=True),
            Column('created_at', DateTime, nullable=False),
            Column('updated_at', DateTime, nullable=False)
        )
    
    def build_query(self, **kwargs) -> str:
        """
        Build SQL query based on parameters
        
        Args:
            **kwargs: Query parameters
                - table_name: Table name (default: 'users')
                - fields: Fields to select (default: '*')
                - where_conditions: WHERE conditions dict
                - order_by: ORDER BY clause
                - limit: LIMIT clause
                - offset: OFFSET clause
                
        Returns:
            SQL query string
        """
        table_name = kwargs.get('table_name', 'users')
        fields = kwargs.get('fields', '*')
        where_conditions = kwargs.get('where_conditions', {})
        order_by = kwargs.get('order_by', '')
        limit = kwargs.get('limit', '')
        offset = kwargs.get('offset', '')
        
        # Build SELECT clause
        sql = f"SELECT {fields} FROM {table_name}"
        
        # Build WHERE clause
        if where_conditions:
            where_clauses = []
            for field, value in where_conditions.items():
                if isinstance(value, str):
                    where_clauses.append(f"{field} = '{value}'")
                else:
                    where_clauses.append(f"{field} = {value}")
            sql += f" WHERE {' AND '.join(where_clauses)}"
        
        # Build ORDER BY clause
        if order_by:
            sql += f" ORDER BY {order_by}"
        
        # Build LIMIT clause
        if limit:
            sql += f" LIMIT {limit}"
        
        # Build OFFSET clause
        if offset:
            sql += f" OFFSET {offset}"
        
        return sql
    
    def build_insert(self, table_name: str, data: Dict[str, Any]) -> str:
        """
        Build INSERT SQL statement using SQLAlchemy
        
        Args:
            table_name: Table name
            data: Data to insert
            
        Returns:
            INSERT SQL statement
        """
        if table_name == 'users':
            table = self.users_table
        else:
            # For other tables, create a generic table
            columns = [Column(key, String(255)) for key in data.keys()]
            table = Table(table_name, self.metadata, *columns)
        
        stmt = insert(table).values(**data)
        return str(stmt.compile(compile_kwargs={"literal_binds": True}))
    
    def build_update(self, table_name: str, data: Dict[str, Any], where_clause: str) -> str:
        """
        Build UPDATE SQL statement using SQLAlchemy
        
        Args:
            table_name: Table name
            data: Data to update
            where_clause: WHERE clause
            
        Returns:
            UPDATE SQL statement
        """
        if table_name == 'users':
            table = self.users_table
        else:
            # For other tables, create a generic table
            columns = [Column(key, String(255)) for key in set(list(data.keys()) + where_clause.split())]
            table = Table(table_name, self.metadata, *columns)
        
        # Parse where clause to create condition
        # This is a simplified version - in production you'd want more robust parsing
        stmt = update(table).values(**data).where(text(where_clause))
        return str(stmt.compile(compile_kwargs={"literal_binds": True}))
    
    def build_delete(self, table_name: str, where_clause: str) -> str:
        """
        Build DELETE SQL statement using SQLAlchemy
        
        Args:
            table_name: Table name
            where_clause: WHERE clause
            
        Returns:
            DELETE SQL statement
        """
        if table_name == 'users':
            table = self.users_table
        else:
            # For other tables, create a generic table
            table = Table(table_name, self.metadata)
        
        stmt = delete(table).where(text(where_clause))
        return str(stmt.compile(compile_kwargs={"literal_binds": True}))
    
    # User-specific database operations
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User data dictionary or None
        """
        sql = self.build_query(
            where_conditions={'id': user_id}
        )
        result = self.execute_query(sql)
        return result[0] if result else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email
        
        Args:
            email: User email
            
        Returns:
            User data dictionary or None
        """
        sql = self.build_query(
            where_conditions={'email': email}
        )
        result = self.execute_query(sql)
        return result[0] if result else None
    
    def get_users_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Get users by name
        
        Args:
            name: User name
            
        Returns:
            List of user data dictionaries
        """
        sql = self.build_query(
            where_conditions={'name': name}
        )
        return self.execute_query(sql)
    
    def get_users_by_age_range(self, min_age: int, max_age: int) -> List[Dict[str, Any]]:
        """
        Get users by age range
        
        Args:
            min_age: Minimum age
            max_age: Maximum age
            
        Returns:
            List of user data dictionaries
        """
        sql = f"SELECT * FROM users WHERE age BETWEEN {min_age} AND {max_age}"
        return self.execute_query(sql)
    
    def get_all_users(self, limit: int = None, offset: int = None) -> List[Dict[str, Any]]:
        """
        Get all users with optional pagination
        
        Args:
            limit: Limit number of records
            offset: Offset for pagination
            
        Returns:
            List of user data dictionaries
        """
        kwargs = {}
        if limit:
            kwargs['limit'] = limit
        if offset:
            kwargs['offset'] = offset
        
        sql = self.build_query(**kwargs)
        return self.execute_query(sql)
    
    def create_user(self, user_data: Dict[str, Any]) -> int:
        """
        Create new user
        
        Args:
            user_data: User data dictionary
            
        Returns:
            New user ID
        """
        sql = self.build_insert('users', user_data)
        return self.execute_insert(sql)
    
    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> int:
        """
        Update user
        
        Args:
            user_id: User ID
            update_data: Data to update
            
        Returns:
            Number of affected rows
        """
        sql = self.build_update('users', update_data, f"id = {user_id}")
        return self.execute_update(sql)
    
    def delete_user(self, user_id: int) -> int:
        """
        Delete user
        
        Args:
            user_id: User ID
            
        Returns:
            Number of affected rows
        """
        sql = self.build_delete('users', f"id = {user_id}")
        return self.execute_update(sql)
    
    def get_user_count(self, where_clause: str = "") -> int:
        """
        Get user count
        
        Args:
            where_clause: WHERE clause (optional)
            
        Returns:
            User count
        """
        return self.get_table_count('users', where_clause)
    
    # User-specific assertions
    def assert_user_exists(self, user_id: int, message: str = None):
        """
        Assert that user exists
        
        Args:
            user_id: User ID
            message: Custom error message
        """
        self.assert_record_exists('users', f"id = {user_id}", message)
    
    def assert_user_not_exists(self, user_id: int, message: str = None):
        """
        Assert that user does not exist
        
        Args:
            user_id: User ID
            message: Custom error message
        """
        self.assert_record_not_exists('users', f"id = {user_id}", message)
    
    def assert_user_email_exists(self, email: str, message: str = None):
        """
        Assert that user with email exists
        
        Args:
            email: User email
            message: Custom error message
        """
        self.assert_record_exists('users', f"email = '{email}'", message)
    
    def assert_user_email_not_exists(self, email: str, message: str = None):
        """
        Assert that user with email does not exist
        
        Args:
            email: User email
            message: Custom error message
        """
        self.assert_record_not_exists('users', f"email = '{email}'", message)
    
    def assert_user_count(self, expected_count: int, where_clause: str = "", message: str = None):
        """
        Assert user count
        
        Args:
            expected_count: Expected user count
            where_clause: WHERE clause (optional)
            message: Custom error message
        """
        self.assert_record_count('users', expected_count, where_clause, message)
    
    def assert_user_field_value(self, user_id: int, field_name: str, expected_value: Any, message: str = None):
        """
        Assert user field value
        
        Args:
            user_id: User ID
            field_name: Field name
            expected_value: Expected field value
            message: Custom error message
        """
        self.assert_field_value('users', field_name, expected_value, f"id = {user_id}", message)
    
    def assert_user_name(self, user_id: int, expected_name: str, message: str = None):
        """
        Assert user name
        
        Args:
            user_id: User ID
            expected_name: Expected user name
            message: Custom error message
        """
        self.assert_user_field_value(user_id, 'name', expected_name, message)
    
    def assert_user_email(self, user_id: int, expected_email: str, message: str = None):
        """
        Assert user email
        
        Args:
            user_id: User ID
            expected_email: Expected user email
            message: Custom error message
        """
        self.assert_user_field_value(user_id, 'email', expected_email, message)
    
    def assert_user_age(self, user_id: int, expected_age: int, message: str = None):
        """
        Assert user age
        
        Args:
            user_id: User ID
            expected_age: Expected user age
            message: Custom error message
        """
        self.assert_user_field_value(user_id, 'age', expected_age, message)
    
    def cleanup_test_data(self, test_email_pattern: str = "test@example.com"):
        """
        Clean up test data
        
        Args:
            test_email_pattern: Email pattern to match for cleanup
        """
        sql = self.build_delete('users', f"email LIKE '%{test_email_pattern}%'")
        self.execute_update(sql)
