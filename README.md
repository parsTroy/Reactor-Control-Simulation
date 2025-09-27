# Nuclear Reactor Control Simulation

A comprehensive nuclear reactor control simulation system demonstrating advanced software engineering principles through C++ high-performance physics calculations and Python data visualization.

## Project Overview

This portfolio project showcases the integration of multiple technologies to create a realistic nuclear reactor control system. The implementation demonstrates expertise in C++ performance optimization, Python scientific computing, real-time web applications, and 3D visualization.

## Technical Architecture

### Core Technologies
- **C++17**: High-performance reactor physics engine
- **Python 3.8+**: Data analysis and visualization
- **Pybind11**: Seamless C++/Python integration
- **Three.js**: 3D WebGL visualization
- **Flask-SocketIO**: Real-time web communication
- **CMake**: Cross-platform build system

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   C++ Core      │    │  Python Layer   │    │  Web Interface  │
│                 │    │                 │    │                 │
│ • Point Kinetics│◄──►│ • Pybind11      │◄──►│ • 3D Visualization│
│ • PID Control   │    │ • Data Analysis │    │ • Real-time Charts│
│ • Safety Systems│    │ • Dashboard     │    │ • WebSocket API │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Key Features

### Nuclear Reactor Physics Implementation
- **Point Kinetics Equations**: Accurate neutron population modeling
- **Delayed Neutron Precursors**: Multi-group precursor tracking
- **Reactivity Control**: Real-time reactivity calculations
- **Safety Systems**: Overpower protection and emergency shutdown (SCRAM)

### Control Systems Engineering
- **PID Controller**: Proportional-Integral-Derivative control algorithm
- **Anti-windup Protection**: Prevents integral windup
- **Rate Limiting**: Smooth control rod movement
- **Setpoint Tracking**: Precise power level control

### Real-time Visualization
- **3D Reactor Model**: Interactive Three.js visualization
- **Dynamic Control Rods**: Real-time position updates
- **Power Indicators**: Color-coded power level display
- **Safety Status**: Visual SCRAM and trip indicators

## Project Structure

```
Reactor-Control-Simulation/
├── cpp_core/                    # C++ implementation
│   ├── kinetics_solver.h/cpp       # Point kinetics equations
│   ├── pid_controller.h/cpp        # PID control system
│   ├── safety.h/cpp                # Safety interlocks
│   └── sim_core.cpp                # Main simulation engine
├── python_bindings/             # Python-C++ interface
│   └── bindings.cpp                 # Pybind11 bindings
├── python_ui/                   # Python visualization
│   ├── dashboard.py                 # Main dashboard
│   └── enhanced_dashboard.py        # Advanced features
├── web_ui/                      # Web interface
│   ├── app.py                       # Flask-SocketIO server
│   ├── templates/index.html         # Web dashboard
│   └── static/js/                   # Frontend JavaScript
├── tests/                       # Unit tests
│   └── test_solver.cpp              # C++ tests
└── docs/                        # Documentation
    ├── RTM.csv                     # Requirements traceability
    └── system_diagram.py           # Architecture diagram
```

## Implementation Highlights

### C++ Performance Optimization
- **Memory Management**: Efficient state vector handling
- **Numerical Stability**: Time step validation and bounds checking
- **Template Programming**: Generic reactor parameter handling
- **Exception Safety**: Robust error handling and recovery

### Python Scientific Computing
- **NumPy Integration**: High-performance array operations
- **Matplotlib Visualization**: Real-time plotting and analysis
- **Pandas Data Handling**: CSV logging and data export
- **Pybind11 Bindings**: Zero-copy data transfer between C++ and Python

### Web Application Architecture
- **Flask-SocketIO**: Real-time bidirectional communication
- **Background Threading**: Non-blocking simulation execution
- **RESTful API**: Clean endpoint design for control operations
- **WebSocket Streaming**: 10Hz real-time data updates

