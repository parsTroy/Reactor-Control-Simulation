// Demo Simulation for GitHub Pages
// Simulates reactor behavior without backend - using simple SVG charts

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
        
        // Chart data - limited to prevent memory issues
        this.maxDataPoints = 50;
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
        // Initialize SVG charts
        this.initPowerChart();
        this.initSafetyChart();
    }
    
    initPowerChart() {
        const svg = document.getElementById('powerSvg');
        if (!svg) return;
        
        // Clear any existing content
        svg.innerHTML = '';
        
        // Add grid lines and labels
        this.drawPowerChartGrid(svg);
    }
    
    initSafetyChart() {
        const svg = document.getElementById('safetySvg');
        if (!svg) return;
        
        // Clear any existing content
        svg.innerHTML = '';
        
        // Add grid lines and labels
        this.drawSafetyChartGrid(svg);
    }
    
    drawPowerChartGrid(svg) {
        const width = svg.clientWidth || 400;
        const height = svg.clientHeight || 200;
        const padding = 40;
        const chartWidth = width - 2 * padding;
        const chartHeight = height - 2 * padding;
        
        // Background
        svg.innerHTML = `
            <rect x="0" y="0" width="${width}" height="${height}" fill="#f9f9f9" stroke="#ddd"/>
            
            <!-- Grid lines -->
            <g stroke="#e0e0e0" stroke-width="1">
                ${Array.from({length: 6}, (_, i) => {
                    const y = padding + (i * chartHeight / 5);
                    return `<line x1="${padding}" y1="${y}" x2="${width - padding}" y2="${y}"/>`;
                }).join('')}
                ${Array.from({length: 11}, (_, i) => {
                    const x = padding + (i * chartWidth / 10);
                    return `<line x1="${x}" y1="${padding}" x2="${x}" y2="${height - padding}"/>`;
                }).join('')}
            </g>
            
            <!-- Y-axis labels -->
            <g fill="#666" font-family="Arial" font-size="12" text-anchor="end">
                ${Array.from({length: 6}, (_, i) => {
                    const y = padding + (i * chartHeight / 5);
                    const value = (2.0 - i * 0.4).toFixed(1);
                    return `<text x="${padding - 5}" y="${y + 4}">${value}</text>`;
                }).join('')}
            </g>
            
            <!-- X-axis label -->
            <text x="${width/2}" y="${height - 5}" fill="#666" font-family="Arial" font-size="12" text-anchor="middle">Time (s)</text>
            
            <!-- Y-axis label -->
            <text x="15" y="${height/2}" fill="#666" font-family="Arial" font-size="12" text-anchor="middle" transform="rotate(-90, 15, ${height/2})">Power</text>
            
            <!-- Reference lines -->
            <line x1="${padding}" y1="${padding + chartHeight * 0.4}" x2="${width - padding}" y2="${padding + chartHeight * 0.4}" stroke="#22c55e" stroke-width="2" stroke-dasharray="5,5" opacity="0.7"/>
            <line x1="${padding}" y1="${padding + chartHeight * 0.2}" x2="${width - padding}" y2="${padding + chartHeight * 0.2}" stroke="#ef4444" stroke-width="2" stroke-dasharray="2,2" opacity="0.7"/>
            
            <!-- Legend -->
            <g font-family="Arial" font-size="10">
                <line x1="${width - 120}" y1="${padding + 10}" x2="${width - 100}" y2="${padding + 10}" stroke="#3b82f6" stroke-width="2"/>
                <text x="${width - 95}" y="${padding + 14}" fill="#333">Power</text>
                <line x1="${width - 120}" y1="${padding + 25}" x2="${width - 100}" y2="${padding + 25}" stroke="#22c55e" stroke-width="2" stroke-dasharray="5,5"/>
                <text x="${width - 95}" y="${padding + 29}" fill="#333">Setpoint</text>
                <line x1="${width - 120}" y1="${padding + 40}" x2="${width - 100}" y2="${padding + 40}" stroke="#ef4444" stroke-width="2" stroke-dasharray="2,2"/>
                <text x="${width - 95}" y="${padding + 44}" fill="#333">Threshold</text>
            </g>
        `;
    }
    
    drawSafetyChartGrid(svg) {
        const width = svg.clientWidth || 400;
        const height = svg.clientHeight || 150;
        const padding = 40;
        const chartWidth = width - 2 * padding;
        const chartHeight = height - 2 * padding;
        
        // Background
        svg.innerHTML = `
            <rect x="0" y="0" width="${width}" height="${height}" fill="#f9f9f9" stroke="#ddd"/>
            
            <!-- Grid lines -->
            <g stroke="#e0e0e0" stroke-width="1">
                ${Array.from({length: 6}, (_, i) => {
                    const y = padding + (i * chartHeight / 5);
                    return `<line x1="${padding}" y1="${y}" x2="${width - padding}" y2="${y}"/>`;
                }).join('')}
                ${Array.from({length: 11}, (_, i) => {
                    const x = padding + (i * chartWidth / 10);
                    return `<line x1="${x}" y1="${padding}" x2="${x}" y2="${height - padding}"/>`;
                }).join('')}
            </g>
            
            <!-- Y-axis labels -->
            <g fill="#666" font-family="Arial" font-size="12" text-anchor="end">
                <text x="${padding - 5}" y="${height - padding + 4}">NO</text>
                <text x="${padding - 5}" y="${padding + 4}">YES</text>
            </g>
            
            <!-- X-axis label -->
            <text x="${width/2}" y="${height - 5}" fill="#666" font-family="Arial" font-size="12" text-anchor="middle">Time (s)</text>
            
            <!-- Y-axis label -->
            <text x="15" y="${height/2}" fill="#666" font-family="Arial" font-size="12" text-anchor="middle" transform="rotate(-90, 15, ${height/2})">SCRAM</text>
        `;
    }
    
    updatePowerChart() {
        const svg = document.getElementById('powerSvg');
        if (!svg || this.chartData.times.length === 0) return;
        
        const width = svg.clientWidth || 400;
        const height = svg.clientHeight || 200;
        const padding = 40;
        const chartWidth = width - 2 * padding;
        const chartHeight = height - 2 * padding;
        
        // Convert data to SVG coordinates
        const points = this.chartData.powers.map((power, i) => {
            const x = padding + (i / (this.chartData.powers.length - 1)) * chartWidth;
            const y = padding + chartHeight - (power / 2.0) * chartHeight;
            return `${x},${y}`;
        }).join(' ');
        
        const setpointPoints = this.chartData.setpoints.map((setpoint, i) => {
            const x = padding + (i / (this.chartData.setpoints.length - 1)) * chartWidth;
            const y = padding + chartHeight - (setpoint / 2.0) * chartHeight;
            return `${x},${y}`;
        }).join(' ');
        
        // Update the chart with new data
        this.drawPowerChartGrid(svg);
        
        // Add data lines
        if (points) {
            svg.innerHTML += `
                <polyline points="${points}" fill="none" stroke="#3b82f6" stroke-width="2"/>
                <polyline points="${setpointPoints}" fill="none" stroke="#22c55e" stroke-width="2" stroke-dasharray="5,5"/>
            `;
        }
    }
    
    updateSafetyChart() {
        const svg = document.getElementById('safetySvg');
        if (!svg || this.chartData.times.length === 0) return;
        
        const width = svg.clientWidth || 400;
        const height = svg.clientHeight || 150;
        const padding = 40;
        const chartWidth = width - 2 * padding;
        const chartHeight = height - 2 * padding;
        
        // Convert SCRAM data to SVG coordinates
        const points = this.chartData.scramStatus.map((scram, i) => {
            const x = padding + (i / (this.chartData.scramStatus.length - 1)) * chartWidth;
            const y = padding + chartHeight - (scram * chartHeight);
            return `${x},${y}`;
        }).join(' ');
        
        // Update the chart with new data
        this.drawSafetyChartGrid(svg);
        
        // Add data line
        if (points) {
            svg.innerHTML += `
                <polyline points="${points}" fill="none" stroke="#ef4444" stroke-width="3"/>
            `;
        }
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
        // Strictly clamp power values
        this.currentPower = Math.max(0.0, Math.min(2.0, this.currentPower));
        
        // Store data
        this.chartData.times.push(this.currentTime);
        this.chartData.powers.push(this.currentPower);
        this.chartData.scramStatus.push(this.scramStatus ? 1.0 : 0.0);
        this.chartData.setpoints.push(this.powerSetpoint);
        
        // Keep only last N points to prevent memory issues
        if (this.chartData.times.length > this.maxDataPoints) {
            this.chartData.times = this.chartData.times.slice(-this.maxDataPoints);
            this.chartData.powers = this.chartData.powers.slice(-this.maxDataPoints);
            this.chartData.scramStatus = this.chartData.scramStatus.slice(-this.maxDataPoints);
            this.chartData.setpoints = this.chartData.setpoints.slice(-this.maxDataPoints);
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
        this.updatePowerChart();
        this.updateSafetyChart();
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
    console.log('Demo simulation initialized with SVG charts');
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
