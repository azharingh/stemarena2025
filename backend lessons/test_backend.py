#!/usr/bin/env python3
"""
Test script to verify backend functionality
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    try:
        from database_sqlite import user_collection
        print("✓ Database module imported successfully")
        
        from utilis import hash_password, verify_password, create_access_token
        print("✓ Utils module imported successfully")
        
        from ai_service import AIService
        print("✓ AI service module imported successfully")
        
        from app_flask import app
        print("✓ Flask app imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_database():
    """Test database initialization"""
    try:
        from database_sqlite import user_collection
        
        # Test database connection
        test_user = user_collection.find_user_by_username("test_user")
        print("✓ Database connection successful")
        
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_ai_service():
    """Test AI service"""
    try:
        from ai_service import AIService
        
        ai = AIService()
        task = ai.generate_task("math", "easy")
        print("✓ AI service working")
        
        return True
    except Exception as e:
        print(f"✗ AI service error: {e}")
        return False

def main():
    print("Testing STEM ARENA Backend...")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("Database", test_database),
        ("AI Service", test_ai_service)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} failed")
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Backend should work correctly.")
        return True
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 