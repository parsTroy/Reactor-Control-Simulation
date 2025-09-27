#!/usr/bin/env python3
"""
Quick test script for the Nuclear Reactor Control Simulation Web UI
This script just starts the web server for manual testing.
"""

import sys
import os

def main():
    print("Nuclear Reactor Control Simulation - Web UI")
    print("=" * 50)
    print("Starting web server...")
    print("Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Add web_ui directory to Python path
        web_ui_path = os.path.join(os.path.dirname(__file__), 'web_ui')
        sys.path.insert(0, web_ui_path)
        
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\nShutting down web server...")
    except Exception as e:
        print(f"\nError starting web server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the virtual environment: source venv/bin/activate")
        print("2. Make sure Flask is installed: pip install Flask")
        print("3. Make sure the C++ module is built: cd build && make")
        sys.exit(1)

if __name__ == '__main__':
    main()
