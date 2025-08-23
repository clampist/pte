#!/usr/bin/env python3
"""
Database initialization script
"""
import pymysql
import sys
import os
from datetime import datetime

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_database():
    """Create PTE database"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host='127.0.0.1',
            port=8306,
            user='root',
            password='patest',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create database if not exists
            cursor.execute("CREATE DATABASE IF NOT EXISTS pte CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Database 'pte' created successfully")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False


def create_users_table():
    """Create users table"""
    try:
        # Connect to PTE database
        connection = pymysql.connect(
            host='127.0.0.1',
            port=8306,
            user='root',
            password='patest',
            database='pte',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create users table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                age INT,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                INDEX idx_email (email),
                INDEX idx_name (name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            
            cursor.execute(create_table_sql)
            print("✅ users table created successfully")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create users table: {e}")
        return False


def insert_test_data():
    """Insert test data"""
    try:
        # Connect to PTE database
        connection = pymysql.connect(
            host='127.0.0.1',
            port=8306,
            user='root',
            password='patest',
            database='pte',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Check if test data already exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE email LIKE 'test%@example.com'")
            existing_count = cursor.fetchone()[0]
            
            if existing_count > 0:
                print(f"⚠️  {existing_count} test records already exist, skipping insertion")
                connection.close()
                return True
            
            # Insert test users
            test_users = [
                ('John Smith', 'test1@example.com', 25),
                ('Jane Doe', 'test2@example.com', 30),
                ('Mike Johnson', 'test3@example.com', 35),
                ('Sarah Wilson', 'test4@example.com', 28),
                ('David Brown', 'test5@example.com', 32)
            ]
            
            now = datetime.now()
            insert_sql = """
            INSERT INTO users (name, email, age, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s)
            """
            
            for user in test_users:
                cursor.execute(insert_sql, (user[0], user[1], user[2], now, now))
            
            connection.commit()
            print(f"✅ Successfully inserted {len(test_users)} test records")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to insert test data: {e}")
        return False


def verify_database():
    """Verify database setup"""
    try:
        # Connect to PTE database
        connection = pymysql.connect(
            host='127.0.0.1',
            port=8306,
            user='root',
            password='patest',
            database='pte',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Check database
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"✅ Current database: {db_name}")
            
            # Check users table
            cursor.execute("SHOW TABLES LIKE 'users'")
            table_exists = cursor.fetchone()
            if table_exists:
                print("✅ users table exists")
                
                # Get table structure
                cursor.execute("DESCRIBE users")
                columns = cursor.fetchall()
                print(f"  Table structure: {len(columns)} fields")
                for column in columns:
                    print(f"    - {column[0]}: {column[1]}")
                
                # Get user count
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                print(f"  User count: {user_count}")
                
                # Show sample data
                cursor.execute("SELECT id, name, email, age FROM users LIMIT 3")
                users = cursor.fetchall()
                print("  Sample data:")
                for user in users:
                    print(f"    - ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Age: {user[3]}")
            else:
                print("❌ users table does not exist")
                return False
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to verify database: {e}")
        return False


def main():
    """Main function"""
    print("=== PTE Database Initialization ===")
    print("Configuration information:")
    print("  Host: 127.0.0.1")
    print("  Port: 8306")
    print("  Username: root")
    print("  Password: patest")
    print("  Database: pte")
    print()
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    if not create_database():
        return 1
    
    # Step 2: Create users table
    print("\nStep 2: Creating users table...")
    if not create_users_table():
        return 1
    
    # Step 3: Insert test data
    print("\nStep 3: Inserting test data...")
    if not insert_test_data():
        return 1
    
    # Step 4: Verify setup
    print("\nStep 4: Verifying database setup...")
    if not verify_database():
        return 1
    
    print("\n🎉 Database initialization completed!")
    print("\nNow you can run tests:")
    print("  python test_db_connection.py")
    print("  pytest test/department/user/test_db_operations.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
