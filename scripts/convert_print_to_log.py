#!/usr/bin/env python3
"""
Convert print statements to Log.info in test files
"""
import os
import re
import sys
from pathlib import Path


def convert_print_to_log(file_path):
    """Convert print statements to Log.info in a single file"""
    print(f"Processing: {file_path}")
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if Log import already exists
    has_log_import = 'from core.logger import Log' in content or 'import core.logger' in content
    
    # Convert print statements
    # Pattern 1: print("string")
    content = re.sub(r'print\("([^"]*)"\)', r'Log.info("\1")', content)
    
    # Pattern 2: print('string')
    content = re.sub(r"print\('([^']*)'\)", r"Log.info('\1')", content)
    
    # Pattern 3: print(f"string")
    content = re.sub(r'print\(f"([^"]*)"\)', r'Log.info(f"\1")', content)
    
    # Pattern 4: print(f'string')
    content = re.sub(r"print\(f'([^']*)'\)", r"Log.info(f'\1')", content)
    
    # Pattern 5: print("string", variable)
    content = re.sub(r'print\("([^"]*)",\s*([^)]+)\)', r'Log.info(f"\1 {\2}")', content)
    
    # Pattern 6: print('string', variable)
    content = re.sub(r"print\('([^']*)',\s*([^)]+)\)", r"Log.info(f'\1 {\2}')", content)
    
    # Pattern 7: print(f"string", variable)
    content = re.sub(r'print\(f"([^"]*)",\s*([^)]+)\)', r'Log.info(f"\1 {\2}")', content)
    
    # Pattern 8: print(f'string', variable)
    content = re.sub(r"print\(f'([^']*)',\s*([^)]+)\)", r"Log.info(f'\1 {\2}')", content)
    
    # Add Log import if not present
    if not has_log_import and 'Log.info(' in content:
        # Find the best place to add import (after other imports)
        lines = content.split('\n')
        import_added = False
        
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                continue
            elif line.strip() == '':
                continue
            else:
                # Insert Log import before the first non-import line
                lines.insert(i, 'from core.logger import Log')
                import_added = True
                break
        
        if not import_added:
            # If no good place found, add at the beginning
            lines.insert(0, 'from core.logger import Log')
        
        content = '\n'.join(lines)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Converted: {file_path}")


def process_test_directory(test_dir):
    """Process all Python files in test directory"""
    test_path = Path(test_dir)
    
    if not test_path.exists():
        print(f"❌ Test directory not found: {test_dir}")
        return
    
    # Find all Python files in test directory
    python_files = list(test_path.rglob('*.py'))
    
    print(f"Found {len(python_files)} Python files in {test_dir}")
    
    converted_count = 0
    
    for file_path in python_files:
        try:
            # Skip __init__.py files
            if file_path.name == '__init__.py':
                continue
                
            # Read file to check if it contains print statements
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Only process files that contain print statements
            if 'print(' in content:
                convert_print_to_log(file_path)
                converted_count += 1
            else:
                print(f"⏭️  Skipped (no print statements): {file_path}")
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print(f"\n🎉 Conversion completed!")
    print(f"   Total files processed: {converted_count}")
    print(f"   Total files found: {len(python_files)}")


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python scripts/convert_print_to_log.py <test_directory>")
        print("Example: python scripts/convert_print_to_log.py test/department/user")
        sys.exit(1)
    
    test_dir = sys.argv[1]
    process_test_directory(test_dir)


if __name__ == "__main__":
    main()
