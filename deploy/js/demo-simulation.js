// Demo Simulation for GitHub Pages
// Simulates reactor behavior without backend

class DemoSimulation {
    constructor() {
        this.isRunning = false;
        this.currentTime = 0.0;
        this.currentPower = 1.0;
        this.scramStatus = false;
        this.powerSetpoint = 1.0;
        this.scenario = 'normal';
        this.animationId = null;
        this.timeStep = 0.1; // 100ms steps for demo
        
        // Chart data
        this.chartData = {
            times: [],
            powers: [],
            scramStatus: [],
            setpoints: []
        };
        
        // Initialize charts
        this.initCharts();
        
        // Start with normal operation
        this.updateReactor3D(1.0, false);
    }
    
    initCharts() {
        // Power Chart
        const powerCtx = document.getElementById('powerChart').getContext('2d');
        this.powerChart = new Chart(powerCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Reactor Power',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.1,
                    fill: true
                }, {
                    label: 'Setpoint',
                    data: [],
                    borderColor: 'rgb(34, 197, 94)',
                    backgroundColor: 'transparent',
                    borderDash: [5, 5],
                    tension: 0
                }, {
                    label: 'Overpower Threshold',
                    data: [],
                    borderColor: 'rgb(239, 68, 68)',
                    backgroundColor: 'transparent',
                    borderDash: [2, 2],
                    tension: 0
                }]
            },
            options: {
                responsive: true,
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
                        ticks: {
                            min: 0.0,
                            max: 2.0
                        }
                    }
                },
                animation: {
                    duration: 0
                }
            }
        });
        
        // Safety Chart
        const safetyCtx = document.getElementById('safetyChart').getContext('2d');
        this.safetyChart = new Chart(safetyCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'SCRAM Status',
                    data: [],
                    borderColor: 'rgb(239, 68, 68)',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
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
                animation: {
                    duration: 0
                }
            }
        });
    }
    
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.updateSimulationStatus();
        this.animate();
    }
    
    stop() {
        this.isRunning = false;
        this.updateSimulationStatus();
    }
    
    reset() {
        this.stop();
        this.currentTime = 0.0;
        this.currentPower = 1.0;
        this.scramStatus = false;
        this.scenario = 'normal';
        
        // Clear chart data
        this.chartData = {
            times: [],
            powers: [],
            scramStatus: [],
            setpoints: []
        };
        
        this.updateCharts();
        this.updateReactor3D(1.0, false);
        this.updateDisplay();
    }
    
    runScenario(scenario) {
        this.scenario = scenario;
        
        switch (scenario) {
            case 'normal':
                this.powerSetpoint = 1.0;
                this.scramStatus = false;
                break;
            case 'ramp':
                this.powerSetpoint = 1.2;
                this.scramStatus = false;
                break;
            case 'scram':
                this.powerSetpoint = 1.0;
                this.scramStatus = true;
                break;
        }
        
        this.updateSetpointDisplay();
        this.updateReactor3D(this.currentPower, this.scramStatus);
    }
    
    animate() {
        if (!this.isRunning) return;
        
        // Update simulation
        this.step();
        
        // Update display
        this.updateDisplay();
        this.updateCharts();
        
        // Continue animation
        this.animationId = requestAnimationFrame(() => this.animate());
    }
    
    step() {
        // Advance time
        this.currentTime += this.timeStep;
        
        // Update power based on scenario
        switch (this.scenario) {
            case 'normal':
                this.currentPower = this.simulateNormalOperation();
                break;
            case 'ramp':
                this.currentPower = this.simulatePowerRamp();
                break;
            case 'scram':
                this.currentPower = this.simulateScram();
                break;
        }
        
        // Add some realistic noise
        this.currentPower += (Math.random() - 0.5) * 0.01;
        this.currentPower = Math.max(0.1, Math.min(2.0, this.currentPower));
        
        // Store data
        this.chartData.times.push(this.currentTime);
        this.chartData.powers.push(this.currentPower);
        this.chartData.scramStatus.push(this.scramStatus ? 1.0 : 0.0);
        this.chartData.setpoints.push(this.powerSetpoint);
        
        // Keep only last 100 points
        if (this.chartData.times.length > 100) {
            this.chartData.times = this.chartData.times.slice(-100);
            this.chartData.powers = this.chartData.powers.slice(-100);
            this.chartData.scramStatus = this.chartData.scramStatus.slice(-100);
            this.chartData.setpoints = this.chartData.setpoints.slice(-100);
        }
    }
    
    simulateNormalOperation() {
        // Oscillate around setpoint with small variations
        const target = this.powerSetpoint;
        const variation = 0.05 * Math.sin(this.currentTime * 2);
        return target + variation;
    }
    
    simulatePowerRamp() {
        // Gradually increase power towards setpoint
        const target = this.powerSetpoint;
        const current = this.currentPower;
        const rate = 0.02;
        return current + (target - current) * rate;
    }
    
    simulateScram() {
        // Rapidly decrease power during SCRAM
        const rate = 0.1;
        return this.currentPower * (1 - rate);
    }
    
    updateDisplay() {
        // Update time and power display
        document.getElementById('current-time').textContent = this.currentTime.toFixed(3);
        document.getElementById('current-power').textContent = this.currentPower.toFixed(3);
        
        // Update SCRAM status
        const scramElement = document.getElementById('scram-status');
        if (this.scramStatus) {
            scramElement.textContent = 'SCRAM ACTIVE';
            scramElement.className = 'badge bg-danger ms-2';
        } else {
            scramElement.textContent = 'NORMAL';
            scramElement.className = 'badge bg-success ms-2';
        }
        
        // Update simulation status
        const simElement = document.getElementById('sim-status');
        if (this.isRunning) {
            simElement.textContent = 'RUNNING';
            simElement.className = 'badge bg-success ms-2';
        } else {
            simElement.textContent = 'STOPPED';
            simElement.className = 'badge bg-secondary ms-2';
        }
    }
    
    updateCharts() {
        if (this.chartData.times.length === 0) return;
        
        // Update power chart
        this.powerChart.data.labels = this.chartData.times.map(t => t.toFixed(3));
        this.powerChart.data.datasets[0].data = this.chartData.powers;
        this.powerChart.data.datasets[1].data = this.chartData.setpoints;
        this.powerChart.data.datasets[2].data = new Array(this.chartData.times.length).fill(1.2);
        this.powerChart.update('none');
        
        // Update safety chart
        this.safetyChart.data.labels = this.chartData.times.map(t => t.toFixed(3));
        this.safetyChart.data.datasets[0].data = this.chartData.scramStatus;
        this.safetyChart.update('none');
    }
    
    updateReactor3D(power, scramStatus) {
        if (typeof updateReactor3D === 'function') {
            updateReactor3D(power, scramStatus);
        }
    }
    
    updateSimulationStatus() {
        // Update button states
        const startBtn = document.querySelector('button[onclick="startSimulation()"]');
        const stopBtn = document.querySelector('button[onclick="stopSimulation()"]');
        
        if (this.isRunning) {
            startBtn.disabled = true;
            stopBtn.disabled = false;
        } else {
            startBtn.disabled = false;
            stopBtn.disabled = true;
        }
    }
    
    updateSetpointDisplay() {
        document.getElementById('setpoint-value').textContent = this.powerSetpoint.toFixed(1);
    }
}

// Global simulation instance
let demoSim = null;

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    demoSim = new DemoSimulation();
    console.log('Demo simulation initialized');
});

// Control functions
function startSimulation() {
    if (demoSim) {
        demoSim.start();
    }
}

function stopSimulation() {
    if (demoSim) {
        demoSim.stop();
    }
}

function resetSimulation() {
    if (demoSim) {
        demoSim.reset();
    }
}

function runScenario(scenario) {
    if (demoSim) {
        demoSim.runScenario(scenario);
    }
}

function updateSetpoint(value) {
    if (demoSim) {
        demoSim.powerSetpoint = parseFloat(value);
        demoSim.updateSetpointDisplay();
    }
}
