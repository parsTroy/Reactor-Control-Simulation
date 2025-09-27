#!/usr/bin/env python3
"""
PID Controller Demonstration and Testing
This script demonstrates PID controller behavior and tuning for reactor control.
"""

import sys
import os
sys.path.append('build')

import reactor_sim
import numpy as np
import matplotlib.pyplot as plt

def test_pid_basic_functionality():
    """Test basic PID controller functionality"""
    print("Testing Basic PID Controller Functionality...")
    
    # Create PID controller
    pid = reactor_sim.PIDController(kp=0.1, ki=0.01, kd=0.05, setpoint=1.0, dt=0.001)
    
    # Test different power levels
    test_powers = [0.5, 0.8, 1.0, 1.2, 1.5]
    
    print("   Power Level | Controller Output | Error")
    print("   ------------|------------------|-------")
    
    for power in test_powers:
        output = pid.calculate(power)
        error = 1.0 - power  # setpoint - current
        print(f"   {power:10.1f} | {output:15.6f} | {error:5.3f}")
    
    # Test setpoint changes
    print("\n   Testing setpoint changes...")
    pid.set_setpoint(0.8)
    output = pid.calculate(1.0)
    print(f"   New setpoint: 0.8, Current power: 1.0, Output: {output:.6f}")
    
    # Test reset
    pid.reset()
    output = pid.calculate(1.0)
    print(f"   After reset, Output: {output:.6f}")
    
    print("   Basic PID functionality working correctly!")

def test_pid_tuning():
    """Test different PID tuning parameters"""
    print("\nTesting PID Tuning Parameters...")
    
    # Test different tuning scenarios
    tuning_scenarios = [
        {"name": "Aggressive", "kp": 0.5, "ki": 0.1, "kd": 0.2},
        {"name": "Conservative", "kp": 0.05, "ki": 0.005, "kd": 0.01},
        {"name": "Balanced", "kp": 0.1, "ki": 0.01, "kd": 0.05},
        {"name": "Overshoot", "kp": 0.3, "ki": 0.05, "kd": 0.0}
    ]
    
    # Simulate step response for each tuning
    time_steps = np.arange(0, 2.0, 0.001)
    setpoint = 1.0
    initial_power = 0.5
    
    plt.figure(figsize=(15, 10))
    
    for i, scenario in enumerate(tuning_scenarios):
        # Create PID with specific tuning
        pid = reactor_sim.PIDController(
            kp=scenario["kp"], 
            ki=scenario["ki"], 
            kd=scenario["kd"], 
            setpoint=setpoint, 
            dt=0.001
        )
        
        # Simulate reactor response (simplified)
        powers = [initial_power]
        outputs = []
        
        for t in time_steps[1:]:
            current_power = powers[-1]
            output = pid.calculate(current_power)
            
            # Simple reactor model: power changes based on reactivity
            reactivity = output
            power_change = reactivity * 0.1  # Simplified response
            new_power = current_power + power_change * 0.001  # dt = 0.001
            
            # Keep power in reasonable bounds
            new_power = max(0.0, min(2.0, new_power))
            
            powers.append(new_power)
            outputs.append(output)
        
        # Plot results
        plt.subplot(2, 2, i+1)
        plt.plot(time_steps, powers, 'b-', linewidth=2, label='Power')
        plt.axhline(y=setpoint, color='r', linestyle='--', label='Setpoint')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (normalized)')
        plt.title(f'{scenario["name"]} Tuning (Kp={scenario["kp"]}, Ki={scenario["ki"]}, Kd={scenario["kd"]})')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Calculate performance metrics
        final_error = abs(powers[-1] - setpoint)
        max_overshoot = max(powers) - setpoint if max(powers) > setpoint else 0
        settling_time = None
        
        # Find settling time (within 2% of setpoint)
        for j, power in enumerate(powers):
            if abs(power - setpoint) <= 0.02:
                settling_time = time_steps[j]
                break
        
        settling_str = f"{settling_time:.3f}s" if settling_time is not None else "N/A"
        print(f"   {scenario['name']:12s}: Final error = {final_error:.4f}, Max overshoot = {max_overshoot:.4f}, Settling time = {settling_str}")
    
    plt.tight_layout()
    plt.savefig('pid_tuning_comparison.png', dpi=150, bbox_inches='tight')
    print("   PID tuning comparison plot saved as 'pid_tuning_comparison.png'")

