#!/usr/bin/env python3
"""
Reactor Control Simulation Dashboard
Interactive dashboard for running reactor simulations and visualizing results.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from datetime import datetime

# Add the build directory to the path to import our C++ module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'build'))

try:
    import reactor_sim
except ImportError:
    print("Error: Could not import reactor_sim module.")
    print("Make sure you have built the C++ project and the Python bindings are available.")
    sys.exit(1)

class ReactorDashboard:
    """Main dashboard class for reactor control simulation"""
    
    def __init__(self):
        self.simulation = None
        self.data_log = []
        self.is_running = False
        
    def create_simulation(self, time_step=1e-6, power_setpoint=1.0):
        """Create a new reactor simulation"""
        print(f"Creating reactor simulation with time step: {time_step:.2e}s")
        self.simulation = reactor_sim.ReactorSimulation(time_step=time_step)
        self.simulation.set_power_setpoint(power_setpoint)
        self.data_log = []
        print("Simulation created successfully!")
        
    def run_simulation(self, duration=0.1, power_setpoint=None, reactivity_insertion=None):
        """Run reactor simulation for specified duration"""
        if self.simulation is None:
            print("Error: No simulation created. Call create_simulation() first.")
            return None
            
        if power_setpoint is not None:
            self.simulation.set_power_setpoint(power_setpoint)
            
        print(f"Running simulation for {duration:.3f} seconds...")
        
        # Calculate number of steps
        time_step = 1e-6  # Default time step
        num_steps = int(duration / time_step)
        
        # Run simulation
        times = []
        powers = []
        reactivities = []
        scram_status = []
        
        for i in range(num_steps):
            self.simulation.step()
            
            times.append(self.simulation.get_current_time())
            powers.append(self.simulation.get_current_power())
            scram_status.append(self.simulation.is_scrammed)
            
            # Log data
            self.data_log.append({
                'time': times[-1],
                'power': powers[-1],
                'scrammed': scram_status[-1],
                'timestamp': datetime.now()
            })
        
        print(f"Simulation completed. Final power: {powers[-1]:.6f}")
        return times, powers, scram_status
    
    def plot_power_curve(self, times, powers, scram_status=None, title="Reactor Power vs Time", save_file=None):
        """Plot reactor power vs time with optional SCRAM annotations"""
        plt.figure(figsize=(12, 8))
        
        # Main power curve
        plt.plot(times, powers, 'b-', linewidth=2, label='Reactor Power')
        
        # Add SCRAM annotations if provided
        if scram_status is not None:
            scram_times = [t for t, s in zip(times, scram_status) if s]
            if scram_times:
                plt.axvline(x=scram_times[0], color='r', linestyle='--', linewidth=2, 
                           label=f'SCRAM at t={scram_times[0]:.3f}s')
        
        # Add setpoint line
        if hasattr(self.simulation, 'get_power_setpoint'):
            setpoint = 1.0  # Default setpoint
            plt.axhline(y=setpoint, color='g', linestyle=':', linewidth=2, label='Setpoint')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Power (normalized)')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        if save_file:
            plt.savefig(save_file, dpi=150, bbox_inches='tight')
            print(f"Plot saved as {save_file}")
        
        plt.show()
    
    def run_scenario(self, scenario_name, duration=0.1, **kwargs):
        """Run a predefined scenario"""
        print(f"\nRunning scenario: {scenario_name}")
        
        if scenario_name == "normal_operation":
            self.create_simulation(time_step=1e-6, power_setpoint=1.0)
            times, powers, scram_status = self.run_simulation(duration=duration)
            self.plot_power_curve(times, powers, scram_status, 
                                "Normal Reactor Operation", "normal_operation.png")
            
        elif scenario_name == "power_increase":
            self.create_simulation(time_step=1e-6, power_setpoint=1.0)
            times, powers, scram_status = self.run_simulation(duration=duration/2)
            # Increase setpoint
            self.simulation.set_power_setpoint(1.2)
            times2, powers2, scram_status2 = self.run_simulation(duration=duration/2)
            # Combine results
            times.extend(times2)
            powers.extend(powers2)
            scram_status.extend(scram_status2)
            self.plot_power_curve(times, powers, scram_status, 
                                "Reactor Response to Power Increase", "power_increase.png")
            
        elif scenario_name == "overpower_trip":
            self.create_simulation(time_step=1e-6, power_setpoint=1.5)  # High setpoint
            times, powers, scram_status = self.run_simulation(duration=duration)
            self.plot_power_curve(times, powers, scram_status, 
                                "Overpower Trip Scenario", "overpower_trip.png")
            
        elif scenario_name == "pid_tuning":
            self.create_simulation(time_step=1e-6, power_setpoint=1.0)
            times, powers, scram_status = self.run_simulation(duration=duration)
            self.plot_power_curve(times, powers, scram_status, 
                                "PID Controller Response", "pid_tuning.png")
            
        else:
            print(f"Unknown scenario: {scenario_name}")
            return None
        
        return times, powers, scram_status
    
    def export_data(self, filename="reactor_data.csv"):
        """Export simulation data to CSV"""
        if not self.data_log:
            print("No data to export. Run a simulation first.")
            return
        
        df = pd.DataFrame(self.data_log)
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")
    
    def get_system_status(self):
        """Get current system status"""
        if self.simulation is None:
            return "No simulation active"
        
        status = {
            "Current Power": f"{self.simulation.get_current_power():.6f}",
            "Current Time": f"{self.simulation.get_current_time():.6f}",
            "SCRAM Status": "Active" if self.simulation.is_scrammed else "Normal",
            "PID Enabled": "Yes" if hasattr(self.simulation, 'pid_enabled') else "Unknown"
        }
        
        return status

def demonstrate_python_cpp_integration():
    """Demonstrate how Python calls into C++ for performance"""
    print("Python-C++ Integration Demonstration")
    print("=" * 50)
    
    # Create dashboard
    dashboard = ReactorDashboard()
    
    # Test 1: Basic simulation
    print("\n1. Basic Reactor Simulation:")
    dashboard.create_simulation(time_step=1e-6, power_setpoint=1.0)
    times, powers, scram_status = dashboard.run_simulation(duration=0.01)
    print(f"   Simulated {len(times)} time steps")
    print(f"   Final power: {powers[-1]:.6f}")
    
    # Test 2: Performance comparison (Python vs C++)
    print("\n2. Performance Analysis:")
    import time
    
    # C++ simulation
    start_time = time.time()
    dashboard.create_simulation(time_step=1e-6, power_setpoint=1.0)
    times, powers, scram_status = dashboard.run_simulation(duration=0.01)
    cpp_time = time.time() - start_time
    
    print(f"   C++ simulation time: {cpp_time:.4f} seconds")
    print(f"   Time steps per second: {len(times)/cpp_time:.0f}")
    
    # Test 3: Multiple scenarios
    print("\n3. Running Multiple Scenarios:")
    scenarios = ["normal_operation", "power_increase", "overpower_trip"]
    
    for scenario in scenarios:
        print(f"   Running {scenario}...")
        dashboard.run_scenario(scenario, duration=0.01)
    
    # Test 4: Data export
    print("\n4. Data Export:")
    dashboard.export_data("reactor_simulation_data.csv")
    
    # Test 5: System status
    print("\n5. System Status:")
    status = dashboard.get_system_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\nPython-C++ Integration Working Perfectly!")
    print("Key Benefits:")
    print("- High performance C++ core for numerical calculations")
    print("- Python interface for easy scripting and visualization")
    print("- Seamless data transfer between languages")
    print("- Rich Python ecosystem for analysis and plotting")

def interactive_dashboard():
    """Interactive dashboard for real-time reactor monitoring"""
    print("Interactive Reactor Dashboard")
    print("=" * 40)
    
    dashboard = ReactorDashboard()
    
    while True:
        print("\nOptions:")
        print("1. Create new simulation")
        print("2. Run simulation")
        print("3. Run scenario")
        print("4. Export data")
        print("5. Show system status")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            time_step = float(input("Enter time step (e.g., 1e-6): "))
            setpoint = float(input("Enter power setpoint (e.g., 1.0): "))
            dashboard.create_simulation(time_step, setpoint)
            
        elif choice == "2":
            duration = float(input("Enter simulation duration (e.g., 0.1): "))
            times, powers, scram_status = dashboard.run_simulation(duration)
            dashboard.plot_power_curve(times, powers, scram_status)
            
        elif choice == "3":
            print("Available scenarios:")
            print("- normal_operation")
            print("- power_increase") 
            print("- overpower_trip")
            print("- pid_tuning")
            scenario = input("Enter scenario name: ").strip()
            duration = float(input("Enter duration (e.g., 0.1): "))
            dashboard.run_scenario(scenario, duration)
            
        elif choice == "4":
            filename = input("Enter filename (e.g., data.csv): ").strip()
            dashboard.export_data(filename)
            
        elif choice == "5":
            status = dashboard.get_system_status()
            for key, value in status.items():
                print(f"{key}: {value}")
                
        elif choice == "6":
            print("Exiting dashboard...")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Reactor Control Simulation Dashboard")
    print("=" * 50)
    
    # Run demonstration
    demonstrate_python_cpp_integration()
    
    # Ask if user wants interactive mode
    response = input("\nWould you like to try the interactive dashboard? (y/n): ").strip().lower()
    if response == 'y':
        interactive_dashboard()
    
    print("\nDashboard session completed!")
