#!/usr/bin/env python3
"""
Test script to verify all components of the LeetCode Tutor application
"""
import os
import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        from models import init_db, get_db, Problem, DailyProblem, RateLimit
        from leetcode_parser import parse_and_save_problems
        from solution_generator import process_problems
        from app import app, get_daily_problems
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_database():
    """Test database initialization"""
    print("\nTesting database...")
    try:
        from models import init_db, get_db, Problem
        init_db()
        db = get_db()
        count = db.query(Problem).count()
        db.close()
        print(f"✓ Database initialized, {count} problems in database")
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False


def test_rate_limiting():
    """Test rate limiting functionality"""
    print("\nTesting rate limiting...")
    try:
        from models import get_db, RateLimit
        from leetcode_parser import check_rate_limit
        
        db = get_db()
        can_proceed = check_rate_limit(db)
        db.close()
        
        print(f"✓ Rate limiting works, can proceed: {can_proceed}")
        return True
    except Exception as e:
        print(f"✗ Rate limiting test failed: {e}")
        return False


def test_web_app():
    """Test web application"""
    print("\nTesting web application...")
    try:
        from app import app
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✓ Web application responds successfully")
                return True
            else:
                print(f"✗ Web application returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"✗ Web application test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("LeetCode Tutor Application - Component Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database,
        test_rate_limiting,
        test_web_app
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("Test Results")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
