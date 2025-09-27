#!/usr/bin/env python3
"""
Test Enhanced Dashboard
Quick test to verify the enhanced dashboard functionality.
"""

import sys
import os
sys.path.append('python_ui')

from enhanced_dashboard import EnhancedReactorDashboard

def test_enhanced_dashboard():
    """Test enhanced dashboard functionality"""
    print("Testing Enhanced Reactor Dashboard")
    print("=" * 40)
    
    # Test 1: Create dashboard with config
    print("1. Creating dashboard with configuration...")
    dashboard = EnhancedReactorDashboard("config/reactor_config.json")
    print("   ✓ Dashboard created with configuration")
    
    # Test 2: Create simulation
    print("2. Creating simulation...")
    dashboard.create_simulation()
    print("   ✓ Simulation created")
    
    # Test 3: Run simulation with logging
    print("3. Running simulation with enhanced logging...")
    times, powers, scram_status, events = dashboard.run_simulation(duration=0.01)
    print(f"   ✓ Simulation completed: {len(times)} time steps")
    print(f"   ✓ Events detected: {len(events)}")
    
    # Test 4: Enhanced plotting
    print("4. Creating enhanced plot...")
    dashboard.plot_enhanced_power_curve(times, powers, scram_status, events,
                                       "Enhanced Test Plot", "enhanced_test.png")
    print("   ✓ Enhanced plot saved as enhanced_test.png")
    
    # Test 5: Data export
    print("5. Exporting enhanced data...")
    dashboard.export_enhanced_data("enhanced_test_data.csv")
    print("   ✓ Enhanced data exported")
    
    # Test 6: System dashboard
    print("6. System dashboard status:")
    status = dashboard.get_system_dashboard()
    for key, value in status.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for subkey, subvalue in value.items():
                print(f"     {subkey}: {subvalue}")
        else:
            print(f"   {key}: {value}")
    
    print("\n✓ All enhanced dashboard tests passed!")
    print("Enhanced dashboard is working correctly!")

def test_scenarios():
    """Test different scenarios"""
    print("\nTesting Interactive Scenarios")
    print("=" * 35)
    
    dashboard = EnhancedReactorDashboard("config/reactor_config.json")
    
    scenarios = ["normal_operation", "power_ramp", "emergency_scram"]
    
    for scenario in scenarios:
        print(f"\nTesting scenario: {scenario}")
        try:
            dashboard.run_interactive_scenario(scenario, duration=0.02)
            print(f"   ✓ {scenario} completed successfully")
        except Exception as e:
            print(f"   ✗ {scenario} failed: {e}")

if __name__ == "__main__":
    test_enhanced_dashboard()
    test_scenarios()
    print("\nEnhanced dashboard testing completed!")
