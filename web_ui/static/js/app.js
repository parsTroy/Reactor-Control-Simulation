// Nuclear Reactor Control Simulation - Web UI JavaScript

// Global variables
let powerChart, safetyChart;
let updateInterval;
let isSimulationRunning = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    startStatusUpdates();
    loadConfiguration();
});

// Initialize Chart.js charts
function initializeCharts() {
    // Power Chart
    const powerCtx = document.getElementById('powerChart').getContext('2d');
    powerChart = new Chart(powerCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Reactor Power',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.1
            }, {
                label: 'Setpoint',
                data: [],
                borderColor: 'rgb(34, 197, 94)',
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false
            }, {
                label: 'Overpower Threshold',
                data: [],
                borderColor: 'rgb(239, 68, 68)',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                borderWidth: 1,
                borderDash: [2, 2],
                fill: false
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time (s)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Power (normalized)'
                    },
                    min: 0.0,
                    max: 2.0,
                    beginAtZero: true,
                    ticks: {
                        min: 0.0,
                        max: 2.0
                    },
                    grid: {
                        display: true
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            animation: {
                duration: 0
            }
        }
    });

    // Safety Chart
    const safetyCtx = document.getElementById('safetyChart').getContext('2d');
    safetyChart = new Chart(safetyCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'SCRAM Status',
                data: [],
                borderColor: 'rgb(239, 68, 68)',
                backgroundColor: 'rgba(239, 68, 68, 0.3)',
                borderWidth: 2,
                fill: true
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time (s)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'SCRAM Active'
                    },
                    min: -0.1,
                    max: 1.1,
                    ticks: {
                        min: -0.1,
                        max: 1.1
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            animation: {
                duration: 0
            }
        }
    });
}

// Start periodic status updates
function startStatusUpdates() {
    updateInterval = setInterval(updateStatus, 1000); // 1 Hz updates (once per second)
}

// Update system status
async function updateStatus() {
    // Only update if the page is visible
    if (document.hidden) {
        return;
    }
    
    // If simulation is not running, update less frequently
    if (!isSimulationRunning) {
        // Only update every 5 seconds when not running
        if (Math.random() > 0.2) {
            return;
        }
    }
    
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        // Update current values
        document.getElementById('current-power').textContent = data.current_data.power.toFixed(3);
        document.getElementById('current-time').textContent = data.current_data.time.toFixed(3);
        
        // Update SCRAM status
        const scramElement = document.getElementById('scram-status');
        if (data.current_data.scram_status) {
            scramElement.textContent = 'SCRAM ACTIVE';
            scramElement.className = 'badge bg-danger';
        } else {
            scramElement.textContent = 'NORMAL';
            scramElement.className = 'badge bg-success';
        }
        
        // Update simulation status
        const simElement = document.getElementById('sim-status');
        if (data.is_running) {
            simElement.textContent = 'RUNNING';
            simElement.className = 'badge bg-success';
        } else {
            simElement.textContent = 'STOPPED';
            simElement.className = 'badge bg-secondary';
        }
        
        // Update status indicator
        const statusIndicator = document.getElementById('status-indicator');
        const statusText = document.getElementById('status-text');
        
        if (data.current_data.scram_status) {
            statusIndicator.className = 'status-indicator status-scram';
            statusText.textContent = 'SCRAM ACTIVE';
        } else if (data.is_running) {
            statusIndicator.className = 'status-indicator status-normal';
            statusText.textContent = 'Simulation Running';
        } else {
            statusIndicator.className = 'status-indicator status-warning';
            statusText.textContent = 'System Ready';
        }
        
        // Update charts
        updateCharts();
        
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

// Update charts with new data
async function updateCharts() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        
        if (data.times && data.times.length > 0 && data.powers && data.powers.length > 0) {
            // Validate and clamp power data to reasonable bounds
            const validPowers = data.powers.map(power => {
                if (isNaN(power) || !isFinite(power)) {
                    return 1.0; // Default to 1.0 for invalid values
                }
                // Clamp between 0 and 2.0 to match chart bounds
                const clamped = Math.max(0, Math.min(power, 2.0));
                return clamped;
            });
            
            // Update power chart
            powerChart.data.labels = data.times.map(t => t.toFixed(3));
            powerChart.data.datasets[0].data = validPowers;
            
            // Update setpoint line
            const setpoint = parseFloat(document.getElementById('power-setpoint').value);
            powerChart.data.datasets[1].data = new Array(data.times.length).fill(setpoint);
            
            // Update overpower threshold line
            powerChart.data.datasets[2].data = new Array(data.times.length).fill(1.2);
            
            // Update chart with animation disabled for performance
            // Only update if we have valid data
            if (validPowers.length > 0) {
                powerChart.update('none');
            }
            
            // Update safety chart
            safetyChart.data.labels = data.times.map(t => t.toFixed(3));
            safetyChart.data.datasets[0].data = data.scram_status.map(s => s ? 1 : 0);
            safetyChart.update('none');
            
            // Update data points counter
            document.getElementById('data-points').textContent = data.times.length;
            
            // Y-axis is already fixed in chart initialization - no changes needed
        }
    } catch (error) {
        console.error('Error updating charts:', error);
    }
}

