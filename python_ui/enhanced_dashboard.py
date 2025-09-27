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
                "log_interval": 1000
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
    
    def create_simulation(self, **kwargs):
        """Create a new reactor simulation with configuration"""
        sim_config = self.config["simulation"].copy()
        sim_config.update(kwargs)
        
        self.simulation = reactor_sim.ReactorSimulation(time_step=sim_config["time_step"])
        self.simulation.set_power_setpoint(sim_config["default_power_setpoint"])
        
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
    
    def run_simulation(self, duration: float, power_setpoint: Optional[float] = None) -> Tuple[List, List, List, List]:
        """Run reactor simulation with enhanced logging"""
        if self.simulation is None:
            self.log_event("ERROR", "No simulation created. Call create_simulation() first.")
            return None, None, None, None
            
        if power_setpoint is not None:
            self.simulation.set_power_setpoint(power_setpoint)
            self.log_event("CONFIG", f"Power setpoint changed to {power_setpoint}")
            
        self.log_event("SIMULATION", f"Starting simulation for {duration:.3f} seconds")
        
        time_step = self.config["simulation"]["time_step"]
        num_steps = int(duration / time_step)
        log_interval = self.config["simulation"]["log_interval"]
        
        times = []
        powers = []
        scram_status = []
        events = []
        
        for i in range(num_steps):
            prev_power = self.simulation.get_current_power()
            prev_scram = self.simulation.is_scrammed
            
            self.simulation.step()
            
            current_time = self.simulation.get_current_time()
            current_power = self.simulation.get_current_power()
            current_scram = self.simulation.is_scrammed
            
            if current_scram and not prev_scram:
                self.log_event("SAFETY", "SCRAM initiated", 
                             {"power": current_power, "time": current_time})
                events.append(("SCRAM", current_time, current_power))
            
            times.append(current_time)
            powers.append(current_power)
            scram_status.append(current_scram)
            
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
        
        ax1.plot(times, powers, color=colors["power"], linewidth=2, label='Reactor Power')
        ax1.axhline(y=1.0, color=colors["setpoint"], linestyle=':', linewidth=2, label='Setpoint')
        
        safety_config = self.config["safety_systems"]
        ax1.axhline(y=safety_config["overpower_threshold"], color=colors["trip"], 
                   linestyle='--', linewidth=1, alpha=0.7, label='Overpower Threshold')
        
        scram_times = [t for t, s in zip(times, scram_status) if s]
        if scram_times:
            ax1.axvline(x=scram_times[0], color=colors["scram"], linestyle='-', 
                       linewidth=3, alpha=0.8, label='SCRAM Active')
        
        for event_type, event_time, event_power in events:
            if event_type == "SCRAM":
                ax1.annotate('SCRAM!', xy=(event_time, event_power), 
                           xytext=(event_time, event_power + 0.1),
                           arrowprops=dict(arrowstyle='->', color='red', lw=2),
                           fontsize=12, color='red', weight='bold')
        
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Power (normalized)')
        ax1.set_title(title)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
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
        
        df_data = pd.DataFrame(self.data_log)
        df_events = pd.DataFrame(self.event_log)
        
        df_data.to_csv(filename, index=False)
        print(f"Simulation data exported to {filename}")
        
        event_filename = filename.replace('.csv', '_events.csv')
        df_events.to_csv(event_filename, index=False)
        print(f"Event log exported to {event_filename}")
    
    def run_interactive_scenario(self, scenario_name: str, duration: float = 0.1):
        """Run an interactive scenario with enhanced logging and visualization"""
        print(f"\nRunning Interactive Scenario: {scenario_name.upper()}")
        
        if scenario_name == "normal_operation":
            self.create_simulation()
            times, powers, scram_status, events = self.run_simulation(duration)
            self.plot_enhanced_power_curve(times, powers, scram_status, events,
                                         "Normal Reactor Operation", "enhanced_normal.png")
            
        elif scenario_name == "power_ramp":
            self.create_simulation()
            all_times, all_powers, all_scram, all_events = [], [], [], []
            
            for setpoint in [1.0, 1.1, 1.2, 1.3]:
                times, powers, scram_status, events = self.run_simulation(duration/4, 
                                                                        power_setpoint=setpoint)
                all_times.extend(times)
                all_powers.extend(powers)
                all_scram.extend(scram_status)
                all_events.extend(events)
            
            self.plot_enhanced_power_curve(all_times, all_powers, all_scram, all_events,
                                         "Power Ramp Scenario", "enhanced_ramp.png")
            
        elif scenario_name == "emergency_scram":
            self.create_simulation()
            times, powers, scram_status, events = self.run_simulation(duration, 
                                                                    power_setpoint=1.5)
            self.plot_enhanced_power_curve(times, powers, scram_status, events,
                                         "Emergency SCRAM Scenario", "enhanced_scram.png")
        
        self.export_enhanced_data(f"enhanced_{scenario_name}_data.csv")
        return times, powers, scram_status, events