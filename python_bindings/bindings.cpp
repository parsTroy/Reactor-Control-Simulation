#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "kinetics_solver.h"
#include "pid_controller.h"
#include "safety.h"
#include "sim_core.cpp"  // Include the simulation core

namespace py = pybind11;

/**
 * @brief Python bindings for Reactor Control Simulation
 * 
 * This module exposes the C++ functionality to Python, allowing us to:
 * - Run reactor simulations from Python
 * - Access all control and safety parameters
 * - Visualize results with matplotlib
 */

PYBIND11_MODULE(reactor_sim, m) {
    m.doc() = "Nuclear Reactor Control Simulation - Python Bindings";
    
    // ============================================================================
    // ReactorParams class
    // ============================================================================
    py::class_<ReactorParams>(m, "ReactorParams")
        .def(py::init<>())
        .def_readwrite("Lambda", &ReactorParams::Lambda)
        .def_readwrite("beta", &ReactorParams::beta)
        .def_readwrite("beta_i", &ReactorParams::beta_i)
        .def_readwrite("lambda_i", &ReactorParams::lambda_i)
        .def("__repr__", [](const ReactorParams& p) {
            return "ReactorParams(Lambda=" + std::to_string(p.Lambda) + 
                   ", beta=" + std::to_string(p.beta) + ")";
        });
    
    // ============================================================================
    // Kinetics solver functions
    // ============================================================================
    m.def("step_point_kinetics", &step_point_kinetics,
          "Single step of point kinetics integration",
          py::arg("t"), py::arg("dt"), py::arg("y"), 
          py::arg("params"), py::arg("rho"));
    
    m.def("initialize_reactor_state", &initialize_reactor_state,
          "Initialize reactor state vector",
          py::arg("params"), py::arg("initial_power") = 1.0);
    
    // ============================================================================
    // PID Controller class
    // ============================================================================
    py::class_<PIDController>(m, "PIDController")
        .def(py::init<double, double, double, double, double>(),
             py::arg("kp") = 0.1, py::arg("ki") = 0.01, py::arg("kd") = 0.05,
             py::arg("setpoint") = 1.0, py::arg("dt") = 0.01)
        .def("calculate", &PIDController::calculate,
             "Calculate controller output",
             py::arg("current_power"))
        .def("set_setpoint", &PIDController::setSetpoint,
             "Set new setpoint",
             py::arg("new_setpoint"))
        .def("reset", &PIDController::reset,
             "Reset controller state")
        .def("set_gains", &PIDController::setGains,
             "Set PID gains",
             py::arg("kp"), py::arg("ki"), py::arg("kd"))
        .def("set_output_limits", &PIDController::setOutputLimits,
             "Set output limits",
             py::arg("min_output"), py::arg("max_output"))
        .def("set_rate_limits", &PIDController::setRateLimits,
             "Set rate limits",
             py::arg("min_rate"), py::arg("max_rate"))
        .def_property_readonly("setpoint", &PIDController::getSetpoint)
        .def_property_readonly("integral_sum", &PIDController::getIntegralSum)
        .def_property_readonly("last_output", &PIDController::getLastOutput)
        .def_property_readonly("kp_", &PIDController::getKp)
        .def_property_readonly("ki_", &PIDController::getKi)
        .def_property_readonly("kd_", &PIDController::getKd);
    
    // ============================================================================
    // Safety System class
    // ============================================================================
    py::class_<SafetySystem>(m, "SafetySystem")
        .def(py::init<double, double, double>(),
             py::arg("overpower_threshold") = 1.2,
             py::arg("coolant_threshold") = 350.0,
             py::arg("scram_reactivity") = -0.1)
        .def("check_overpower_trip", &SafetySystem::checkOverpowerTrip,
             "Check for overpower condition",
             py::arg("current_power"), py::arg("current_time"))
        .def("check_coolant_loss_trip", &SafetySystem::checkCoolantLossTrip,
             "Check for coolant loss condition",
             py::arg("coolant_temperature"), py::arg("current_time"))
        .def("get_safety_reactivity", &SafetySystem::getSafetyReactivity,
             "Get current safety reactivity",
             py::arg("current_time"))
        .def("reset", &SafetySystem::reset,
             "Reset safety system")
        .def("set_trip_thresholds", &SafetySystem::setTripThresholds,
             "Set trip thresholds",
             py::arg("overpower_threshold"), py::arg("coolant_threshold"))
        .def_property_readonly("is_scrammed", &SafetySystem::isScrammed)
        .def_property_readonly("is_coolant_loss_detected", &SafetySystem::isCoolantLossDetected)
        .def_property_readonly("overpower_threshold_", &SafetySystem::getOverpowerThreshold)
        .def_property_readonly("coolant_loss_threshold_", &SafetySystem::getCoolantLossThreshold);
    
    // ============================================================================
    // Main Simulation class
    // ============================================================================
    py::class_<ReactorSimulation>(m, "ReactorSimulation")
        .def(py::init<double>(), py::arg("time_step") = 0.001)
        .def("step", &ReactorSimulation::step,
             "Run one simulation step")
        .def("get_current_power", &ReactorSimulation::getCurrentPower,
             "Get current power level")
        .def("get_current_time", &ReactorSimulation::getCurrentTime,
             "Get current simulation time")
        .def("set_power_setpoint", &ReactorSimulation::setPowerSetpoint,
             "Set power setpoint",
             py::arg("setpoint"))
        .def("set_pid_enabled", &ReactorSimulation::setPIDEnabled,
             "Enable/disable PID control",
             py::arg("enabled"))
        .def_property_readonly("is_scrammed", &ReactorSimulation::isScrammed)
        .def_property_readonly("reactor_params", &ReactorSimulation::getReactorParams);
}
