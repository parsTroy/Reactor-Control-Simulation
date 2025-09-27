#!/usr/bin/env python3
"""
Basic Dashboard Demo
Simple example showing how to use the reactor control simulation dashboard.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'build'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dashboard import ReactorDashboard

def main():
    print("Basic Reactor Dashboard Demo")
    print("=" * 40)
    
    # Create dashboard instance
    dashboard = ReactorDashboard()
    
    # Demo 1: Normal operation
    print("\nDemo 1: Normal Reactor Operation")
    print("-" * 30)
    dashboard.create_simulation(time_step=1e-6, power_setpoint=1.0)
    times, powers, scram_status = dashboard.run_simulation(duration=0.01)
    dashboard.plot_power_curve(times, powers, scram_status, 
                              "Normal Reactor Operation", "demo_normal.png")
    
    # Demo 2: Power increase scenario
    print("\nDemo 2: Power Increase Scenario")
    print("-" * 30)
    dashboard.run_scenario("power_increase", duration=0.02)
    
    # Demo 3: System status
    print("\nDemo 3: System Status")
    print("-" * 30)
    status = dashboard.get_system_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    # Demo 4: Data export
    print("\nDemo 4: Data Export")
    print("-" * 30)
    dashboard.export_data("demo_data.csv")
    
    print("\nBasic demo completed!")
    print("Check the generated plots and data files.")

if __name__ == "__main__":
    main()
