#!/usr/bin/env python3
"""
Comprehensive Kinetics Solver Demonstration
This script shows different reactor behaviors with various reactivity insertions.
"""

import sys
import os
sys.path.append('build')

import reactor_sim
import numpy as np
import matplotlib.pyplot as plt

def test_constant_reactivity():
    """Test reactor response to constant reactivity insertion"""
    print("Testing Constant Reactivity Insertion...")
    
    # Create reactor parameters
    params = reactor_sim.ReactorParams()
    
    # Test different reactivity values
    reactivities = [0.001, 0.0, -0.001]  # 1 mk positive, zero, 1 mk negative
    colors = ['red', 'blue', 'green']
    labels = ['+1 mk (positive)', '0 mk (critical)', '-1 mk (negative)']
    
    plt.figure(figsize=(12, 8))
    
    for i, (rho, color, label) in enumerate(zip(reactivities, colors, labels)):
        # Initialize reactor
        state = reactor_sim.initialize_reactor_state(params, 1.0)
        
        # Run simulation
        times = []
        powers = []
        dt = 1e-6
        
        for t in np.arange(0, 0.01, dt):
            state = reactor_sim.step_point_kinetics(t, dt, state, params, rho)
            times.append(t)
            powers.append(state[0])
        
        # Plot results
        plt.subplot(2, 2, i+1)
        plt.plot(times, powers, color=color, linewidth=2, label=label)
        plt.xlabel('Time (s)')
        plt.ylabel('Power (normalized)')
        plt.title(f'Reactivity = {rho:.3f} ({label})')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Print results
        final_power = powers[-1]
        power_change = (final_power - 1.0) / 1.0 * 100
        print(f"   {label}: Final power = {final_power:.6f} ({power_change:+.2f}% change)")
    
    # Test PID control
    plt.subplot(2, 2, 4)
    print("\nTesting PID Control...")
    
    # Create simulation with PID
    sim = reactor_sim.ReactorSimulation(time_step=1e-6)
    sim.set_power_setpoint(1.0)
    
    times = []
    powers = []
    reactivities = []
    
    # Run for 0.01 seconds
    for i in range(10000):
        sim.step()
        times.append(sim.get_current_time())
        powers.append(sim.get_current_power())
        # Get current reactivity (simplified - in real implementation we'd track this)
        reactivities.append(0.0)  # Placeholder
    
    plt.plot(times, powers, 'purple', linewidth=2, label='PID Controlled')
    plt.axhline(y=1.0, color='black', linestyle='--', label='Setpoint')
    plt.xlabel('Time (s)')
    plt.ylabel('Power (normalized)')
    plt.title('PID Control (Setpoint = 1.0)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    print(f"   PID Control: Final power = {powers[-1]:.6f}")
    
    plt.tight_layout()
    plt.savefig('kinetics_demo.png', dpi=150, bbox_inches='tight')
    print("   Demo plot saved as 'kinetics_demo.png'")

def test_numerical_stability():
    """Test numerical stability with different time steps"""
    print("\nTesting Numerical Stability...")
    
    params = reactor_sim.ReactorParams()
    state = reactor_sim.initialize_reactor_state(params, 1.0)
    reactivity = 0.001  # 1 mk positive
    
    # Test different time steps
    time_steps = [1e-6, 5e-6, 1e-5, 2e-5]
    
    plt.figure(figsize=(10, 6))
    
    for dt in time_steps:
        try:
            state_copy = state.copy()
            times = []
            powers = []
            
            for t in np.arange(0, 0.001, dt):  # Short simulation
                state_copy = reactor_sim.step_point_kinetics(t, dt, state_copy, params, reactivity)
                times.append(t)
                powers.append(state_copy[0])
            
            plt.plot(times, powers, linewidth=2, label=f'dt = {dt:.0e}s')
            print(f"   dt = {dt:.0e}s: Stable, final power = {powers[-1]:.6f}")
            
        except Exception as e:
            print(f"   dt = {dt:.0e}s: UNSTABLE - {e}")
    
    plt.xlabel('Time (s)')
    plt.ylabel('Power (normalized)')
    plt.title('Numerical Stability Test (Reactivity = +1 mk)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('stability_test.png', dpi=150, bbox_inches='tight')
    print("   Stability test plot saved as 'stability_test.png'")

def test_learning_checkpoint():
    """Demonstrate the learning checkpoint concepts"""
    print("\nLearning Checkpoint: Understanding Numerical Integration...")
    
    print("\nWhat We Learned About Numerical Integration:")
    print("   1. Time Step Size Matters:")
    print("      - Too large → Numerical instability (exponential growth)")
    print("      - Too small → Slow computation")
    print("      - Rule of thumb: dt < Λ/10 (generation time / 10)")
    
    print("\n   2. Euler's Method:")
    print("      - Simple: y_next = y + dt * dy/dt")
    print("      - First-order accuracy")
    print("      - Can be unstable for stiff ODEs")
    
    print("\n   3. Bounds Checking:")
    print("      - Physical constraints (neutron density ≥ 0)")
    print("      - Reasonable limits (prevent overflow)")
    print("      - Error detection (catch instabilities)")
    
    print("\n   4. Reactor Physics:")
    print("      - Positive reactivity → Power increases")
    print("      - Negative reactivity → Power decreases")
    print("      - Zero reactivity → Steady state")
    
    print("\n   5. PID Control:")
    print("      - Automatically adjusts reactivity")
    print("      - Maintains desired power level")
    print("      - Includes safety limits")

if __name__ == "__main__":
    print("Reactor Kinetics Solver - Comprehensive Demo")
    print("=" * 60)
    
    try:
        test_constant_reactivity()
        test_numerical_stability()
        test_learning_checkpoint()
        
        print("\nALL DEMONSTRATIONS COMPLETED!")
        print("Check the generated plots to see the results!")
        
    except Exception as e:
        print(f"\nDEMO FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
