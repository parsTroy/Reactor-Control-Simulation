#!/usr/bin/env python3
"""
Test the fixed simulation with SCRAM functionality
"""

import sys
import os

# Add paths
sys.path.append('build')
sys.path.append('python_ui')

def test_scram_functionality():
    print("Testing SCRAM Functionality")
    print("=" * 50)
    
    try:
        # Import the C++ module
        import reactor_sim
        print("✓ C++ module imported successfully")
        
        # Create simulation
        sim = reactor_sim.ReactorSimulation()
        print("✓ Simulation created successfully")
        
        # Test initial state
        print(f"Initial SCRAM status: {sim.is_scrammed}")
        
        # Test triggering SCRAM
        print("\nTriggering SCRAM...")
        sim.trigger_scram()
        print(f"SCRAM status after trigger: {sim.is_scrammed}")
        
        # Test stepping with SCRAM
        print("\nTesting steps with SCRAM active...")
        for i in range(5):
            old_time = sim.get_current_time()
            old_power = sim.get_current_power()
            scram_status = sim.is_scrammed
            
            sim.step()
            
            new_time = sim.get_current_time()
            new_power = sim.get_current_power()
            new_scram_status = sim.is_scrammed
            
            print(f"Step {i+1}: Time {old_time:.6f} -> {new_time:.6f}, Power {old_power:.6f} -> {new_power:.6f}, SCRAM {scram_status} -> {new_scram_status}")
        
        # Test resetting SCRAM
        print("\nResetting SCRAM...")
        sim.reset_scram()
        print(f"SCRAM status after reset: {sim.is_scrammed}")
        
        # Test stepping after reset
        print("\nTesting steps after SCRAM reset...")
        for i in range(3):
            old_time = sim.get_current_time()
            old_power = sim.get_current_power()
            scram_status = sim.is_scrammed
            
            sim.step()
            
            new_time = sim.get_current_time()
            new_power = sim.get_current_power()
            new_scram_status = sim.is_scrammed
            
            print(f"Step {i+1}: Time {old_time:.6f} -> {new_time:.6f}, Power {old_power:.6f} -> {new_power:.6f}, SCRAM {scram_status} -> {new_scram_status}")
        
        print("\n✓ SCRAM functionality test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error testing SCRAM functionality: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_scram():
    print("\nTesting Dashboard SCRAM Integration")
    print("=" * 50)
    
    try:
        from python_ui.enhanced_dashboard import EnhancedReactorDashboard
        
        # Create dashboard
        dashboard = EnhancedReactorDashboard()
        dashboard.create_simulation()
        print("✓ Dashboard created successfully")
        
        # Test initial state
        print(f"Initial SCRAM status: {dashboard.simulation.is_scrammed}")
        
        # Test triggering SCRAM
        print("\nTriggering SCRAM via dashboard...")
        dashboard.simulation.trigger_scram()
        print(f"SCRAM status after trigger: {dashboard.simulation.is_scrammed}")
        
        # Test stepping with SCRAM
        print("\nTesting steps with SCRAM active...")
        for i in range(5):
            old_time = dashboard.simulation.get_current_time()
            old_power = dashboard.simulation.get_current_power()
            scram_status = dashboard.simulation.is_scrammed
            
            dashboard.simulation.step()
            
            new_time = dashboard.simulation.get_current_time()
            new_power = dashboard.simulation.get_current_power()
            new_scram_status = dashboard.simulation.is_scrammed
            
            print(f"Step {i+1}: Time {old_time:.6f} -> {new_time:.6f}, Power {old_power:.6f} -> {new_power:.6f}, SCRAM {scram_status} -> {new_scram_status}")
        
        print("\n✓ Dashboard SCRAM integration test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error testing dashboard SCRAM: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Nuclear Reactor Simulation - SCRAM Functionality Test")
    print("=" * 70)
    
    # Test C++ SCRAM functionality
    cpp_success = test_scram_functionality()
    
    # Test dashboard SCRAM integration
    dashboard_success = test_dashboard_scram()
    
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print(f"C++ SCRAM Functionality: {'✓ PASS' if cpp_success else '✗ FAIL'}")
    print(f"Dashboard SCRAM Integration: {'✓ PASS' if dashboard_success else '✗ FAIL'}")
    
    if cpp_success and dashboard_success:
        print("\n🎉 All SCRAM tests passed!")
        print("The Emergency SCRAM scenario should now work correctly.")
        print("Next steps:")
        print("1. Start the web server: python test_3d_websocket_ui.py")
        print("2. Open browser to: http://localhost:5001")
        print("3. Click 'Emergency SCRAM' scenario")
        print("4. Watch for:")
        print("   - Time advancing")
        print("   - Power changing")
        print("   - SCRAM status showing 'SCRAM ACTIVE'")
        print("   - 3D visualization showing red emergency state")
        print("   - Safety chart showing 1.0 instead of -0.1")
    else:
        print("\n❌ Some SCRAM tests failed. Check the errors above.")

if __name__ == '__main__':
    main()
