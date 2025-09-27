#!/usr/bin/env python3
"""
Comprehensive Test Suite Runner
Runs all tests and generates a test report for the project.
"""

import sys
import os
import subprocess
import time
from datetime import datetime

def run_test(test_name, test_file, description):
    """Run a single test and return results"""
    print(f"\n{'='*60}")
    print(f"Running Test: {test_name}")
    print(f"Description: {description}")
    print(f"File: {test_file}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Run the test
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=60)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"PASSED - {test_name}")
            print(f"Duration: {duration:.2f} seconds")
            return True, duration, result.stdout, result.stderr
        else:
            print(f"FAILED - {test_name}")
            print(f"Duration: {duration:.2f} seconds")
            print(f"Error Output: {result.stderr}")
            return False, duration, result.stdout, result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT - {test_name} (exceeded 60 seconds)")
        return False, 60.0, "", "Test timeout"
    except Exception as e:
        print(f"ERROR - {test_name}: {str(e)}")
        return False, 0.0, "", str(e)

def generate_test_report(results, total_duration):
    """Generate a comprehensive test report"""
    report = []
    report.append("# Nuclear Reactor Control Simulation - Test Report")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total Duration: {total_duration:.2f} seconds")
    report.append("")
    
    # Summary
    passed = sum(1 for r in results if r[0])
    total = len(results)
    report.append("## Test Summary")
    report.append(f"- **Total Tests**: {total}")
    report.append(f"- **Passed**: {passed}")
    report.append(f"- **Failed**: {total - passed}")
    report.append(f"- **Success Rate**: {(passed/total)*100:.1f}%")
    report.append("")
    
    # Individual test results
    report.append("## Test Results")
    report.append("")
    
    for i, (test_name, test_file, description, passed, duration, stdout, stderr) in enumerate(results, 1):
        status = "✅ PASSED" if passed else "❌ FAILED"
        report.append(f"### {i}. {test_name} - {status}")
        report.append(f"- **File**: `{test_file}`")
        report.append(f"- **Description**: {description}")
        report.append(f"- **Duration**: {duration:.2f} seconds")
        
        if not passed and stderr:
            report.append(f"- **Error**: ```\n{stderr}\n```")
        
        report.append("")
    
    # Performance metrics
    report.append("## Performance Metrics")
    report.append("")
    
    durations = [r[4] for r in results if r[0]]  # Only passed tests
    if durations:
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        min_duration = min(durations)
        
        report.append(f"- **Average Test Duration**: {avg_duration:.2f} seconds")
        report.append(f"- **Longest Test**: {max_duration:.2f} seconds")
        report.append(f"- **Shortest Test**: {min_duration:.2f} seconds")
        report.append("")
    
    # Recommendations
    report.append("## Recommendations")
    report.append("")
    
    if passed == total:
        report.append("**All tests passed!** The system is ready for production.")
    else:
        report.append("**Some tests failed.** Please review the error messages above.")
        failed_tests = [r for r in results if not r[0]]
        report.append(f"Failed tests: {', '.join([r[0] for r in failed_tests])}")
    
    report.append("")
    report.append("---")
    report.append("*This report was generated automatically by the test suite runner.*")
    
    return "\n".join(report)

def main():
    """Run all tests and generate report"""
    print("Nuclear Reactor Control Simulation - Comprehensive Test Suite")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Define all tests
    tests = [
        ("Basic Functionality", "test_basic.py", "Core simulation functionality and basic dashboard"),
        ("Kinetics Demo", "test_kinetics_demo.py", "Point kinetics solver demonstration"),
        ("PID Controller Demo", "test_pid_demo.py", "PID controller functionality and tuning"),
        ("Safety Systems Demo", "test_safety_demo.py", "Safety interlocks and SCRAM functionality"),
        ("Dashboard Simple", "test_dashboard_simple.py", "Basic dashboard functionality"),
        ("Enhanced Dashboard", "test_enhanced_dashboard.py", "Advanced dashboard with logging and configuration"),
        ("Performance Demo", "python_ui/examples/performance_demo.py", "Performance comparison and benchmarking")
    ]
    
    # Run all tests
    results = []
    start_time = time.time()
    
    for test_name, test_file, description in tests:
        if os.path.exists(test_file):
            passed, duration, stdout, stderr = run_test(test_name, test_file, description)
            results.append((test_name, test_file, description, passed, duration, stdout, stderr))
        else:
            print(f"SKIPPED - {test_name} (file not found: {test_file})")
            results.append((test_name, test_file, description, False, 0.0, "", f"File not found: {test_file}"))
    
    total_duration = time.time() - start_time
    
    # Generate and save report
    report = generate_test_report(results, total_duration)
    
    with open('test_report.md', 'w') as f:
        f.write(report)
    
    print(f"\n{'='*70}")
    print("TEST SUITE COMPLETED")
    print(f"{'='*70}")
    print(f"Total Duration: {total_duration:.2f} seconds")
    print(f"Tests Passed: {sum(1 for r in results if r[0])}/{len(results)}")
    print(f"Test Report: test_report.md")
    print("")
    
    # Show summary
    for test_name, _, _, passed, duration, _, _ in results:
        status = "PASS" if passed else "FAIL"
        print(f"{status} {test_name} ({duration:.2f}s)")

if __name__ == "__main__":
    main()
