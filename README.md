# Reactor Control Simulation

A nuclear reactor control simulation implementing point kinetics equations with PID control and safety interlocks.

## Project Overview

This project simulates nuclear reactor point kinetics with delayed neutron groups, implements a PID controller to manipulate reactivity and stabilize reactor power, and includes safety interlocks for overpower and coolant-loss trips with automatic SCRAM.

## Features

- **Zero-dimensional point kinetics** simulation (1-6 delayed neutron groups)
- **PID controller** with anti-windup and rate limits
- **Safety interlocks** for overpower and coolant loss SCRAM
- **Python dashboard** for visualization and analysis
- **Comprehensive testing** with GoogleTest and pytest
- **Requirements traceability matrix** for verification

## Prerequisites

### System Requirements
- **C++ Compiler**: g++ (GCC) 7.0+ or Clang 5.0+
- **CMake**: 3.16 or higher
- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows

### Installation Commands

#### macOS (using Homebrew)
```bash
# Install C++ compiler and build tools
brew install gcc cmake

# Install Python (if not already installed)
brew install python@3.9

# Install pybind11
pip3 install pybind11
```

#### Ubuntu/Debian
```bash
# Install C++ compiler and build tools
sudo apt update
sudo apt install build-essential cmake

# Install Python development headers
sudo apt install python3-dev python3-pip

# Install pybind11
pip3 install pybind11
```

## Quick Start

### 1. Clone and Setup
```bash
cd Reactor-Control-Simulation

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Build C++ Core
```bash
# Create build directory
mkdir build && cd build

# Configure with CMake
cmake ..

# Build the project
make -j4  # On Windows: cmake --build . --config Release
```

### 3. Run Tests
```bash
# Run C++ tests
ctest --verbose

# Run Python tests
cd ..
python -m pytest tests/
```

### 4. Run Dashboard
```bash
# Activate virtual environment
source venv/bin/activate

# Run the dashboard
python python_ui/dashboard.py
```

## Project Structure

```
Reactor-Control-Simulation/
├── cpp_core/              # C++ core library
│   ├── kinetics_solver.cpp
│   ├── pid_controller.cpp
│   ├── safety.cpp
│   └── sim_core.cpp
├── python_bindings/       # Python-C++ bindings
│   └── bindings.cpp
├── python_ui/            # Python dashboard
│   ├── dashboard.py
│   └── examples/
├── tests/                # Test files
│   ├── test_solver.cpp
│   ├── test_pid.cpp
│   ├── test_safety.cpp
│   └── test_bindings.py
├── docs/                 # Documentation
│   └── RTM.csv
├── notebooks/            # Jupyter notebooks
│   └── demo.ipynb
├── CMakeLists.txt        # CMake configuration
├── requirements.txt      # Python dependencies
└── README.md
```

## Mathematical Model

The simulation implements the point kinetics equations:

**Neutron density equation:**
```
dn/dt = (ρ(t) - β)/Λ * n(t) + Σ λᵢ * Cᵢ(t)
```

**Delayed neutron precursor equations:**
```
dCᵢ/dt = βᵢ/Λ * n(t) - λᵢ * Cᵢ(t)
```

Where:
- `n(t)` = neutron density (proportional to reactor power)
- `Cᵢ(t)` = delayed neutron precursor concentration for group i
- `ρ(t)` = reactivity (control input)
- `β, βᵢ` = delayed neutron fractions
- `Λ` = neutron generation time
- `λᵢ` = precursor decay constants

## Learning Resources

See the [Learning Materials section](reactorproject.md#learning-materials--study-resources) in the project specification for comprehensive study resources covering:

- Nuclear Reactor Physics & Point Kinetics
- Numerical Methods & ODE Integration
- Control Systems & PID Controllers
- C++ Advanced Programming
- Python-C++ Integration & Scientific Computing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Nuclear reactor theory based on Lamarsh & Baratta
- Control systems theory from Norman Nise
- Implementation inspired by modern scientific computing practices
