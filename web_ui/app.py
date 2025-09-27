#!/usr/bin/env python3
"""
Nuclear Reactor Control Simulation - Web UI
Flask-based web interface for interactive reactor simulation.
"""

import sys
import os
import json
import threading
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

# Add the build directory to the path to import our C++ module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'build'))

try:
    import reactor_sim
except ImportError:
    print("Error: Could not import reactor_sim module.")
    print("Make sure you have built the C++ project and the Python bindings are available.")
    sys.exit(1)

# Add the python_ui directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python_ui'))

from enhanced_dashboard import EnhancedReactorDashboard

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nuclear_reactor_simulation_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global simulation state
simulation_state = {
    'dashboard': None,
    'is_running': False,
    'step_count': 0,
    'current_data': {
        'time': 0.0,
        'power': 1.0,
        'scram_status': False,
        'pid_output': 0.0
    },
    'history': {
        'times': [],
        'powers': [],
        'scram_status': [],
        'pid_outputs': []
    },
    'config': {
        'time_step': 1e-3,  # 1 millisecond - much more visible
        'power_setpoint': 1.0,
        'pid_gains': {'kp': 0.1, 'ki': 0.01, 'kd': 0.05},
        'safety_thresholds': {'overpower': 1.2, 'coolant': 350.0}
    }
}

def initialize_simulation():
    """Initialize the reactor simulation"""
    global simulation_state
    if simulation_state['dashboard'] is None:
        simulation_state['dashboard'] = EnhancedReactorDashboard()
        simulation_state['dashboard'].create_simulation()
    return simulation_state['dashboard']

def run_simulation_step():
    """Run a single simulation step"""
    global simulation_state
    if simulation_state['is_running'] and simulation_state['dashboard']:
        try:
            # Get state before step
            old_time = simulation_state['dashboard'].simulation.get_current_time()
            old_power = simulation_state['dashboard'].simulation.get_current_power()
            
            # Step the simulation
            simulation_state['dashboard'].simulation.step()
            
            # Get state after step
            new_time = simulation_state['dashboard'].simulation.get_current_time()
            new_power = simulation_state['dashboard'].simulation.get_current_power()
            
            # Debug output
            if simulation_state['step_count'] % 1000 == 0:  # Print every 1000 steps
                print(f"Step {simulation_state['step_count']}: Time {old_time:.6f} -> {new_time:.6f}, Power {old_power:.6f} -> {new_power:.6f}")
            
            simulation_state['step_count'] += 1
            
            # Update current state
            simulation_state['current_data'] = {
                'time': new_time,
                'power': new_power,
                'scram_status': simulation_state['dashboard'].simulation.is_scrammed,
                'pid_output': 0.0  # Placeholder for PID output
            }
            
            # Update history (keep last 1000 points)
            simulation_state['history']['times'].append(simulation_state['current_data']['time'])
            simulation_state['history']['powers'].append(simulation_state['current_data']['power'])
            simulation_state['history']['scram_status'].append(simulation_state['current_data']['scram_status'])
            simulation_state['history']['pid_outputs'].append(simulation_state['current_data']['pid_output'])
            
            # Keep history manageable
            if len(simulation_state['history']['times']) > 1000:
                simulation_state['history']['times'] = simulation_state['history']['times'][-1000:]
                simulation_state['history']['powers'] = simulation_state['history']['powers'][-1000:]
                simulation_state['history']['scram_status'] = simulation_state['history']['scram_status'][-1000:]
                simulation_state['history']['pid_outputs'] = simulation_state['history']['pid_outputs'][-1000:]
                
        except Exception as e:
            print(f"Simulation error: {e}")
            simulation_state['is_running'] = False

def simulation_loop():
    """Main simulation loop running in background thread"""
    while True:
        if simulation_state['is_running']:
            run_simulation_step()
            # Emit real-time data via WebSocket
            socketio.emit('simulation_update', {
                'current_data': simulation_state['current_data'],
                'history': simulation_state['history']
            })
            
            # Debug: Print every 1000 steps
            if simulation_state['step_count'] % 1000 == 0:
                print(f"WebSocket emit: Time={simulation_state['current_data']['time']:.6f}, Power={simulation_state['current_data']['power']:.6f}")
        time.sleep(0.1)  # 10 Hz update rate (much more reasonable)