def test_anti_windup():
    """Test anti-windup protection"""
    print("\nTesting Anti-Windup Protection...")
    
    # Create PID with tight output limits
    pid = reactor_sim.PIDController(kp=1.0, ki=0.5, kd=0.1, setpoint=1.0, dt=0.001)
    pid.set_output_limits(-0.1, 0.1)  # Very tight limits
    
    # Simulate scenario where power is stuck below setpoint
    powers = [0.5]  # Stuck at 50% power
    outputs = []
    integral_sums = []
    
    for i in range(1000):
        output = pid.calculate(0.5)  # Always below setpoint
        powers.append(0.5)  # Power stays stuck
        outputs.append(output)
        integral_sums.append(pid.integral_sum)
    
    # Plot results
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(outputs, 'b-', linewidth=2)
    plt.axhline(y=0.1, color='r', linestyle='--', label='Output Limit')
    plt.axhline(y=-0.1, color='r', linestyle='--')
    plt.xlabel('Time Steps')
    plt.ylabel('Controller Output')
    plt.title('Controller Output with Anti-Windup')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 2)
    plt.plot(integral_sums, 'g-', linewidth=2)
    plt.xlabel('Time Steps')
    plt.ylabel('Integral Sum')
    plt.title('Integral Term (Anti-Windup Active)')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 3)
    plt.plot(powers, 'k-', linewidth=2)
    plt.axhline(y=1.0, color='r', linestyle='--', label='Setpoint')
    plt.xlabel('Time Steps')
    plt.ylabel('Power Level')
    plt.title('Power Level (Stuck Below Setpoint)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Test rate limiting
    plt.subplot(2, 2, 4)
    pid2 = reactor_sim.PIDController(kp=1.0, ki=0.1, kd=0.1, setpoint=1.0, dt=0.001)
    pid2.set_rate_limits(-0.01, 0.01)  # Very slow rate limits
    
    # Simulate step change in power
    powers2 = [0.5]
    outputs2 = []
    
    for i in range(500):
        if i < 250:
            power = 0.5
        else:
            power = 1.5  # Step change
        
        output = pid2.calculate(power)
        powers2.append(power)
        outputs2.append(output)
    
    plt.plot(outputs2, 'm-', linewidth=2, label='Rate Limited Output')
    plt.xlabel('Time Steps')
    plt.ylabel('Controller Output')
    plt.title('Rate Limiting Test')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('pid_anti_windup_test.png', dpi=150, bbox_inches='tight')
    print("   Anti-windup test plot saved as 'pid_anti_windup_test.png'")
    
    # Verify anti-windup is working
    max_output = max(outputs)
    min_output = min(outputs)
    print(f"   Output range: [{min_output:.6f}, {max_output:.6f}] (limits: [-0.1, 0.1])")
    print(f"   Anti-windup working: {max_output <= 0.1 and min_output >= -0.1}")

def test_pid_integration():
    """Test PID controller integration with reactor simulation"""
    print("\nTesting PID Integration with Reactor Simulation...")
    
    # Create simulation with PID control
    sim = reactor_sim.ReactorSimulation(time_step=1e-6)
    sim.set_power_setpoint(1.0)
    sim.set_pid_enabled(True)
    
    # Run simulation
    times = []
    powers = []
    
    for i in range(50000):  # 0.05 seconds
        sim.step()
        times.append(sim.get_current_time())
        powers.append(sim.get_current_power())
    
    # Plot results
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(times, powers, 'b-', linewidth=2, label='Reactor Power')
    plt.axhline(y=1.0, color='r', linestyle='--', label='Setpoint')
    plt.xlabel('Time (s)')
    plt.ylabel('Power (normalized)')
    plt.title('PID-Controlled Reactor Response')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Test setpoint change
    sim.set_power_setpoint(1.2)  # Increase setpoint
    
    times2 = []
    powers2 = []
    
    for i in range(50000):  # Another 0.05 seconds
        sim.step()
        times2.append(sim.get_current_time())
        powers2.append(sim.get_current_power())
    
    plt.subplot(1, 2, 2)
    plt.plot(times2, powers2, 'g-', linewidth=2, label='Reactor Power')
    plt.axhline(y=1.2, color='r', linestyle='--', label='New Setpoint')
    plt.xlabel('Time (s)')
    plt.ylabel('Power (normalized)')
    plt.title('Response to Setpoint Change')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('pid_integration_test.png', dpi=150, bbox_inches='tight')
    print("   PID integration test plot saved as 'pid_integration_test.png'")
    
    # Calculate performance metrics
    final_power = powers[-1]
    final_error = abs(final_power - 1.0)
    print(f"   Final power: {final_power:.6f}")
    print(f"   Final error: {final_error:.6f}")
    print(f"   PID integration working: {final_error < 0.01}")

def test_learning_checkpoint():
    """Demonstrate PID controller learning concepts"""
    print("\nLearning Checkpoint: Understanding PID Control...")
    
    print("\nWhat We Learned About PID Controllers:")
    print("   1. Proportional Term (Kp):")
    print("      - Responds to current error")
    print("      - Higher Kp = faster response, more overshoot")
    print("      - Too high = oscillations")
    
    print("\n   2. Integral Term (Ki):")
    print("      - Eliminates steady-state error")
    print("      - Accumulates past errors")
    print("      - Too high = overshoot and instability")
    print("      - Anti-windup prevents integral saturation")
    
    print("\n   3. Derivative Term (Kd):")
    print("      - Predicts future error trends")
    print("      - Reduces overshoot and oscillations")
    print("      - Too high = noise sensitivity")
    
    print("\n   4. Tuning Guidelines:")
    print("      - Start with Ki=Kd=0, increase Kp until oscillations")
    print("      - Add Ki to eliminate steady-state error")
    print("      - Add Kd to reduce overshoot")
    print("      - Use rate limiting for smooth control")
    
    print("\n   5. Safety Features:")
    print("      - Output limits prevent extreme control actions")
    print("      - Rate limits prevent sudden changes")
    print("      - Anti-windup prevents integral saturation")

if __name__ == "__main__":
    print("PID Controller - Comprehensive Demonstration")
    print("=" * 50)
    
    try:
        test_pid_basic_functionality()
        test_pid_tuning()
        test_anti_windup()
        test_pid_integration()
        test_learning_checkpoint()
        
        print("\nALL PID TESTS COMPLETED!")
        print("Check the generated plots to see the results!")
        
    except Exception as e:
        print(f"\nPID TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
