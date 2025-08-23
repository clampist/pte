#!/usr/bin/env python3
"""
Database Connection Test Script
"""
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import TestEnvironment
from core.db_checker import DatabaseConfig
from biz.department.user.db_checker import UserDBChecker


def test_database_connection():
    """Test database connection"""
    try:
        print("=== Database Connection Test ===")
        
        # Get current IDC and environment
        current_idc = TestEnvironment.get_current_idc()
        current_env = TestEnvironment.get_current_env()
        print(f"Current IDC: {current_idc}")
        print(f"Current environment: {current_env}")
        
        # Get MySQL configuration
        mysql_config = TestEnvironment.get_mysql_config()
        print(f"\nMySQL Configuration:")
        print(f"  Host: {mysql_config.get('host')}")
        print(f"  Port: {mysql_config.get('port')}")
        print(f"  Database: {mysql_config.get('database')}")
        print(f"  Username: {mysql_config.get('username')}")
        print(f"  Charset: {mysql_config.get('charset')}")
        
        # Create database configuration
        db_config = DatabaseConfig(mysql_config)
        
        # Create database checker
        db_checker = UserDBChecker(db_config)
        
        # Test connection
        print(f"\nTesting database connection...")
        result = db_checker.execute_query("SELECT 1 as test")
        
        if result:
            print("✅ Database connection successful!")
            print(f"  Test query result: {result[0]}")
            
            # Test table operations
            print(f"\nTesting table operations...")
            
            # Test if users table exists
            if db_checker.table_exists('users'):
                print("✅ users table exists")
                
                # Get table structure
                structure = db_checker.get_table_structure('users')
                print(f"  Table structure: {len(structure)} fields")
                for column in structure:
                    print(f"    - {column['Field']}: {column['Type']}")
                
                # Get user count
                user_count = db_checker.get_user_count()
                print(f"  User count: {user_count}")
                
            else:
                print("⚠️  users table does not exist")
                
        else:
            print("❌ Database connection failed!")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False


def test_sql_building():
    """Test SQL building"""
    try:
        print(f"\n=== SQL Building Test ===")
        
        # Get MySQL configuration
        mysql_config = TestEnvironment.get_mysql_config()
        db_config = DatabaseConfig(mysql_config)
        db_checker = UserDBChecker(db_config)
        
        # Test SELECT query building
        print("Testing SELECT query building:")
        select_sql = db_checker.build_query(
            where_conditions={'name': 'Test User', 'age': 25}
        )
        print(f"  {select_sql}")
        
        # Test INSERT query building
        print("Testing INSERT query building:")
        insert_data = {'name': 'Test User', 'email': 'test@example.com', 'age': 25}
        insert_sql = db_checker.build_insert('users', insert_data)
        print(f"  {insert_sql}")
        
        # Test UPDATE query building
        print("Testing UPDATE query building:")
        update_data = {'name': 'Updated User', 'age': 30}
        update_sql = db_checker.build_update('users', update_data, 'id = 1')
        print(f"  {update_sql}")
        
        # Test DELETE query building
        print("Testing DELETE query building:")
        delete_sql = db_checker.build_delete('users', 'id = 1')
        print(f"  {delete_sql}")
        
        print("✅ SQL building test passed!")
        return True
        
    except Exception as e:
        print(f"❌ SQL building test failed: {e}")
        return False


def main():
    """Main function"""
    # Test database connection
    connection_ok = test_database_connection()
    
    # Test SQL building
    sql_ok = test_sql_building()
    
    # Summary
    print(f"\n=== Test Summary ===")
    print(f"Database connection: {'✅ Passed' if connection_ok else '❌ Failed'}")
    print(f"SQL building: {'✅ Passed' if sql_ok else '❌ Failed'}")
    
    if connection_ok and sql_ok:
        print("🎉 All database tests passed!")
        return 0
    else:
        print("❌ Some database tests failed!")
        return 1


if __name__ == "__main__":
    # Set test environment if provided
    if len(sys.argv) > 1:
        os.environ["TEST_IDC"] = sys.argv[1]
    if len(sys.argv) > 2:
        os.environ["TEST_ENV"] = sys.argv[2]
    
    sys.exit(main())
