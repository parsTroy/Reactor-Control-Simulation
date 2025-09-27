#!/usr/bin/env python3
"""
Debug test for the C++ simulation to verify it's working properly
"""

import sys
import os

# Add paths
sys.path.append('build')
sys.path.append('python_ui')

def test_cpp_simulation():
    print("Testing C++ Simulation Step Function")
    print("=" * 50)
    
    try:
        # Import the C++ module
        import reactor_sim
        print("✓ C++ module imported successfully")
        
        # Create simulation
        sim = reactor_sim.ReactorSimulation()
        print("✓ Simulation created successfully")
        
        # Test initial state
        print(f"Initial time: {sim.get_current_time()}")
        print(f"Initial power: {sim.get_current_power()}")
        print(f"Initial SCRAM status: {sim.is_scrammed}")
        
        # Test stepping
        print("\nTesting simulation steps...")
        for i in range(10):
            old_time = sim.get_current_time()
            old_power = sim.get_current_power()
            
            sim.step()
            
            new_time = sim.get_current_time()
            new_power = sim.get_current_power()
            
            print(f"Step {i+1}: Time {old_time:.6f} -> {new_time:.6f}, Power {old_power:.6f} -> {new_power:.6f}")
            
            # Check if time is advancing
            if new_time <= old_time:
                print(f"⚠️  WARNING: Time not advancing! {old_time:.6f} -> {new_time:.6f}")
            else:
                print(f"✓ Time advancing correctly")
        
        print("\n✓ C++ simulation test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error testing C++ simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_simulation():
    print("\nTesting Dashboard Simulation")
    print("=" * 50)
    
    try:
        from python_ui.enhanced_dashboard import EnhancedReactorDashboard
        
        # Create dashboard
        dashboard = EnhancedReactorDashboard()
        dashboard.create_simulation()
        print("✓ Dashboard created successfully")
        
        # Test initial state
        print(f"Initial time: {dashboard.simulation.get_current_time()}")
        print(f"Initial power: {dashboard.simulation.get_current_power()}")
        print(f"Initial SCRAM status: {dashboard.simulation.is_scrammed}")
        
        # Test stepping
        print("\nTesting dashboard simulation steps...")
        for i in range(10):
            old_time = dashboard.simulation.get_current_time()
            old_power = dashboard.simulation.get_current_power()
            
            dashboard.simulation.step()
            
            new_time = dashboard.simulation.get_current_time()
            new_power = dashboard.simulation.get_current_power()
            
            print(f"Step {i+1}: Time {old_time:.6f} -> {new_time:.6f}, Power {old_power:.6f} -> {new_power:.6f}")
            
            # Check if time is advancing
            if new_time <= old_time:
                print(f"⚠️  WARNING: Time not advancing! {old_time:.6f} -> {new_time:.6f}")
            else:
                print(f"✓ Time advancing correctly")
        
        print("\n✓ Dashboard simulation test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error testing dashboard simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Nuclear Reactor Simulation Debug Test")
    print("=" * 60)
    
    # Test C++ simulation directly
    cpp_success = test_cpp_simulation()
    
    # Test dashboard simulation
    dashboard_success = test_dashboard_simulation()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"C++ Simulation: {'✓ PASS' if cpp_success else '✗ FAIL'}")
    print(f"Dashboard Simulation: {'✓ PASS' if dashboard_success else '✗ FAIL'}")
    
    if cpp_success and dashboard_success:
        print("\n🎉 All tests passed! The simulation should be working.")
        print("If the web UI still shows time not advancing, check:")
        print("1. WebSocket connection status")
        print("2. Browser console for errors")
        print("3. Server console for debug output")
    else:
        print("\n❌ Some tests failed. The simulation has issues that need to be fixed.")

if __name__ == '__main__':
    main()