# Start simulation thread
simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
simulation_thread.start()

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    emit('connection_status', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")

@socketio.on('request_status')
def handle_status_request():
    """Send current simulation status to client"""
    emit('status_update', {
        'is_running': simulation_state['is_running'],
        'current_data': simulation_state['current_data'],
        'config': simulation_state['config']
    })

@socketio.on('start_simulation')
def handle_start_simulation():
    """Start simulation via WebSocket"""
    global simulation_state
    initialize_simulation()
    simulation_state['is_running'] = True
    emit('simulation_started', {'status': 'started'})

@socketio.on('stop_simulation')
def handle_stop_simulation():
    """Stop simulation via WebSocket"""
    global simulation_state
    simulation_state['is_running'] = False
    emit('simulation_stopped', {'status': 'stopped'})

@socketio.on('reset_simulation')
def handle_reset_simulation():
    """Reset simulation via WebSocket"""
    global simulation_state
    simulation_state['is_running'] = False
    simulation_state['current_data'] = {
        'time': 0.0,
        'power': 1.0,
        'scram_status': False,
        'pid_output': 0.0
    }
    simulation_state['history'] = {
        'times': [],
        'powers': [],
        'scram_status': [],
        'pid_outputs': []
    }
    initialize_simulation()
    emit('simulation_reset', {'status': 'reset'})

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current simulation status"""
    initialize_simulation()
    return jsonify({
        'is_running': simulation_state['is_running'],
        'current_data': simulation_state['current_data'],
        'config': simulation_state['config']
    })

@app.route('/api/start', methods=['POST'])
def start_simulation():
    """Start the simulation"""
    global simulation_state
    initialize_simulation()
    simulation_state['is_running'] = True
    return jsonify({'status': 'started'})

@app.route('/api/stop', methods=['POST'])
def stop_simulation():
    """Stop the simulation"""
    global simulation_state
    simulation_state['is_running'] = False
    return jsonify({'status': 'stopped'})

@app.route('/api/reset', methods=['POST'])
def reset_simulation():
    """Reset the simulation"""
    global simulation_state
    simulation_state['is_running'] = False
    simulation_state['step_count'] = 0
    simulation_state['current_data'] = {
        'time': 0.0,
        'power': 1.0,
        'scram_status': False,
        'pid_output': 0.0
    }
    simulation_state['history'] = {
        'times': [],
        'powers': [],
        'scram_status': [],
        'pid_outputs': []
    }
    initialize_simulation()
    return jsonify({'status': 'reset'})

@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """Get or update simulation configuration"""
    global simulation_state
    
    if request.method == 'POST':
        new_config = request.json
        simulation_state['config'].update(new_config)
        
        # Apply configuration to simulation
        if simulation_state['dashboard']:
            simulation_state['dashboard'].simulation.set_power_setpoint(
                simulation_state['config']['power_setpoint']
            )
        
        return jsonify({'status': 'updated', 'config': simulation_state['config']})
    
    return jsonify(simulation_state['config'])

@app.route('/api/data')
def get_data():
    """Get simulation data for plotting"""
    return jsonify({
        'times': simulation_state['history']['times'],
        'powers': simulation_state['history']['powers'],
        'scram_status': simulation_state['history']['scram_status'],
        'pid_outputs': simulation_state['history']['pid_outputs']
    })

@app.route('/api/plot')
def generate_plot():
    """Generate a plot of current simulation data"""
    if not simulation_state['history']['times']:
        return jsonify({'error': 'No data available'})
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    times = simulation_state['history']['times']
    powers = simulation_state['history']['powers']
    scram_status = simulation_state['history']['scram_status']
    
    # Power plot
    ax1.plot(times, powers, 'b-', linewidth=2, label='Reactor Power')
    ax1.axhline(y=simulation_state['config']['power_setpoint'], 
                color='g', linestyle='--', label='Setpoint')
    ax1.axhline(y=simulation_state['config']['safety_thresholds']['overpower'], 
                color='r', linestyle=':', label='Overpower Threshold')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Power (normalized)')
    ax1.set_title('Reactor Power vs Time')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # SCRAM status plot
    scram_binary = [1 if s else 0 for s in scram_status]
    ax2.fill_between(times, 0, scram_binary, color='red', alpha=0.7, label='SCRAM Active')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('SCRAM Status')
    ax2.set_title('Safety System Status')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_ylim(-0.1, 1.1)
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return jsonify({'plot': f'data:image/png;base64,{img_base64}'})

@app.route('/api/scenarios/<scenario_name>', methods=['POST'])
def run_scenario(scenario_name):
    """Run a predefined scenario"""
    global simulation_state
    
    # Reset simulation first
    simulation_state['is_running'] = False
    simulation_state['history'] = {'times': [], 'powers': [], 'scram_status': [], 'pid_outputs': []}
    initialize_simulation()
    
    # Configure scenario
    if scenario_name == 'normal_operation':
        simulation_state['config']['power_setpoint'] = 1.0
        # Reset any SCRAM
        if simulation_state['dashboard']:
            simulation_state['dashboard'].simulation.reset_scram()
    elif scenario_name == 'power_ramp':
        simulation_state['config']['power_setpoint'] = 1.2
        # Reset any SCRAM
        if simulation_state['dashboard']:
            simulation_state['dashboard'].simulation.reset_scram()
    elif scenario_name == 'emergency_scram':
        simulation_state['config']['power_setpoint'] = 1.0  # Normal setpoint
        # Trigger emergency SCRAM
        if simulation_state['dashboard']:
            simulation_state['dashboard'].simulation.trigger_scram()
    else:
        return jsonify({'error': 'Unknown scenario'})
    
    # Apply configuration
    if simulation_state['dashboard']:
        simulation_state['dashboard'].simulation.set_power_setpoint(
            simulation_state['config']['power_setpoint']
        )
    
    # Start simulation
    simulation_state['is_running'] = True
    
    return jsonify({'status': f'Running scenario: {scenario_name}'})

if __name__ == '__main__':
    print("Starting Nuclear Reactor Control Simulation Web UI with WebSocket support...")
    print("Open your browser to: http://localhost:5001")
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
