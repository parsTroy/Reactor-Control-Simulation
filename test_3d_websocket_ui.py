#!/usr/bin/env python3
"""
Test script for WebSocket + 3D Visualization Nuclear Reactor Control Simulation
"""

import sys
import os

def main():
    print("Nuclear Reactor Control Simulation - WebSocket + 3D Visualization")
    print("=" * 70)
    print("ENHANCEMENTS INCLUDED:")
    print("✓ WebSocket real-time communication (10Hz)")
    print("✓ 3D Reactor Visualization with Three.js")
    print("✓ Interactive 3D controls (rotate, zoom, pan)")
    print("✓ Real-time 3D power representation")
    print("✓ Dynamic control rod positioning")
    print("✓ Visual SCRAM indicators")
    print("=" * 70)
    
    # Add paths
    sys.path.append('build')
    sys.path.append('web_ui')
    sys.path.append('python_ui')
    
    try:
        print("1. Testing C++ module import...")
        import reactor_sim
        print("   ✓ C++ module imported successfully")
        
        print("2. Testing Flask-SocketIO import...")
        import flask_socketio
        print("   ✓ Flask-SocketIO imported successfully")
        
        print("3. Testing Flask app with WebSocket + 3D support...")
        from app import app, socketio
        print("   ✓ Flask app with WebSocket + 3D support imported successfully")
        
        print("4. Starting enhanced web server...")
        print("   Open your browser to: http://localhost:5001")
        print("   Features:")
        print("   - Real-time WebSocket data streaming (10Hz)")
        print("   - Interactive 3D reactor visualization")
        print("   - Dynamic control rod positioning")
        print("   - Visual power level indicators")
        print("   - SCRAM visual alerts")
        print("   - Smooth 3D animations")
        print("   Press Ctrl+C to stop")
        print("-" * 70)
        
        # Start the server with WebSocket support
        socketio.run(app, debug=False, host='0.0.0.0', port=5001, use_reloader=False)
        
    except ImportError as e:
        print(f"   ✗ Import error: {e}")
        print("\nTroubleshooting:")
        print("- Make sure you're in the project root directory")
        print("- Make sure the virtual environment is activated")
        print("- Make sure Flask-SocketIO is installed: pip install Flask-SocketIO")
        print("- Make sure the C++ module is built: cd build && make")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    except KeyboardInterrupt:
        print("\n\nShutting down enhanced web server...")

if __name__ == '__main__':
    main()
