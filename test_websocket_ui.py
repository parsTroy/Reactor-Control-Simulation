#!/usr/bin/env python3
"""
Test script for WebSocket-enabled Nuclear Reactor Control Simulation Web UI
"""

import sys
import os

def main():
    print("Nuclear Reactor Control Simulation - WebSocket Web UI Test")
    print("=" * 60)
    print("NEW FEATURES:")
    print("✓ WebSocket real-time communication")
    print("✓ Instant data updates (no polling delays)")
    print("✓ Smooth chart animations")
    print("✓ Better performance and user experience")
    print("=" * 60)
    
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
        
        print("3. Testing Flask app with WebSocket support...")
        from app import app, socketio
        print("   ✓ Flask app with WebSocket support imported successfully")
        
        print("4. Starting WebSocket-enabled web server...")
        print("   Open your browser to: http://localhost:5001")
        print("   Features:")
        print("   - Real-time data streaming via WebSocket")
        print("   - Instant chart updates (10Hz)")
        print("   - Smooth animations and transitions")
        print("   - Better performance than HTTP polling")
        print("   Press Ctrl+C to stop")
        print("-" * 60)
        
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
        print("\n\nShutting down WebSocket web server...")

if __name__ == '__main__':
    main()
