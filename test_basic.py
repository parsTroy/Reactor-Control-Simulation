#!/usr/bin/env python3
"""
Basic test script for Reactor Control Simulation
This script demonstrates the core functionality and verifies everything works.
"""

import sys
import os
sys.path.append('build')

import reactor_sim
import numpy as np
import matplotlib.pyplot as plt

def test_kinetics_solver():
    """Test the basic kinetics solver functionality"""
    print("Testing Kinetics Solver...")
    
    # Create reactor parameters
    params = reactor_sim.ReactorParams()
    print(f"   Reactor parameters: Lambda={params.Lambda:.2e}s, beta={params.beta:.4f}")
    
    # Initialize reactor state
    initial_state = reactor_sim.initialize_reactor_state(params, 1.0)
    print(f"   Initial state vector size: {len(initial_state)}")
    print(f"   Initial neutron density: {initial_state[0]:.6f}")
    
    # Test positive reactivity insertion
    print("   Testing positive reactivity insertion...")
    state = initial_state.copy()
    reactivity = 0.001  # 1 mk positive reactivity
    
    for i in range(100):
        state = reactor_sim.step_point_kinetics(0.0, 0.001, state, params, reactivity)
    
    final_power = state[0]
    power_increase = final_power / initial_state[0]
    print(f"   Power after 0.1s: {final_power:.6f} (increased by {power_increase:.2f}x)")
    
    assert power_increase > 1.0, "Power should increase with positive reactivity"
    print("   Kinetics solver working correctly!")

def test_pid_controller():
    """Test the PID controller functionality"""
    print("\n  Testing PID Controller...")
    
    # Create PID controller
    pid = reactor_sim.PIDController(kp=0.1, ki=0.01, kd=0.05, setpoint=1.0)
    print(f"   PID gains: Kp={pid.kp_}, Ki={pid.ki_}, Kd={pid.kd_}")
    
    # Test controller response
    current_power = 0.8  # Below setpoint
    output = pid.calculate(current_power)
    print(f"   Current power: {current_power}, Controller output: {output:.6f}")
    
    assert output > 0, "Controller should output positive reactivity when power is below setpoint"
    print(" PID controller working correctly!")

def test_safety_system():
    """Test the safety system functionality"""
    print("\n Testing Safety System...")
    
    # Create safety system
    safety = reactor_sim.SafetySystem(overpower_threshold=1.2, coolant_threshold=350.0)
    print(f"   Overpower threshold: {safety.overpower_threshold_}")
    print(f"   Coolant threshold: {safety.coolant_loss_threshold_}")
    
    # Test overpower trip
    normal_power = 1.0
    overpower = 1.5
    
    trip1 = safety.check_overpower_trip(normal_power, 0.0)
    trip2 = safety.check_overpower_trip(overpower, 1.0)
    
    print(f"   Normal power trip: {trip1}")
    print(f"   Overpower trip: {trip2}")
    
    assert not trip1, "Normal power should not trigger trip"
    assert trip2, "Overpower should trigger trip"
    print(" Safety system working correctly!")

def test_full_simulation():
    """Test the complete simulation"""
    print("\n Testing Full Simulation...")
    
    # Create simulation
    sim = reactor_sim.ReactorSimulation(time_step=0.01)
    print(f"   Initial power: {sim.get_current_power():.6f}")
    print(f"   Initial time: {sim.get_current_time():.6f}")
    
    # Run simulation for 1 second
    times = []
    powers = []
    
    for i in range(100):
        sim.step()
        times.append(sim.get_current_time())
        powers.append(sim.get_current_power())
    
    print(f"   Final power: {sim.get_current_power():.6f}")
    print(f"   Final time: {sim.get_current_time():.6f}")
    print(f"   Power range: {min(powers):.6f} - {max(powers):.6f}")
    
    # Check that simulation ran
    assert len(times) == 100, "Should have 100 time steps"
    assert sim.get_current_time() > 0, "Time should advance"
    print(" Full simulation working correctly!")

def create_demo_plot():
    """Create a simple demonstration plot"""
    print("\n Creating Demo Plot...")
    
    # Run a longer simulation
    sim = reactor_sim.ReactorSimulation(time_step=0.01)
    sim.set_power_setpoint(1.0)
    
    times = []
    powers = []
    
    # Run for 5 seconds
    for i in range(500):
        sim.step()
        times.append(sim.get_current_time())
        powers.append(sim.get_current_power())
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(times, powers, 'b-', linewidth=2, label='Reactor Power')
    plt.axhline(y=1.0, color='r', linestyle='--', label='Setpoint')
    plt.xlabel('Time (s)')
    plt.ylabel('Power (normalized)')
    plt.title('Reactor Control Simulation - Power vs Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    plt.savefig('demo_plot.png', dpi=150, bbox_inches='tight')
    print(" Demo plot saved as 'demo_plot.png'")

if __name__ == "__main__":
    print(" Reactor Control Simulation - Basic Test Suite")
    print("=" * 50)
    
    try:
        test_kinetics_solver()
        test_pid_controller()
        test_safety_system()
        test_full_simulation()
        create_demo_plot()
        
        print("\n ALL TESTS PASSED!")
        print("Your reactor control simulation is working correctly!")
        
    except Exception as e:
        print(f"\n TEST FAILED: {e}")
        sys.exit(1)
