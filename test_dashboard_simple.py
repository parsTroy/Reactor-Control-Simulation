#!/usr/bin/env python3
"""
Simple Dashboard Test
Quick test to verify the dashboard is working correctly.
"""

import sys
import os
sys.path.append('build')
sys.path.append('python_ui')

from dashboard import ReactorDashboard

def test_dashboard():
    """Test basic dashboard functionality"""
    print("Testing Reactor Dashboard")
    print("=" * 30)
    
    # Create dashboard
    dashboard = ReactorDashboard()
    
    # Test 1: Create simulation
    print("1. Creating simulation...")
    dashboard.create_simulation(time_step=1e-6, power_setpoint=1.0)
    print("   ✓ Simulation created")
    
    # Test 2: Run simulation
    print("2. Running simulation...")
    times, powers, scram_status = dashboard.run_simulation(duration=0.01)
    print(f"   ✓ Simulation completed: {len(times)} time steps")
    print(f"   ✓ Final power: {powers[-1]:.6f}")
    
    # Test 3: Plot results
    print("3. Creating plot...")
    dashboard.plot_power_curve(times, powers, scram_status, 
                              "Test Plot", "test_plot.png")
    print("   ✓ Plot saved as test_plot.png")
    
    # Test 4: Export data
    print("4. Exporting data...")
    dashboard.export_data("test_data.csv")
    print("   ✓ Data exported to test_data.csv")
    
    # Test 5: System status
    print("5. System status:")
    status = dashboard.get_system_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n✓ All tests passed!")
    print("Dashboard is working correctly!")

if __name__ == "__main__":
    test_dashboard()
