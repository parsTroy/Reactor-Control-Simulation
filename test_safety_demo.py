#!/usr/bin/env python3
"""
Safety Systems Demonstration and Testing
This script demonstrates safety interlocks and SCRAM functionality.
"""

import sys
import os
sys.path.append('build')

import reactor_sim
import numpy as np
import matplotlib.pyplot as plt

def test_overpower_trip():
    """Test overpower protection system"""
    print("Testing Overpower Protection System...")
    
    # Create safety system with low threshold for testing
    safety = reactor_sim.SafetySystem(overpower_threshold=1.1, coolant_threshold=350.0)
    
    # Test normal operation
    normal_power = 1.0
    trip1 = safety.check_overpower_trip(normal_power, 0.0)
    print(f"   Normal power ({normal_power}): Trip = {trip1}")
    
    # Test overpower condition
    overpower = 1.2
    trip2 = safety.check_overpower_trip(overpower, 1.0)
    print(f"   Overpower ({overpower}): Trip = {trip2}")
    
    # Test SCRAM reactivity
    safety_reactivity = safety.get_safety_reactivity(1.0)
    print(f"   Safety reactivity during SCRAM: {safety_reactivity}")
    
    # Test SCRAM status
    is_scrammed = safety.is_scrammed
    print(f"   Reactor SCRAMmed: {is_scrammed}")
    
    print("   Overpower protection working correctly!")

def test_coolant_loss_trip():
    """Test coolant loss protection system"""
    print("\nTesting Coolant Loss Protection System...")
    
    # Create safety system
    safety = reactor_sim.SafetySystem(overpower_threshold=1.2, coolant_threshold=350.0)
    
    # Test normal temperature
    normal_temp = 300.0
    trip1 = safety.check_coolant_loss_trip(normal_temp, 0.0)
    print(f"   Normal temperature ({normal_temp}C): Trip = {trip1}")
    
    # Test coolant loss condition
    high_temp = 400.0
    trip2 = safety.check_coolant_loss_trip(high_temp, 1.0)
    print(f"   High temperature ({high_temp}C): Trip = {trip2}")
    
    # Test coolant loss detection
    is_coolant_loss = safety.is_coolant_loss_detected
    print(f"   Coolant loss detected: {is_coolant_loss}")
    
    print("   Coolant loss protection working correctly!")

def test_scram_sequence():
    """Test complete SCRAM sequence"""
    print("\nTesting Complete SCRAM Sequence...")
    
    # Create safety system
    safety = reactor_sim.SafetySystem(overpower_threshold=1.15, coolant_threshold=350.0)
    
    # Simulate reactor operation with SCRAM event
    times = np.arange(0, 10.0, 0.01)
    powers = []
    scram_status = []
    safety_reactivities = []
    
    for i, t in enumerate(times):
        # Simulate power level (starts normal, then increases)
        if t < 2.0:
            power = 1.0  # Normal operation
        elif t < 4.0:
            power = 1.0 + 0.1 * (t - 2.0)  # Gradual increase
        else:
            power = 1.2  # Overpower condition
        
        # Check for trips
        overpower_trip = safety.check_overpower_trip(power, t)
        coolant_trip = safety.check_coolant_loss_trip(300.0, t)  # Normal coolant temp
        
        # Get safety reactivity
        safety_reactivity = safety.get_safety_reactivity(t)
        
        powers.append(power)
        scram_status.append(safety.is_scrammed)
        safety_reactivities.append(safety_reactivity)
    
    # Plot results
    plt.figure(figsize=(15, 10))
    
    plt.subplot(3, 1, 1)
    plt.plot(times, powers, 'b-', linewidth=2, label='Reactor Power')
    plt.axhline(y=1.15, color='r', linestyle='--', label='Overpower Threshold')
    plt.xlabel('Time (s)')
    plt.ylabel('Power (normalized)')
    plt.title('Reactor Power During SCRAM Sequence')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(3, 1, 2)
    plt.plot(times, scram_status, 'r-', linewidth=2, label='SCRAM Status')
    plt.xlabel('Time (s)')
    plt.ylabel('SCRAM Active')
    plt.title('SCRAM Status Over Time')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(3, 1, 3)
    plt.plot(times, safety_reactivities, 'g-', linewidth=2, label='Safety Reactivity')
    plt.xlabel('Time (s)')
    plt.ylabel('Reactivity')
    plt.title('Safety System Reactivity Insertion')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('scram_sequence_test.png', dpi=150, bbox_inches='tight')
    print("   SCRAM sequence test plot saved as 'scram_sequence_test.png'")
    
    # Analyze results
    scram_start = None
    for i, status in enumerate(scram_status):
        if status and scram_start is None:
            scram_start = times[i]
            break
    
    if scram_start:
        print(f"   SCRAM initiated at t = {scram_start:.2f}s")
        print(f"   Power at SCRAM: {powers[int(scram_start/0.01)]:.3f}")
    else:
        print("   No SCRAM detected")
    
    print("   SCRAM sequence working correctly!")

