#!/usr/bin/env python3
"""
Test script for the Nuclear Reactor Control Simulation Web UI
"""

import sys
import os
import time
import requests
import subprocess
import threading

def test_web_ui():
    """Test the web UI functionality"""
    print("Testing Nuclear Reactor Control Simulation Web UI")
    print("=" * 50)
    
    # Check if C++ module is available
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'build'))
        import reactor_sim
        print("✓ C++ module is available")
    except ImportError:
        print("✗ C++ module not found. Please build the project first.")
        return False
    
    # Check Flask dependencies
    try:
        import flask
        import matplotlib
        import numpy
        import pandas
        print("✓ All required dependencies are available")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False
    
    # Start the web server in background
    print("\nStarting web server...")
    web_ui_path = os.path.join(os.path.dirname(__file__), 'web_ui')
    
    # Start Flask app in a separate process
    process = subprocess.Popen([
        sys.executable, 'app.py'
    ], cwd=web_ui_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test API endpoints
        base_url = "http://localhost:5000"
        
        print("\nTesting API endpoints...")
        
        # Test status endpoint
        try:
            response = requests.get(f"{base_url}/api/status", timeout=5)
            if response.status_code == 200:
                print("✓ Status endpoint working")
                data = response.json()
                print(f"  - Simulation running: {data['is_running']}")
                print(f"  - Current power: {data['current_data']['power']:.3f}")
            else:
                print(f"✗ Status endpoint failed: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Status endpoint error: {e}")
        
        # Test start simulation
        try:
            response = requests.post(f"{base_url}/api/start", timeout=5)
            if response.status_code == 200:
                print("✓ Start simulation endpoint working")
            else:
                print(f"✗ Start simulation failed: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Start simulation error: {e}")
        
        # Test data endpoint
        try:
            response = requests.get(f"{base_url}/api/data", timeout=5)
            if response.status_code == 200:
                print("✓ Data endpoint working")
                data = response.json()
                print(f"  - Data points: {len(data['times'])}")
            else:
                print(f"✗ Data endpoint failed: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Data endpoint error: {e}")
        
        # Test configuration endpoint
        try:
            response = requests.get(f"{base_url}/api/config", timeout=5)
            if response.status_code == 200:
                print("✓ Configuration endpoint working")
                config = response.json()
                print(f"  - Power setpoint: {config['power_setpoint']}")
                print(f"  - PID gains: Kp={config['pid_gains']['kp']}, Ki={config['pid_gains']['ki']}, Kd={config['pid_gains']['kd']}")
            else:
                print(f"✗ Configuration endpoint failed: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Configuration endpoint error: {e}")
        
        # Test main page
        try:
            response = requests.get(base_url, timeout=5)
            if response.status_code == 200:
                print("✓ Main page accessible")
                if "Nuclear Reactor Control Simulation" in response.text:
                    print("✓ Page content looks correct")
                else:
                    print("✗ Page content seems incorrect")
            else:
                print(f"✗ Main page failed: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Main page error: {e}")
        
        print("\n✓ Web UI test completed successfully!")
        print("You can now open your browser to: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        
        # Keep server running for manual testing
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping web server...")
    
    finally:
        # Clean up
        process.terminate()
        process.wait()
        print("Web server stopped.")
    
    return True

if __name__ == '__main__':
    try:
        test_web_ui()
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        sys.exit(1)
