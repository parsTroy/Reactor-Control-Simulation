#ifndef PID_CONTROLLER_H
#define PID_CONTROLLER_H

/**
 * @brief PID Controller for reactor power control
 * 
 * This class implements a Proportional-Integral-Derivative (PID) controller
 * to automatically adjust reactor reactivity and maintain desired power level.
 * Includes anti-windup protection and rate limiting for safe operation.
 */
class PIDController {
private:
    // PID gains
    double kp_;     // Proportional gain
    double ki_;     // Integral gain  
    double kd_;     // Derivative gain
    
    // Controller state
    double setpoint_;           // Desired power level
    double previous_error_;     // Previous error for derivative term
    double integral_sum_;       // Integral term accumulator
    double last_output_;        // Previous controller output
    
    // Anti-windup parameters
    double integral_max_;       // Maximum integral term
    double integral_min_;       // Minimum integral term
    
    // Rate limiting parameters
    double max_rate_;           // Maximum rate of change (per second)
    double min_rate_;           // Minimum rate of change (per second)
    
    // Output limits
    double output_max_;         // Maximum controller output
    double output_min_;         // Minimum controller output
    
    // Time step for derivative calculation
    double dt_;

public:
    /**
     * @brief Constructor with default parameters
     * 
     * @param kp Proportional gain (default: 0.1)
     * @param ki Integral gain (default: 0.01) 
     * @param kd Derivative gain (default: 0.05)
     * @param setpoint Initial setpoint (default: 1.0)
     * @param dt Time step (default: 0.01)
     */
    PIDController(double kp = 0.1, double ki = 0.01, double kd = 0.05, 
                  double setpoint = 1.0, double dt = 0.01);
    
    /**
     * @brief Calculate controller output for given power level
     * 
     * @param current_power Current reactor power level
     * @return Controller output (reactivity adjustment)
     */
    double calculate(double current_power);
    
    /**
     * @brief Set new setpoint
     * 
     * @param new_setpoint Desired power level
     */
    void setSetpoint(double new_setpoint);
    
    /**
     * @brief Reset controller state
     * 
     * Clears integral term and resets derivative calculation
     */
    void reset();
    
    /**
     * @brief Set PID gains
     * 
     * @param kp Proportional gain
     * @param ki Integral gain
     * @param kd Derivative gain
     */
    void setGains(double kp, double ki, double kd);
    
    /**
     * @brief Set output limits
     * 
     * @param min_output Minimum controller output
     * @param max_output Maximum controller output
     */
    void setOutputLimits(double min_output, double max_output);
    
    /**
     * @brief Set rate limits
     * 
     * @param min_rate Minimum rate of change
     * @param max_rate Maximum rate of change
     */
    void setRateLimits(double min_rate, double max_rate);
    
    // Getters for monitoring
    double getSetpoint() const { return setpoint_; }
    double getIntegralSum() const { return integral_sum_; }
    double getLastOutput() const { return last_output_; }
    double getKp() const { return kp_; }
    double getKi() const { return ki_; }
    double getKd() const { return kd_; }
};

#endif // PID_CONTROLLER_H