### 3D Graphics Programming
- **Three.js WebGL**: Hardware-accelerated 3D rendering
- **Interactive Controls**: Mouse-based camera manipulation
- **Dynamic Materials**: Real-time color and property updates
- **Performance Optimization**: Efficient rendering pipeline

## Nuclear Reactor Physics

### Point Kinetics Implementation
The simulation implements the fundamental point kinetics equations:

```
dn/dt = (ρ - β)/Λ * n + Σ(λᵢ * Cᵢ) + S
dCᵢ/dt = βᵢ/Λ * n - λᵢ * Cᵢ
```

**Key Parameters:**
- `n` = neutron density (proportional to power)
- `Cᵢ` = delayed neutron precursor concentrations
- `ρ` = reactivity
- `β` = total delayed neutron fraction
- `Λ` = neutron generation time
- `λᵢ` = decay constants for precursor groups

### Safety System Design
- **Overpower Protection**: Configurable trip thresholds
- **Emergency Shutdown**: Rapid SCRAM implementation
- **Coolant Loss Detection**: Temperature-based monitoring
- **Trip Logic**: Multi-level safety interlocks

## Performance Characteristics

- **C++ Core**: ~1μs per simulation step
- **Python Integration**: <1ms overhead per call
- **WebSocket Updates**: 10Hz real-time streaming
- **3D Rendering**: 60 FPS smooth animation
- **Memory Usage**: <50MB total application footprint

## Build and Execution

### Prerequisites
- C++17 compatible compiler (g++, clang++, or MSVC)
- CMake 3.15+
- Python 3.8+
- pip package manager

### Build Process
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build C++ core
mkdir build && cd build
cmake ..
make
cd ..
```

### Execution Examples
```bash
# Basic C++ simulation test
python test_basic.py

# Python dashboard with data visualization
python test_enhanced_dashboard.py

# Full web interface with 3D visualization
python test_3d_websocket_ui.py
# Access at: http://localhost:5001
```

## Testing and Validation

### Unit Testing
- **C++ Tests**: GoogleTest framework for core algorithms
- **Python Tests**: pytest for integration testing
- **Performance Tests**: Benchmarking and profiling

### Integration Testing
- **End-to-End**: Complete system workflow validation
- **Real-time Performance**: WebSocket communication testing
- **3D Visualization**: Cross-browser compatibility testing

## Software Engineering Practices

### Code Organization
- **Modular Design**: Clear separation of concerns
- **Header Guards**: Proper C++ include management
- **Documentation**: Comprehensive inline documentation
- **Error Handling**: Robust exception management

### Version Control
- **Git Workflow**: Feature branch development
- **Commit History**: Clear, descriptive commit messages
- **Code Review**: Systematic review process

### Build System
- **CMake**: Cross-platform build configuration
- **Dependency Management**: Automated dependency resolution
- **Testing Integration**: Automated test execution

## Learning Outcomes

This project demonstrates proficiency in:

- **Advanced C++ Programming**: Templates, memory management, performance optimization
- **Python Scientific Computing**: NumPy, Matplotlib, data analysis
- **Web Development**: Flask, WebSocket, real-time applications
- **3D Graphics Programming**: Three.js, WebGL, interactive visualization
- **System Integration**: Multi-language, multi-platform development
- **Nuclear Engineering**: Reactor physics, control systems, safety engineering

## Technical Challenges Solved

1. **Real-time Performance**: Achieving 10Hz updates with complex physics calculations
2. **Cross-language Integration**: Seamless C++/Python data exchange
3. **3D Visualization**: Real-time 3D updates with WebSocket data
4. **Numerical Stability**: Preventing simulation divergence with proper time stepping
5. **WebSocket Communication**: Reliable real-time data streaming
6. **Memory Management**: Efficient state vector handling in C++

## Future Enhancements

- **Advanced Physics**: Multi-dimensional neutron transport
- **Machine Learning**: AI-powered control optimization
- **Distributed Computing**: Multi-core simulation acceleration
- **Mobile Support**: Responsive design improvements
- **Data Analytics**: Advanced statistical analysis tools