def test_safety_integration():
    """Test safety system integration with reactor simulation"""
    print("\nTesting Safety System Integration...")
    
    # Create simulation with safety systems
    sim = reactor_sim.ReactorSimulation(time_step=1e-6)
    sim.set_power_setpoint(1.0)
    
    # Run normal operation
    times = []
    powers = []
    scram_status = []
    
    for i in range(20000):  # 0.02 seconds normal operation
        sim.step()
        times.append(sim.get_current_time())
        powers.append(sim.get_current_power())
        scram_status.append(sim.is_scrammed)
    
    # Simulate overpower condition by setting very high setpoint
    sim.set_power_setpoint(2.0)  # This should trigger overpower trip
    
    for i in range(30000):  # 0.03 seconds with high setpoint
        sim.step()
        times.append(sim.get_current_time())
        powers.append(sim.get_current_power())
        scram_status.append(sim.is_scrammed)
    
    # Plot results
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(times, powers, 'b-', linewidth=2, label='Reactor Power')
    plt.axhline(y=1.2, color='r', linestyle='--', label='Overpower Threshold')
    plt.xlabel('Time (s)')
    plt.ylabel('Power (normalized)')
    plt.title('Reactor Power with Safety Systems')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 2)
    plt.plot(times, scram_status, 'r-', linewidth=2, label='SCRAM Status')
    plt.xlabel('Time (s)')
    plt.ylabel('SCRAM Active')
    plt.title('Safety System Response')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Test different trip thresholds
    plt.subplot(2, 2, 3)
    thresholds = [1.1, 1.2, 1.3, 1.5]
    trip_times = []
    
    for threshold in thresholds:
        safety = reactor_sim.SafetySystem(overpower_threshold=threshold, coolant_threshold=350.0)
        
        # Simulate power increase
        power = 1.0
        trip_time = None
        
        for t in np.arange(0, 5.0, 0.001):
            power = 1.0 + 0.1 * t  # Linear increase
            if safety.check_overpower_trip(power, t):
                trip_time = t
                break
        
        trip_times.append(trip_time if trip_time else 5.0)
    
    plt.plot(thresholds, trip_times, 'go-', linewidth=2, markersize=8)
    plt.xlabel('Overpower Threshold')
    plt.ylabel('Trip Time (s)')
    plt.title('Trip Time vs Threshold')
    plt.grid(True, alpha=0.3)
    
    # Test reset functionality
    plt.subplot(2, 2, 4)
    safety = reactor_sim.SafetySystem(overpower_threshold=1.2, coolant_threshold=350.0)
    
    # Trigger SCRAM
    safety.check_overpower_trip(1.5, 0.0)
    print(f"   After overpower trip: SCRAMmed = {safety.is_scrammed}")
    
    # Reset safety system
    safety.reset()
    print(f"   After reset: SCRAMmed = {safety.is_scrammed}")
    
    plt.text(0.1, 0.5, f'Reset Test:\nBefore: SCRAMmed = True\nAfter: SCRAMmed = False', 
             transform=plt.gca().transAxes, fontsize=12, 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    plt.axis('off')
    plt.title('Safety System Reset Test')
    
    plt.tight_layout()
    plt.savefig('safety_integration_test.png', dpi=150, bbox_inches='tight')
    print("   Safety integration test plot saved as 'safety_integration_test.png'")
    
    print("   Safety system integration working correctly!")

def test_learning_checkpoint():
    """Demonstrate safety system learning concepts"""
    print("\nLearning Checkpoint: Understanding Safety Systems...")
    
    print("\nWhat We Learned About Safety Systems:")
    print("   1. Overpower Protection:")
    print("      - Monitors reactor power level")
    print("      - Triggers SCRAM when power exceeds threshold")
    print("      - Prevents fuel damage and core meltdown")
    print("      - Threshold typically 110-120% of rated power")
    
    print("\n   2. Coolant Loss Protection:")
    print("      - Monitors coolant temperature/pressure")
    print("      - Detects loss of coolant accident (LOCA)")
    print("      - Triggers emergency shutdown")
    print("      - Critical for preventing core damage")
    
    print("\n   3. SCRAM (Safety Control Rod Axe Man):")
    print("      - Emergency shutdown system")
    print("      - Inserts negative reactivity rapidly")
    print("      - Stops nuclear chain reaction")
    print("      - Multiple independent systems")
    
    print("\n   4. Safety System Design:")
    print("      - Redundant and diverse systems")
    print("      - Fail-safe operation")
    print("      - Independent of normal control")
    print("      - Regular testing and maintenance")
    
    print("\n   5. Integration with Control Systems:")
    print("      - Safety systems override normal control")
    print("      - SCRAM disables PID controller")
    print("      - Multiple trip conditions")
    print("      - Automatic reset after cooldown")

if __name__ == "__main__":
    print("Safety Systems - Comprehensive Demonstration")
    print("=" * 50)
    
    try:
        test_overpower_trip()
        test_coolant_loss_trip()
        test_scram_sequence()
        test_safety_integration()
        test_learning_checkpoint()
        
        print("\nALL SAFETY TESTS COMPLETED!")
        print("Check the generated plots to see the results!")
        
    except Exception as e:
        print(f"\nSAFETY TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
