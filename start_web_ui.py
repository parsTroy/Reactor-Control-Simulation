#!/usr/bin/env python3
"""
Startup script for the Nuclear Reactor Control Simulation Web UI
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import matplotlib
        import numpy
        import pandas
        print("✓ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_cpp_build():
    """Check if C++ module is built"""
    build_path = os.path.join(os.path.dirname(__file__), 'build')
    if not os.path.exists(build_path):
        print("✗ C++ module not built. Please run: mkdir build && cd build && cmake .. && make")
        return False
    
    # Check for the Python module
    try:
        sys.path.append(build_path)
        import reactor_sim
        print("✓ C++ module is available")
        return True
    except ImportError:
        print("✗ C++ module not found. Please build the project first.")
        return False

def main():
    """Main startup function"""
    print("Nuclear Reactor Control Simulation - Web UI")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check C++ build
    if not check_cpp_build():
        sys.exit(1)
    
    # Start the web server
    print("\nStarting web server...")
    print("Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to web_ui directory and start Flask app
        web_ui_path = os.path.join(os.path.dirname(__file__), 'web_ui')
        os.chdir(web_ui_path)
        
        # Import and run the Flask app
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\nShutting down web server...")
    except Exception as e:
        print(f"\nError starting web server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
