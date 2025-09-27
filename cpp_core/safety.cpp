#include "safety.h"
#include <algorithm>

/**
 * @brief Constructor with default safety parameters
 */
SafetySystem::SafetySystem(double overpower_threshold, double coolant_threshold, double scram_reactivity)
    : overpower_threshold_(overpower_threshold),
      coolant_loss_threshold_(coolant_threshold),
      scram_reactivity_(scram_reactivity),
      scram_duration_(10.0),  // 10 seconds SCRAM duration
      is_scrammed_(false),
      coolant_loss_detected_(false),
      scram_start_time_(0.0),
      last_power_level_(0.0),
      overpower_trip_(false),
      coolant_trip_(false)
{
}

/**
 * @brief Check for overpower condition
 */
bool SafetySystem::checkOverpowerTrip(double current_power, double current_time) {
    last_power_level_ = current_power;
    
    // Check if power exceeds threshold
    if (current_power > overpower_threshold_) {
        overpower_trip_ = true;
        is_scrammed_ = true;
        scram_start_time_ = current_time;
        return true;
    }
    
    return false;
}

/**
 * @brief Check for coolant loss condition
 */
bool SafetySystem::checkCoolantLossTrip(double coolant_temperature, double current_time) {
    // Check if temperature exceeds threshold (indicating coolant loss)
    if (coolant_temperature > coolant_loss_threshold_) {
        coolant_loss_detected_ = true;
        coolant_trip_ = true;
        is_scrammed_ = true;
        scram_start_time_ = current_time;
        return true;
    }
    
    return false;
}

/**
 * @brief Get current reactivity based on safety status
 */
double SafetySystem::getSafetyReactivity(double current_time) {
    if (!is_scrammed_) {
        return 0.0;  // No safety reactivity
    }
    
    // Check if SCRAM duration has expired
    if (current_time - scram_start_time_ > scram_duration_) {
        is_scrammed_ = false;  // SCRAM has ended
        return 0.0;
    }
    
    // Return negative reactivity during SCRAM
    return scram_reactivity_;
}

/**
 * @brief Reset safety system
 */
void SafetySystem::reset() {
    is_scrammed_ = false;
    coolant_loss_detected_ = false;
    scram_start_time_ = 0.0;
    last_power_level_ = 0.0;
    overpower_trip_ = false;
    coolant_trip_ = false;
}

/**
 * @brief Set trip thresholds
 */
void SafetySystem::setTripThresholds(double overpower_threshold, double coolant_threshold) {
    overpower_threshold_ = overpower_threshold;
    coolant_loss_threshold_ = coolant_threshold;
}

/**
 * @brief Get current trip status
 */
std::pair<bool, bool> SafetySystem::getTripStatus() const {
    return std::make_pair(overpower_trip_, coolant_trip_);
}

/**
 * @brief Get SCRAM information
 */
std::pair<bool, double> SafetySystem::getScramInfo() const {
    double scram_duration = is_scrammed_ ? (scram_start_time_ + scram_duration_) : 0.0;
    return std::make_pair(is_scrammed_, scram_duration);
}

/**
 * @brief Manually trigger SCRAM
 */
void SafetySystem::triggerScram() {
    is_scrammed_ = true;
    scram_start_time_ = 0.0;  // Will be set properly when simulation steps
    overpower_trip_ = true;   // Mark as overpower trip
}

/**
 * @brief Reset SCRAM status
 */
void SafetySystem::resetScram() {
    is_scrammed_ = false;
    scram_start_time_ = 0.0;
    overpower_trip_ = false;
    coolant_trip_ = false;
    coolant_loss_detected_ = false;
}
