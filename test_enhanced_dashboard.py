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
    
    # Test 1: Create dashboard
    print("1. Creating dashboard...")
    dashboard = EnhancedReactorDashboard()
    print("   Dashboard created")
    
    # Test 2: Create simulation
    print("2. Creating simulation...")
    dashboard.create_simulation()
    print("   Simulation created")
    
    # Test 3: Run simulation
    print("3. Running simulation...")
    times, powers, scram_status, events = dashboard.run_simulation(duration=0.01)
    print(f"   Simulation completed: {len(times)} time steps")
    
    # Test 4: Enhanced plotting
    print("4. Creating enhanced plot...")
    dashboard.plot_enhanced_power_curve(times, powers, scram_status, events,
                                       "Enhanced Test Plot", "enhanced_test.png")
    print("   Enhanced plot created")
    
    # Test 5: Data export
    print("5. Exporting data...")
    dashboard.export_enhanced_data("enhanced_test_data.csv")
    print("   Data exported")
    
    print("\nAll enhanced dashboard tests passed!")

if __name__ == "__main__":
    test_enhanced_dashboard()
