# Reactor Control Simulation - Main CMake Configuration
# This file tells CMake how to build our C++ project

# Set minimum CMake version (required for modern C++ features)
cmake_minimum_required(VERSION 3.16)

# Set project name and version
project(ReactorControlSim 
    VERSION 1.0.0
    DESCRIPTION "Nuclear Reactor Control Simulation"
    LANGUAGES CXX
)

# Set C++ standard (C++17 for modern features like std::optional, structured bindings)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set build type to Release for better performance (Debug for development)
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler-specific options
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    # Enable all warnings and treat them as errors
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic -Werror")
    # Optimize for performance
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -DNDEBUG")
    # Debug information for development
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -O0")
endif()

# Find required packages
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Find pybind11 - try to find it in the virtual environment first
set(pybind11_DIR "${CMAKE_CURRENT_SOURCE_DIR}/venv/lib/python3.13/site-packages/pybind11/share/cmake/pybind11")
find_package(pybind11 REQUIRED)

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/cpp_core)

# Create the main C++ library
add_library(reactor_core
    cpp_core/kinetics_solver.cpp
    cpp_core/pid_controller.cpp
    cpp_core/safety.cpp
    cpp_core/sim_core.cpp
)

# Link libraries
target_link_libraries(reactor_core)

# Create Python bindings
pybind11_add_module(reactor_sim
    python_bindings/bindings.cpp
)

# Link the C++ core to Python bindings
target_link_libraries(reactor_sim PRIVATE reactor_core)

# Enable testing (simplified for now)
enable_testing()

# Note: GoogleTest will be added later when we implement the full test suite

# Installation rules
install(TARGETS reactor_core reactor_sim
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
)
