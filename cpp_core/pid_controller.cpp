#include "pid_controller.h"
#include <algorithm>
#include <cmath>

/**
 * @brief Constructor with default parameters
 */
PIDController::PIDController(double kp, double ki, double kd, double setpoint, double dt)
    : kp_(kp), ki_(ki), kd_(kd), setpoint_(setpoint),
      previous_error_(0.0), integral_sum_(0.0), last_output_(0.0),
      integral_max_(1.0), integral_min_(-1.0),
      max_rate_(1.0), min_rate_(-1.0),
      output_max_(0.1), output_min_(-0.1), dt_(dt)
{
}

/**
 * @brief Calculate controller output for given power level
 * 
 * Implements the PID control algorithm:
 * output = Kp*e + Ki*∫e*dt + Kd*de/dt
 * 
 * @param current_power Current reactor power level
 * @return Controller output (reactivity adjustment)
 */
double PIDController::calculate(double current_power) {
    // Calculate error
    double error = setpoint_ - current_power;
    
    // Proportional term
    double proportional = kp_ * error;
    
    // Integral term with anti-windup
    integral_sum_ += error * dt_;
    
    // Apply anti-windup limits
    integral_sum_ = std::clamp(integral_sum_, integral_min_, integral_max_);
    
    double integral = ki_ * integral_sum_;
    
    // Derivative term
    double derivative = kd_ * (error - previous_error_) / dt_;
    
    // Calculate raw output
    double output = proportional + integral + derivative;
    
    // Apply output limits
    output = std::clamp(output, output_min_, output_max_);
    
    // Apply rate limiting
    double max_change = max_rate_ * dt_;
    double min_change = min_rate_ * dt_;
    double change = output - last_output_;
    change = std::clamp(change, min_change, max_change);
    output = last_output_ + change;
    
    // Update state
    previous_error_ = error;
    last_output_ = output;
    
    return output;
}

/**
 * @brief Set new setpoint
 */
void PIDController::setSetpoint(double new_setpoint) {
    setpoint_ = new_setpoint;
}

/**
 * @brief Reset controller state
 */
void PIDController::reset() {
    previous_error_ = 0.0;
    integral_sum_ = 0.0;
    last_output_ = 0.0;
}

/**
 * @brief Set PID gains
 */
void PIDController::setGains(double kp, double ki, double kd) {
    kp_ = kp;
    ki_ = ki;
    kd_ = kd;
}

/**
 * @brief Set output limits
 */
void PIDController::setOutputLimits(double min_output, double max_output) {
    output_min_ = min_output;
    output_max_ = max_output;
}

/**
 * @brief Set rate limits
 */
void PIDController::setRateLimits(double min_rate, double max_rate) {
    min_rate_ = min_rate;
    max_rate_ = max_rate;
}
