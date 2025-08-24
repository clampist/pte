#!/usr/bin/env python3
"""
Docker MySQL connection test script
"""
import subprocess
import sys
import os
import time

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import TestEnvironment
from core.db_checker import DatabaseConfig
from biz.department.user.db_checker import UserDBChecker


def get_mysql_config():
    """Get MySQL configuration from config file"""
    try:
        mysql_config = TestEnvironment.get_mysql_config()
        return mysql_config
    except Exception as e:
        print(f"❌ Failed to load MySQL configuration: {e}")
        # Fallback to default values
        return {
            "host": "127.0.0.1",
            "port": 3306,
            "username": "root",
            "password": "password",
            "database": "pte",
            "charset": "utf8mb4"
        }


def check_docker_mysql():
    """Check if MySQL Docker container is running"""
    try:
        # Check if MySQL container is running
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=mysql57', '--format', '{{.Names}}'],
            capture_output=True, text=True, check=True
        )
        
        if 'mysql57' in result.stdout:
            print("✅ MySQL Docker container is running")
            return True
        else:
            print("❌ MySQL Docker container is not running")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to check Docker container: {e}")
        return False
    except FileNotFoundError:
        print("❌ Docker command not found, please ensure Docker is installed")
        return False


def test_mysql_connection():
    """Test MySQL connection using docker exec"""
    try:
        print("=== Testing Docker MySQL Connection ===")
        
        # Get MySQL configuration
        mysql_config = get_mysql_config()
        
        # Test basic connection
        cmd = [
            'docker', 'exec', '-i', 'mysql57', 
            'mysql', '-u', mysql_config['username'], f"-p{mysql_config['password']}", 
            '-e', 'SELECT 1 as test'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Docker MySQL connection successful!")
            print(f"Query result:\n{result.stdout}")
            return True
        else:
            print(f"❌ Docker MySQL connection failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Docker MySQL connection timeout")
        return False
    except Exception as e:
        print(f"❌ Docker MySQL connection test failed: {e}")
        return False


def create_pte_database():
    """Create PTE database in Docker MySQL"""
    try:
        print("=== Creating PTE Database ===")
        
        # Get MySQL configuration
        mysql_config = get_mysql_config()
        
        # Create database
        create_db_cmd = [
            'docker', 'exec', '-i', 'mysql57',
            'mysql', '-u', mysql_config['username'], f"-p{mysql_config['password']}",
            '-e', f"CREATE DATABASE IF NOT EXISTS {mysql_config['database']} CHARACTER SET {mysql_config['charset']} COLLATE {mysql_config['charset']}_unicode_ci"
        ]
        
        result = subprocess.run(create_db_cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ PTE database created successfully")
            return True
        else:
            print(f"❌ PTE database creation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to create PTE database: {e}")
        return False


def create_users_table():
    """Create users table in PTE database"""
    try:
        print("=== Creating Users Table ===")
        
        # Get MySQL configuration
        mysql_config = get_mysql_config()
        
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
        
        cmd = [
            'docker', 'exec', '-i', 'mysql57',
            'mysql', '-u', mysql_config['username'], f"-p{mysql_config['password']}", mysql_config['database'],
            '-e', create_table_sql
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ users table created successfully")
            return True
        else:
            print(f"❌ users table creation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to create users table: {e}")
        return False


def insert_test_data():
    """Insert test data into users table"""
    try:
        print("=== Inserting Test Data ===")
        
        # Get MySQL configuration
        mysql_config = get_mysql_config()
        
        # Check if test data already exists
        check_cmd = [
            'docker', 'exec', '-i', 'mysql57',
            'mysql', '-u', mysql_config['username'], f"-p{mysql_config['password']}", mysql_config['database'],
            '-e', "SELECT COUNT(*) as count FROM users WHERE email LIKE 'test%@example.com'"
        ]
        
        result = subprocess.run(check_cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            # Parse count from output
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                count_line = lines[1]
                try:
                    count = int(count_line)
                    if count > 0:
                        print(f"⚠️  {count} test records already exist, skipping insertion")
                        return True
                except ValueError:
                    pass
        
        # Insert test data
        insert_sql = """
        INSERT INTO users (name, email, age, created_at, updated_at) VALUES
        ('John Smith', 'test1@example.com', 25, NOW(), NOW()),
        ('Jane Doe', 'test2@example.com', 30, NOW(), NOW()),
        ('Mike Johnson', 'test3@example.com', 35, NOW(), NOW()),
        ('Sarah Wilson', 'test4@example.com', 28, NOW(), NOW()),
        ('David Brown', 'test5@example.com', 32, NOW(), NOW())
        """
        
        cmd = [
            'docker', 'exec', '-i', 'mysql57',
            'mysql', '-u', mysql_config['username'], f"-p{mysql_config['password']}", mysql_config['database'],
            '-e', insert_sql
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Test data inserted successfully")
            return True
        else:
            print(f"❌ Test data insertion failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to insert test data: {e}")
        return False


def verify_database_setup():
    """Verify database setup"""
    try:
        print("=== Verifying Database Setup ===")
        
        # Get MySQL configuration
        mysql_config = get_mysql_config()
        
        # Check database
        check_db_cmd = [
            'docker', 'exec', '-i', 'mysql57',
            'mysql', '-u', mysql_config['username'], f"-p{mysql_config['password']}",
            '-e', f'SHOW DATABASES LIKE "{mysql_config["database"]}"'
        ]
        
        result = subprocess.run(check_db_cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and mysql_config['database'] in result.stdout:
            print("✅ PTE database exists")
        else:
            print("❌ PTE database does not exist")
            return False
        
        # Check users table
        check_table_cmd = [
            'docker', 'exec', '-i', 'mysql57',
            'mysql', '-u', mysql_config['username'], f"-p{mysql_config['password']}", mysql_config['database'],
            '-e', 'SHOW TABLES LIKE "users"'
        ]
        
        result = subprocess.run(check_table_cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and 'users' in result.stdout:
            print("✅ users table exists")
        else:
            print("❌ users table does not exist")
            return False
        
        # Get table structure
        structure_cmd = [
            'docker', 'exec', '-i', 'mysql57',
            'mysql', '-u', mysql_config['username'], f"-p{mysql_config['password']}", mysql_config['database'],
            '-e', 'DESCRIBE users'
        ]
        
        result = subprocess.run(structure_cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Table structure:")
            print(result.stdout)
        
        # Get user count
        count_cmd = [
            'docker', 'exec', '-i', 'mysql57',
            'mysql', '-u', mysql_config['username'], f"-p{mysql_config['password']}", mysql_config['database'],
            '-e', 'SELECT COUNT(*) as user_count FROM users'
        ]
        
        result = subprocess.run(count_cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ User count:")
            print(result.stdout)
        
        # Show sample data
        sample_cmd = [
            'docker', 'exec', '-i', 'mysql57',
            'mysql', '-u', mysql_config['username'], f"-p{mysql_config['password']}", mysql_config['database'],
            '-e', 'SELECT id, name, email, age FROM users LIMIT 3'
        ]
        
        result = subprocess.run(sample_cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Sample data:")
            print(result.stdout)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to verify database setup: {e}")
        return False


def test_python_connection():
    """Test Python connection to Docker MySQL"""
    try:
        print("=== Testing Python Connection to Docker MySQL ===")
        
        # Get MySQL configuration from current environment
        mysql_config = TestEnvironment.get_mysql_config()
        print(f"MySQL configuration: {mysql_config}")
        
        # Create database configuration
        db_config = DatabaseConfig(mysql_config)
        
        # Create database checker
        db_checker = UserDBChecker(db_config)
        
        # Test connection
        print("Testing database connection...")
        result = db_checker.execute_query("SELECT 1 as test")
        
        if result:
            print("✅ Python connection to Docker MySQL successful!")
            print(f"Query result: {result[0]}")
            
            # Test table operations
            print("Testing table operations...")
            
            # Test if users table exists
            if db_checker.table_exists('users'):
                print("✅ users table exists")
                
                # Get table structure
                structure = db_checker.get_table_structure('users')
                print(f"Table structure: {len(structure)} fields")
                for column in structure:
                    print(f"  - {column['Field']}: {column['Type']}")
                
                # Get user count
                user_count = db_checker.get_user_count()
                print(f"User count: {user_count}")
                
                # Get sample users
                users = db_checker.get_all_users(limit=3)
                print("Sample users:")
                for user in users:
                    print(f"  - ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Age: {user['age']}")
                
            else:
                print("⚠️  users table does not exist")
                
        else:
            print("❌ Python connection to Docker MySQL failed!")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Python connection to Docker MySQL failed: {e}")
        return False


def main():
    """Main function"""
    print("=== Docker MySQL Verification Test ===")
    
    # Get MySQL configuration
    mysql_config = get_mysql_config()
    
    print("Configuration information:")
    print("  Container name: mysql57")
    print(f"  Host: {mysql_config['host']}")
    print(f"  Port: {mysql_config['port']}")
    print(f"  Username: {mysql_config['username']}")
    print(f"  Password: {'*' * len(mysql_config['password'])}")  # Hide password
    print(f"  Database: {mysql_config['database']}")
    print()
    
    # Step 1: Check Docker MySQL container
    print("Step 1: Checking Docker MySQL container...")
    if not check_docker_mysql():
        print("Please ensure MySQL Docker container is running:")
        print(f"  docker run --name mysql57 -p {mysql_config['port']}:3306 -e MYSQL_ROOT_PASSWORD={mysql_config['password']} -d mysql:5.7")
        return 1
    
    # Step 2: Test Docker MySQL connection
    print("\nStep 2: Testing Docker MySQL connection...")
    if not test_mysql_connection():
        return 1
    
    # Step 3: Create PTE database
    print("\nStep 3: Creating PTE database...")
    if not create_pte_database():
        return 1
    
    # Step 4: Create users table
    print("\nStep 4: Creating users table...")
    if not create_users_table():
        return 1
    
    # Step 5: Insert test data
    print("\nStep 5: Inserting test data...")
    if not insert_test_data():
        return 1
    
    # Step 6: Verify database setup
    print("\nStep 6: Verifying database setup...")
    if not verify_database_setup():
        return 1
    
    # Step 7: Test Python connection
    print("\nStep 7: Testing Python connection...")
    if not test_python_connection():
        return 1
    
    print("\n🎉 Docker MySQL verification completed!")
    print("\nNow you can run tests:")
    print("  python test_db_connection.py local_test local")
    print("  pytest test/department/user/test_sql_building.py")
    
    return 0


if __name__ == "__main__":
    # Set test environment
    os.environ['TEST_IDC'] = 'local_test'
    os.environ['TEST_ENV'] = 'local'
    
    sys.exit(main())
