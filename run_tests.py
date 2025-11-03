#!/usr/bin/env python
"""
Comprehensive test runner for ResQTrack.
Tests all backend endpoints and admin functionality.
"""
import sys
import subprocess


def run_tests():
    """Run all tests and report results"""
    print("=" * 70)
    print("ResQTrack - Comprehensive Test Suite")
    print("=" * 70)
    print()
    
    test_suites = [
        ("Authentication Tests", "tests/test_auth.py"),
        ("Case Management Tests", "tests/test_cases.py"),
        ("Upload Tests", "tests/test_uploads.py"),
        ("Admin Dashboard Tests", "tests/test_e2e_admin.py"),
        ("Frontend Integration Tests", "tests/test_frontend_integration.py"),
    ]
    
    results = []
    
    for suite_name, test_file in test_suites:
        print(f"\n{'─' * 70}")
        print(f"Running: {suite_name}")
        print(f"{'─' * 70}")
        
        try:
            result = subprocess.run(
                ["pytest", test_file, "-v", "--tb=short"],
                capture_output=False,
                text=True
            )
            
            results.append((suite_name, result.returncode == 0))
        except Exception as e:
            print(f"Error running {suite_name}: {e}")
            results.append((suite_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for suite_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status:12} - {suite_name}")
    
    print("=" * 70)
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
