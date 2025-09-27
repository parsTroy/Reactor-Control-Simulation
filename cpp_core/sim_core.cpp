#include "kinetics_solver.h"
#include "pid_controller.h"
#include "safety.h"
#include <vector>

/**
 * @brief Main simulation core that integrates all components
 * 
 * This class coordinates the kinetics solver, PID controller, and safety system
 * to run a complete reactor simulation.
 */
class ReactorSimulation {
private:
    ReactorParams params_;
    PIDController pid_controller_;
    SafetySystem safety_system_;
    
    // Simulation state
    std::vector<double> state_;
    double current_time_;
    double time_step_;
    
    // Control parameters
    double power_setpoint_;
    bool pid_enabled_;
    
public:
    /**
     * @brief Constructor
     */
    ReactorSimulation(double time_step = 1e-6)  // Much smaller default time step for stability
        : params_(),
          pid_controller_(0.1, 0.01, 0.05, 1.0, time_step),
          safety_system_(),
          current_time_(0.0),
          time_step_(time_step),
          power_setpoint_(1.0),
          pid_enabled_(true)
    {
        // Initialize reactor at steady state
        state_ = initialize_reactor_state(params_, 1.0);
    }
    
    /**
     * @brief Run one simulation step
     */
    void step() {
        // Get current power level (neutron density)
        double current_power = state_[0];
        
        // Check safety systems
        safety_system_.checkOverpowerTrip(current_power, current_time_);
        
        // Calculate control reactivity
        double control_reactivity = 0.0;
        if (pid_enabled_ && !safety_system_.isScrammed()) {
            control_reactivity = pid_controller_.calculate(current_power);
        }
        
        // Get safety reactivity
        double safety_reactivity = safety_system_.getSafetyReactivity(current_time_);
        
        // Total reactivity
        double total_reactivity = control_reactivity + safety_reactivity;
        
        // Update reactor state
        state_ = step_point_kinetics(current_time_, time_step_, state_, params_, total_reactivity);
        
        // Update time
        current_time_ += time_step_;
    }
    
    /**
     * @brief Get current power level
     */
    double getCurrentPower() const {
        return state_[0];
    }
    
    /**
     * @brief Get current time
     */
    double getCurrentTime() const {
        return current_time_;
    }
    
    /**
     * @brief Set power setpoint
     */
    void setPowerSetpoint(double setpoint) {
        power_setpoint_ = setpoint;
        pid_controller_.setSetpoint(setpoint);
    }
    
    /**
     * @brief Enable/disable PID control
     */
    void setPIDEnabled(bool enabled) {
        pid_enabled_ = enabled;
    }
    
    /**
     * @brief Check if reactor is SCRAMmed
     */
    bool isScrammed() const {
        return safety_system_.isScrammed();
    }
    
    /**
     * @brief Manually trigger SCRAM
     */
    void triggerScram() {
        safety_system_.triggerScram();
    }
    
    /**
     * @brief Reset SCRAM status
     */
    void resetScram() {
        safety_system_.resetScram();
    }
    
    /**
     * @brief Get reactor parameters
     */
    const ReactorParams& getReactorParams() const {
        return params_;
    }
};
