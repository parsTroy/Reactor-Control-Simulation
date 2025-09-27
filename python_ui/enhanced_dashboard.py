#!/usr/bin/env python3
"""
Enhanced Reactor Control Simulation Dashboard
Interactive dashboard with advanced logging, annotations, and configuration management.
"""

import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import matplotlib.patches as patches

# Add the build directory to the path to import our C++ module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'build'))

try:
    import reactor_sim
except ImportError:
    print("Error: Could not import reactor_sim module.")
    print("Make sure you have built the C++ project and the Python bindings are available.")
    sys.exit(1)

class EnhancedReactorDashboard:
    """Enhanced dashboard with advanced logging and visualization"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.simulation = None
        self.data_log = []
        self.event_log = []
        self.is_running = False
        self.config = self.load_config(config_file)
        
    def load_config(self, config_file: Optional[str] = None) -> Dict:
        """Load configuration from JSON file or use defaults"""
        default_config = {
            "simulation": {
                "time_step": 1e-6,
                "default_power_setpoint": 1.0,
                "log_interval": 1000  # Log every N steps
            },
            "pid_controller": {
                "kp": 0.1,
                "ki": 0.01,
                "kd": 0.05,
                "output_limits": [-0.1, 0.1],
                "rate_limits": [-0.01, 0.01]
            },
            "safety_systems": {
                "overpower_threshold": 1.2,
                "coolant_loss_threshold": 350.0,
                "scram_reactivity": -0.1,
                "scram_duration": 10.0
            },
            "visualization": {
                "figure_size": [12, 8],
                "dpi": 150,
                "colors": {
                    "power": "blue",
                    "setpoint": "green",
                    "scram": "red",
                    "trip": "orange"
                }
            }
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                # Merge with defaults
                self._merge_config(default_config, user_config)
                print(f"Configuration loaded from {config_file}")
            except Exception as e:
                print(f"Error loading config file: {e}")
                print("Using default configuration")
        else:
            print("Using default configuration")
            
        return default_config
    
    def _merge_config(self, default: Dict, user: Dict) -> None:
        """Recursively merge user config into default config"""
        for key, value in user.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
    
    def save_config(self, filename: str) -> None:
        """Save current configuration to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"Configuration saved to {filename}")
    
    def create_simulation(self, **kwargs):
        """Create a new reactor simulation with configuration"""
        # Override defaults with kwargs
        sim_config = self.config["simulation"].copy()
        sim_config.update(kwargs)
        
        print(f"Creating reactor simulation with configuration:")
        for key, value in sim_config.items():
            print(f"  {key}: {value}")
        
        self.simulation = reactor_sim.ReactorSimulation(time_step=sim_config["time_step"])
        self.simulation.set_power_setpoint(sim_config["default_power_setpoint"])
        
        # Note: PID controller configuration would need to be implemented
        # in the C++ simulation core to be accessible here
        print("  Note: PID controller configuration loaded but not yet applied to simulation")
        
        self.data_log = []
        self.event_log = []
        print("Simulation created successfully!")
    
    def log_event(self, event_type: str, message: str, data: Dict = None):
        """Log an event with timestamp"""
        event = {
            "timestamp": datetime.now(),
            "simulation_time": self.simulation.get_current_time() if self.simulation else 0.0,
            "event_type": event_type,
            "message": message,
            "data": data or {}
        }
        self.event_log.append(event)
        print(f"[{event['timestamp'].strftime('%H:%M:%S.%f')[:-3]}] {event_type}: {message}")
    
    def run_simulation(self, duration: float, power_setpoint: Optional[float] = None, 
                      reactivity_insertion: Optional[float] = None) -> Tuple[List, List, List, List]:
        """Run reactor simulation with enhanced logging"""
        if self.simulation is None:
            self.log_event("ERROR", "No simulation created. Call create_simulation() first.")
            return None, None, None, None
            
        if power_setpoint is not None:
            self.simulation.set_power_setpoint(power_setpoint)
            self.log_event("CONFIG", f"Power setpoint changed to {power_setpoint}")
            
        self.log_event("SIMULATION", f"Starting simulation for {duration:.3f} seconds")
        
        # Calculate number of steps
        time_step = self.config["simulation"]["time_step"]
        num_steps = int(duration / time_step)
        log_interval = self.config["simulation"]["log_interval"]
        
        # Run simulation with enhanced logging
        times = []
        powers = []
        reactivities = []
        scram_status = []
        events = []
        
        for i in range(num_steps):
            # Store previous state for comparison
            prev_power = self.simulation.get_current_power()
            prev_scram = self.simulation.is_scrammed
            
            # Run simulation step
            self.simulation.step()
            
            # Get current state
            current_time = self.simulation.get_current_time()
            current_power = self.simulation.get_current_power()
            current_scram = self.simulation.is_scrammed
            
            # Check for events
            if current_scram and not prev_scram:
                self.log_event("SAFETY", "SCRAM initiated - Overpower or coolant loss detected", 
                             {"power": current_power, "time": current_time})
                events.append(("SCRAM", current_time, current_power))
            elif not current_scram and prev_scram:
                self.log_event("SAFETY", "SCRAM cleared - Reactor back to normal operation",
                             {"power": current_power, "time": current_time})
                events.append(("SCRAM_CLEAR", current_time, current_power))
            
            # Check for power excursions
            if abs(current_power - 1.0) > 0.1:  # 10% deviation from normal
                if current_power > 1.1:
                    self.log_event("WARNING", f"High power excursion: {current_power:.3f}",
                                 {"power": current_power, "time": current_time})
                    events.append(("HIGH_POWER", current_time, current_power))
                elif current_power < 0.9:
                    self.log_event("WARNING", f"Low power excursion: {current_power:.3f}",
                                 {"power": current_power, "time": current_time})
                    events.append(("LOW_POWER", current_time, current_power))
            
            # Store data
            times.append(current_time)
            powers.append(current_power)
            scram_status.append(current_scram)
            
            # Log data at specified intervals
            if i % log_interval == 0:
                self.data_log.append({
                    "timestamp": datetime.now(),
                    "simulation_time": current_time,
                    "power": current_power,
                    "scrammed": current_scram,
                    "step": i
                })
        
        self.log_event("SIMULATION", f"Simulation completed. Final power: {powers[-1]:.6f}")
        return times, powers, scram_status, events
    
    def plot_enhanced_power_curve(self, times: List, powers: List, scram_status: List, 
                                events: List, title: str = "Enhanced Reactor Power vs Time", 
                                save_file: Optional[str] = None):
        """Create enhanced plot with safety annotations and events"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.config["visualization"]["figure_size"])
        
        colors = self.config["visualization"]["colors"]
        
        # Main power curve
        ax1.plot(times, powers, color=colors["power"], linewidth=2, label='Reactor Power')
        
        # Add setpoint line
        setpoint = 1.0  # Default setpoint since we don't have a getter method
        ax1.axhline(y=setpoint, color=colors["setpoint"], linestyle=':', linewidth=2, 
                   label=f'Setpoint ({setpoint})')
        
        # Add safety threshold lines
        safety_config = self.config["safety_systems"]
        ax1.axhline(y=safety_config["overpower_threshold"], color=colors["trip"], 
                   linestyle='--', linewidth=1, alpha=0.7, label='Overpower Threshold')
        
        # Add SCRAM annotations
        scram_times = [t for t, s in zip(times, scram_status) if s]
        if scram_times:
            for i, scram_time in enumerate(scram_times):
                if i == 0:  # Only label the first one
                    ax1.axvline(x=scram_time, color=colors["scram"], linestyle='-', 
                               linewidth=3, alpha=0.8, label='SCRAM Active')
                else:
                    ax1.axvline(x=scram_time, color=colors["scram"], linestyle='-', 
                               linewidth=3, alpha=0.8)
        
        # Add event annotations
        for event_type, event_time, event_power in events:
            if event_type == "SCRAM":
                ax1.annotate('SCRAM!', xy=(event_time, event_power), 
                           xytext=(event_time, event_power + 0.1),
                           arrowprops=dict(arrowstyle='->', color='red', lw=2),
                           fontsize=12, color='red', weight='bold')
            elif event_type == "HIGH_POWER":
                ax1.annotate('High Power', xy=(event_time, event_power),
                           xytext=(event_time, event_power + 0.05),
                           arrowprops=dict(arrowstyle='->', color='orange', lw=1),
                           fontsize=10, color='orange')
            elif event_type == "LOW_POWER":
                ax1.annotate('Low Power', xy=(event_time, event_power),
                           xytext=(event_time, event_power - 0.05),
                           arrowprops=dict(arrowstyle='->', color='orange', lw=1),
                           fontsize=10, color='orange')
        
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Power (normalized)')
        ax1.set_title(title)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Second subplot: SCRAM status
        scram_binary = [1 if s else 0 for s in scram_status]
        ax2.fill_between(times, 0, scram_binary, color=colors["scram"], alpha=0.7, 
                        label='SCRAM Status')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('SCRAM Active')
        ax2.set_title('Safety System Status')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_ylim(-0.1, 1.1)
        
        plt.tight_layout()
        
        if save_file:
            plt.savefig(save_file, dpi=self.config["visualization"]["dpi"], 
                       bbox_inches='tight')
            print(f"Enhanced plot saved as {save_file}")
        
        plt.show()
    
    def export_enhanced_data(self, filename: str = "enhanced_reactor_data.csv"):
        """Export comprehensive simulation data to CSV"""
        if not self.data_log:
            print("No data to export. Run a simulation first.")
            return
        
        # Create comprehensive DataFrame
        df_data = pd.DataFrame(self.data_log)
        df_events = pd.DataFrame(self.event_log)
        
        # Save data log
        df_data.to_csv(filename, index=False)
        print(f"Simulation data exported to {filename}")
        
        # Save event log
        event_filename = filename.replace('.csv', '_events.csv')
        df_events.to_csv(event_filename, index=False)
        print(f"Event log exported to {event_filename}")
        
        # Save configuration
        config_filename = filename.replace('.csv', '_config.json')
        self.save_config(config_filename)
        print(f"Configuration saved to {config_filename}")
    
    def run_interactive_scenario(self, scenario_name: str, duration: float = 0.1):
        """Run an interactive scenario with enhanced logging and visualization"""
        print(f"\n{'='*60}")
        print(f"Running Interactive Scenario: {scenario_name.upper()}")
        print(f"{'='*60}")
        
        if scenario_name == "normal_operation":
            self.create_simulation()
            times, powers, scram_status, events = self.run_simulation(duration)
            self.plot_enhanced_power_curve(times, powers, scram_status, events,
                                         "Normal Reactor Operation", "enhanced_normal.png")
            
        elif scenario_name == "power_ramp":
            self.create_simulation()
            # Gradual power increase
            for setpoint in [1.0, 1.1, 1.2, 1.3]:
                times, powers, scram_status, events = self.run_simulation(duration/4, 
                                                                        power_setpoint=setpoint)
                if setpoint == 1.0:
                    all_times, all_powers, all_scram, all_events = times, powers, scram_status, events
                else:
                    all_times.extend(times)
                    all_powers.extend(powers)
                    all_scram.extend(scram_status)
                    all_events.extend(events)
            
            self.plot_enhanced_power_curve(all_times, all_powers, all_scram, all_events,
                                         "Power Ramp Scenario", "enhanced_ramp.png")
            
        elif scenario_name == "emergency_scram":
            # Create simulation with high setpoint to trigger SCRAM
            self.create_simulation()
            times, powers, scram_status, events = self.run_simulation(duration, 
                                                                    power_setpoint=1.5)
            self.plot_enhanced_power_curve(times, powers, scram_status, events,
                                         "Emergency SCRAM Scenario", "enhanced_scram.png")
            
        elif scenario_name == "pid_tuning_demo":
            # Test different PID settings
            pid_configs = [
                {"kp": 0.05, "ki": 0.005, "kd": 0.01, "name": "Conservative"},
                {"kp": 0.1, "ki": 0.01, "kd": 0.05, "name": "Balanced"},
                {"kp": 0.2, "ki": 0.02, "kd": 0.1, "name": "Aggressive"}
            ]
            
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))
            
            for i, config in enumerate(pid_configs):
                self.create_simulation()
                # Update PID settings
                self.config["pid_controller"].update(config)
                
                times, powers, scram_status, events = self.run_simulation(duration)
                
                axes[i].plot(times, powers, 'b-', linewidth=2, label='Power')
                axes[i].axhline(y=1.0, color='g', linestyle=':', label='Setpoint')
                axes[i].set_title(f'{config["name"]} PID (Kp={config["kp"]})')
                axes[i].set_xlabel('Time (s)')
                axes[i].set_ylabel('Power')
                axes[i].grid(True, alpha=0.3)
                axes[i].legend()
            
            plt.tight_layout()
            plt.savefig('enhanced_pid_tuning.png', dpi=150, bbox_inches='tight')
            print("PID tuning comparison saved as enhanced_pid_tuning.png")
            
        else:
            print(f"Unknown scenario: {scenario_name}")
            return None
        
        # Export data
        self.export_enhanced_data(f"enhanced_{scenario_name}_data.csv")
        
        return times, powers, scram_status, events
    
    def get_system_dashboard(self):
        """Get comprehensive system status for monitoring"""
        if self.simulation is None:
            return {"status": "No simulation active"}
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "simulation": {
                "current_power": f"{self.simulation.get_current_power():.6f}",
                "current_time": f"{self.simulation.get_current_time():.6f}",
                "scram_status": "ACTIVE" if self.simulation.is_scrammed else "NORMAL"
            },
            "safety": {
                "overpower_threshold": self.config["safety_systems"]["overpower_threshold"],
                "coolant_threshold": self.config["safety_systems"]["coolant_loss_threshold"],
                "scram_reactivity": self.config["safety_systems"]["scram_reactivity"]
            },
            "pid_controller": self.config["pid_controller"],
            "data_log_entries": len(self.data_log),
            "event_log_entries": len(self.event_log)
        }
        
        return status

def demonstrate_enhanced_dashboard():
    """Demonstrate the enhanced dashboard capabilities"""
    print("Enhanced Reactor Dashboard Demonstration")
    print("=" * 50)
    
    # Create enhanced dashboard
    dashboard = EnhancedReactorDashboard()
    
    # Run different scenarios
    scenarios = ["normal_operation", "power_ramp", "emergency_scram", "pid_tuning_demo"]
    
    for scenario in scenarios:
        print(f"\nRunning scenario: {scenario}")
        dashboard.run_interactive_scenario(scenario, duration=0.05)
    
    # Show system dashboard
    print("\nSystem Dashboard:")
    status = dashboard.get_system_dashboard()
    for key, value in status.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for subkey, subvalue in value.items():
                print(f"    {subkey}: {subvalue}")
        else:
            print(f"  {key}: {value}")
    
    print("\nEnhanced dashboard demonstration completed!")
    print("Check the generated plots and data files for detailed analysis.")

if __name__ == "__main__":
    demonstrate_enhanced_dashboard()
