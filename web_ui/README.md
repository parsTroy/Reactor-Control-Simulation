# Nuclear Reactor Control Simulation - Web UI

A modern, interactive web interface for the Nuclear Reactor Control Simulation project. This web UI provides real-time visualization, control, and monitoring capabilities for nuclear reactor simulations.

## Features

### Real-time Monitoring
- **Live Power Display**: Real-time reactor power levels with visual indicators
- **Safety Status**: SCRAM status monitoring with visual alerts
- **Time Tracking**: Simulation time display and history
- **Interactive Charts**: Real-time plotting with Chart.js

### Control Interface
- **Simulation Controls**: Start, stop, and reset simulation
- **Power Setpoint**: Adjustable power setpoint with slider control
- **PID Configuration**: Real-time PID gain adjustment (Kp, Ki, Kd)
- **Scenario Testing**: Pre-built test scenarios for different conditions

### Data Management
- **Data Export**: Download simulation data as CSV
- **Plot Generation**: Generate high-quality plots for analysis
- **Configuration Management**: Save and load simulation parameters
- **Performance Monitoring**: Track simulation performance metrics

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Clean, professional interface with Bootstrap 5
- **Real-time Updates**: 10Hz update rate for smooth visualization
- **Fullscreen Support**: Toggle fullscreen mode for presentations

## Architecture

### Backend (Flask)
- **REST API**: RESTful endpoints for all simulation operations
- **Real-time Data**: Background thread for continuous simulation updates
- **C++ Integration**: Direct integration with C++ simulation core
- **Data Management**: Efficient data storage and retrieval

### Frontend (HTML/CSS/JavaScript)
- **Bootstrap 5**: Modern, responsive UI framework
- **Chart.js**: Interactive, real-time data visualization
- **Font Awesome**: Professional icons and indicators
- **Vanilla JavaScript**: No external dependencies, fast loading

### Data Flow
```
C++ Simulation Core → Flask Backend → REST API → JavaScript Frontend → Charts
```

## Installation

### Prerequisites
1. **C++ Build**: Ensure the C++ simulation core is built
2. **Python Dependencies**: Install required Python packages
3. **Web Browser**: Modern browser with JavaScript enabled

### Setup Steps

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Build C++ Module** (if not already done):
   ```bash
   mkdir build
   cd build
   cmake ..
   make
   ```

3. **Start Web Server**:
   ```bash
   python start_web_ui.py
   ```

4. **Open Browser**:
   Navigate to `http://localhost:5000`

## Usage

### Basic Operation

1. **Start Simulation**: Click "Start Simulation" to begin
2. **Monitor Power**: Watch real-time power levels in the chart
3. **Adjust Setpoint**: Use the power setpoint slider
4. **Configure PID**: Adjust Kp, Ki, Kd gains as needed
5. **Run Scenarios**: Test different operational scenarios

### Test Scenarios

- **Normal Operation**: Steady-state operation at 100% power
- **Power Ramp**: Gradual increase to 120% power
- **Emergency SCRAM**: Rapid power increase triggering safety systems

### Data Export

- **CSV Export**: Download time-series data for analysis
- **Plot Generation**: Create publication-quality plots
- **Configuration Save**: Save current settings for later use

## API Endpoints

### Simulation Control
- `GET /api/status` - Get current simulation status
- `POST /api/start` - Start simulation
- `POST /api/stop` - Stop simulation
- `POST /api/reset` - Reset simulation

### Configuration
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration

### Data Access
- `GET /api/data` - Get simulation data for plotting
- `GET /api/plot` - Generate plot image

### Scenarios
- `POST /api/scenarios/<name>` - Run predefined scenario

## Configuration

### PID Controller Settings
- **Kp (Proportional)**: Response to current error
- **Ki (Integral)**: Response to accumulated error
- **Kd (Derivative)**: Response to error rate

### Safety Thresholds
- **Overpower Threshold**: Maximum allowed power level
- **Coolant Threshold**: Maximum coolant temperature

### Simulation Parameters
- **Time Step**: Integration time step for numerical stability
- **Update Rate**: Web UI refresh rate (10 Hz)

## Performance

### Optimization Features
- **Efficient Data Management**: Circular buffer for history data
- **Background Processing**: Non-blocking simulation updates
- **Chart Optimization**: Minimal redraws for smooth performance
- **Memory Management**: Automatic cleanup of old data points

### System Requirements
- **CPU**: Modern multi-core processor recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)
- **Network**: Local network connection (localhost)

## Troubleshooting

### Common Issues

1. **"Could not import reactor_sim module"**
   - Ensure C++ project is built: `cd build && make`
   - Check Python path includes build directory

2. **"Missing dependency" errors**
   - Install requirements: `pip install -r requirements.txt`
   - Activate virtual environment if using one

3. **Charts not updating**
   - Check browser console for JavaScript errors
   - Ensure simulation is running
   - Refresh the page

4. **Slow performance**
   - Reduce update rate in JavaScript
   - Close other browser tabs
   - Check system resources

### Debug Mode

Enable debug mode by setting `debug=True` in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Development

### File Structure
```
web_ui/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Main HTML template
├── static/
│   ├── css/            # Custom styles
│   └── js/
│       └── app.js      # Frontend JavaScript
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Adding Features

1. **New API Endpoints**: Add routes in `app.py`
2. **UI Components**: Modify `templates/index.html`
3. **Interactive Features**: Update `static/js/app.js`
4. **Styling**: Add CSS in `static/css/`

### Testing

Test the web UI with different scenarios:
- Normal operation
- Power ramps
- Emergency conditions
- Configuration changes

## Security Considerations

- **Local Access Only**: Default configuration for localhost only
- **Input Validation**: All user inputs are validated
- **Error Handling**: Comprehensive error handling and logging
- **Resource Limits**: Automatic cleanup of old data

## Future Enhancements

### Planned Features
- **Multi-user Support**: Multiple simultaneous users
- **Advanced Analytics**: Statistical analysis tools
- **3D Visualization**: Three-dimensional reactor visualization
- **Mobile App**: Native mobile application
- **Cloud Deployment**: Cloud-based simulation hosting

### Integration Opportunities
- **SCADA Systems**: Integration with industrial control systems
- **Machine Learning**: AI-powered optimization
- **Virtual Reality**: VR-based training environment
- **IoT Sensors**: Real sensor data integration

## License

This project is part of the Nuclear Reactor Control Simulation suite.
See the main project README for licensing information.

## Support

For technical support or questions:
- Check the troubleshooting section above
- Review the main project documentation
- Open an issue in the project repository

---

**Nuclear Reactor Control Simulation - Web UI**  
Professional-grade simulation interface for nuclear engineering education and research.
