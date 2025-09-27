#!/usr/bin/env python3
"""
Fixed Web UI Test - Optimized update frequency
"""

import sys
import os
import time

def main():
    print("Nuclear Reactor Control Simulation - Web UI (Fixed)")
    print("=" * 60)
    print("OPTIMIZATIONS APPLIED:")
    print("✓ Reduced JavaScript update frequency: 10Hz → 1Hz")
    print("✓ Added page visibility check (pauses when tab hidden)")
    print("✓ Reduced simulation loop: 100Hz → 10Hz")
    print("✓ Less frequent updates when simulation stopped")
    print("=" * 60)
    
    # Add paths
    sys.path.append('build')
    sys.path.append('web_ui')
    sys.path.append('python_ui')
    
    try:
        print("1. Testing C++ module import...")
        import reactor_sim
        print("   ✓ C++ module imported successfully")
        
        print("2. Testing Flask app import...")
        from app import app
        print("   ✓ Flask app imported successfully")
        
        print("3. Starting optimized web server...")
        print("   Open your browser to: http://localhost:5001")
        print("   Update frequency: 1Hz (much more reasonable)")
        print("   Press Ctrl+C to stop")
        print("-" * 60)
        
        # Start the server
        app.run(debug=False, host='0.0.0.0', port=5001, use_reloader=False)
        
    except ImportError as e:
        print(f"   ✗ Import error: {e}")
        print("\nTroubleshooting:")
        print("- Make sure you're in the project root directory")
        print("- Make sure the virtual environment is activated")
        print("- Make sure the C++ module is built: cd build && make")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    except KeyboardInterrupt:
        print("\n\nShutting down web server...")

if __name__ == '__main__':
    main()