// Start simulation
async function startSimulation() {
    try {
        const response = await fetch('/api/start', { method: 'POST' });
        const data = await response.json();
        
        if (data.status === 'started') {
            isSimulationRunning = true;
            document.getElementById('start-btn').disabled = true;
            document.getElementById('stop-btn').disabled = false;
        }
    } catch (error) {
        console.error('Error starting simulation:', error);
        alert('Error starting simulation: ' + error.message);
    }
}

// Stop simulation
async function stopSimulation() {
    try {
        const response = await fetch('/api/stop', { method: 'POST' });
        const data = await response.json();
        
        if (data.status === 'stopped') {
            isSimulationRunning = false;
            document.getElementById('start-btn').disabled = false;
            document.getElementById('stop-btn').disabled = true;
        }
    } catch (error) {
        console.error('Error stopping simulation:', error);
        alert('Error stopping simulation: ' + error.message);
    }
}

// Reset simulation
async function resetSimulation() {
    try {
        const response = await fetch('/api/reset', { method: 'POST' });
        const data = await response.json();
        
        if (data.status === 'reset') {
            isSimulationRunning = false;
            document.getElementById('start-btn').disabled = false;
            document.getElementById('stop-btn').disabled = true;
            
            // Clear charts
            powerChart.data.labels = [];
            powerChart.data.datasets.forEach(dataset => dataset.data = []);
            powerChart.update();
            
            safetyChart.data.labels = [];
            safetyChart.data.datasets.forEach(dataset => dataset.data = []);
            safetyChart.update();
            
            document.getElementById('data-points').textContent = '0';
        }
    } catch (error) {
        console.error('Error resetting simulation:', error);
        alert('Error resetting simulation: ' + error.message);
    }
}

// Update power setpoint
async function updateSetpoint(value) {
    document.getElementById('setpoint-value').textContent = parseFloat(value).toFixed(2);
    
    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                power_setpoint: parseFloat(value)
            })
        });
    } catch (error) {
        console.error('Error updating setpoint:', error);
    }
}

// Update PID gains
async function updatePIDGains() {
    const kp = parseFloat(document.getElementById('kp-gain').value);
    const ki = parseFloat(document.getElementById('ki-gain').value);
    const kd = parseFloat(document.getElementById('kd-gain').value);
    
    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                pid_gains: { kp: kp, ki: ki, kd: kd }
            })
        });
    } catch (error) {
        console.error('Error updating PID gains:', error);
    }
}

// Run scenario
async function runScenario(scenarioName) {
    try {
        const response = await fetch(`/api/scenarios/${scenarioName}`, { method: 'POST' });
        const data = await response.json();
        
        if (data.status) {
            isSimulationRunning = true;
            document.getElementById('start-btn').disabled = true;
            document.getElementById('stop-btn').disabled = false;
            
            // Update setpoint slider based on scenario
            if (scenarioName === 'normal_operation') {
                document.getElementById('power-setpoint').value = 1.0;
            } else if (scenarioName === 'power_ramp') {
                document.getElementById('power-setpoint').value = 1.2;
            } else if (scenarioName === 'emergency_scram') {
                document.getElementById('power-setpoint').value = 1.5;
            }
            updateSetpoint(document.getElementById('power-setpoint').value);
        }
    } catch (error) {
        console.error('Error running scenario:', error);
        alert('Error running scenario: ' + error.message);
    }
}

// Load configuration
async function loadConfiguration() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();
        
        // Update UI elements with current configuration
        document.getElementById('power-setpoint').value = config.power_setpoint;
        document.getElementById('setpoint-value').textContent = config.power_setpoint.toFixed(2);
        
        document.getElementById('kp-gain').value = config.pid_gains.kp;
        document.getElementById('ki-gain').value = config.pid_gains.ki;
        document.getElementById('kd-gain').value = config.pid_gains.kd;
        
        document.getElementById('overpower-threshold').textContent = config.safety_thresholds.overpower;
        document.getElementById('coolant-threshold').textContent = config.safety_thresholds.coolant;
        
    } catch (error) {
        console.error('Error loading configuration:', error);
    }
}

// Export data
function exportData() {
    // Create CSV content
    const csvContent = "Time,Power,SCRAM_Status\n" + 
        powerChart.data.labels.map((time, index) => 
            `${time},${powerChart.data.datasets[0].data[index]},${safetyChart.data.datasets[0].data[index]}`
        ).join('\n');
    
    // Download CSV
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `reactor_simulation_${new Date().toISOString().slice(0,19)}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Generate plot
async function generatePlot() {
    try {
        const response = await fetch('/api/plot');
        const data = await response.json();
        
        if (data.plot) {
            document.getElementById('plot-image').src = data.plot;
            const modal = new bootstrap.Modal(document.getElementById('plotModal'));
            modal.show();
        } else if (data.error) {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error generating plot:', error);
        alert('Error generating plot: ' + error.message);
    }
}

// Toggle fullscreen
function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

// Handle window resize
window.addEventListener('resize', function() {
    if (powerChart) powerChart.resize();
    if (safetyChart) safetyChart.resize();
});
