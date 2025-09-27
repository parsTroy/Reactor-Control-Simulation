#ifndef SAFETY_H
#define SAFETY_H

#include <utility>  // for std::pair

/**
 * @brief Safety system for reactor protection
 * 
 * This class implements safety interlocks that monitor reactor conditions
 * and trigger emergency shutdown (SCRAM) when unsafe conditions are detected.
 * Includes overpower protection and coolant loss detection.
 */
class SafetySystem {
private:
    // Trip thresholds
    double overpower_threshold_;     // Power level that triggers overpower trip
    double coolant_loss_threshold_;  // Temperature threshold for coolant loss detection
    
    // SCRAM parameters
    double scram_reactivity_;        // Reactivity inserted during SCRAM
    double scram_duration_;          // Duration of SCRAM (seconds)
    
    // System state
    bool is_scrammed_;              // Current SCRAM status
    bool coolant_loss_detected_;    // Coolant loss status
    double scram_start_time_;       // Time when SCRAM was initiated
    double last_power_level_;       // Last recorded power level
    
    // Trip flags
    bool overpower_trip_;           // Overpower trip flag
    bool coolant_trip_;             // Coolant loss trip flag

public:
    /**
     * @brief Constructor with default safety parameters
     * 
     * @param overpower_threshold Power level for overpower trip (default: 1.2)
     * @param coolant_threshold Temperature threshold for coolant loss (default: 350°C)
     * @param scram_reactivity Reactivity inserted during SCRAM (default: -0.1)
     */
    SafetySystem(double overpower_threshold = 1.2, 
                 double coolant_threshold = 350.0,
                 double scram_reactivity = -0.1);
    
    /**
     * @brief Check for overpower condition
     * 
     * Monitors current power level and triggers SCRAM if it exceeds threshold
     * 
     * @param current_power Current reactor power level
     * @param current_time Current simulation time
     * @return true if overpower trip is triggered
     */
    bool checkOverpowerTrip(double current_power, double current_time);
    
    /**
     * @brief Check for coolant loss condition
     * 
     * Monitors coolant temperature and triggers SCRAM if loss is detected
     * 
     * @param coolant_temperature Current coolant temperature (°C)
     * @param current_time Current simulation time
     * @return true if coolant loss trip is triggered
     */
    bool checkCoolantLossTrip(double coolant_temperature, double current_time);
    
    /**
     * @brief Get current reactivity based on safety status
     * 
     * Returns negative reactivity if SCRAM is active, zero otherwise
     * 
     * @param current_time Current simulation time
     * @return Reactivity contribution from safety system
     */
    double getSafetyReactivity(double current_time);
    
    /**
     * @brief Check if reactor is currently SCRAMmed
     * 
     * @return true if SCRAM is active
     */
    bool isScrammed() const { return is_scrammed_; }
    
    /**
     * @brief Check if coolant loss is detected
     * 
     * @return true if coolant loss is detected
     */
    bool isCoolantLossDetected() const { return coolant_loss_detected_; }
    
    /**
     * @brief Reset safety system
     * 
     * Clears all trip flags and resets SCRAM status
     */
    void reset();
    
    /**
     * @brief Set trip thresholds
     * 
     * @param overpower_threshold New overpower trip threshold
     * @param coolant_threshold New coolant loss trip threshold
     */
    void setTripThresholds(double overpower_threshold, double coolant_threshold);
    
    /**
     * @brief Get current trip status
     * 
     * @return Pair of (overpower_trip, coolant_trip) flags
     */
    std::pair<bool, bool> getTripStatus() const;
    
    /**
     * @brief Get SCRAM information
     * 
     * @return Pair of (is_scrammed, scram_duration) 
     */
    std::pair<bool, double> getScramInfo() const;
    
    // Getters for monitoring
    double getOverpowerThreshold() const { return overpower_threshold_; }
    double getCoolantLossThreshold() const { return coolant_loss_threshold_; }
};

#endif // SAFETY_H
