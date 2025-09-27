#include "kinetics_solver.h"
#include <algorithm>
#include <stdexcept>

/**
 * @brief Single step of point kinetics integration using Euler's method
 * 
 * This function implements one time step of the point kinetics equations:
 * dn/dt = (ρ(t) - β)/Λ * n(t) + Σ λᵢ * Cᵢ(t)
 * dCᵢ/dt = βᵢ/Λ * n(t) - λᵢ * Cᵢ(t)
 * 
 * @param t Current time (seconds)
 * @param dt Time step size (seconds)
 * @param y Current state vector [n, C1, C2, ..., CM]
 * @param params Reactor physical parameters
 * @param rho Current reactivity (dimensionless)
 * @return Next state vector after time step dt
 */
std::vector<double> step_point_kinetics(
    double /* t */,  // Time parameter (unused but kept for future extensibility)
    double dt,
    const std::vector<double>& y,
    const ReactorParams& params,
    double rho)
{
    // Validate input
    if (y.size() != 1 + params.beta_i.size()) {
        throw std::invalid_argument("State vector size doesn't match number of delayed neutron groups");
    }
    
    if (params.beta_i.size() != params.lambda_i.size()) {
        throw std::invalid_argument("Number of beta_i and lambda_i must be equal");
    }
    
    // Check for reasonable time step size to prevent instability
    double max_dt = params.Lambda / 10.0;  // Time step should be much smaller than generation time
    if (dt > max_dt) {
        throw std::invalid_argument("Time step too large for numerical stability. Max allowed: " + 
                                  std::to_string(max_dt) + "s, provided: " + std::to_string(dt) + "s");
    }
    
    // Extract neutron density and precursor concentrations
    double n = y[0];
    std::vector<double> C(y.begin() + 1, y.end());
    
    // Check for negative or extremely large values (sanity check)
    if (n < 0.0 || n > 1e10) {
        throw std::runtime_error("Neutron density out of reasonable range: " + std::to_string(n));
    }
    
    // Calculate neutron density derivative
    // dn/dt = (ρ - β)/Λ * n + Σ λᵢ * Cᵢ
    double dn_dt = ((rho - params.beta) / params.Lambda) * n;
    for (size_t i = 0; i < C.size(); ++i) {
        dn_dt += params.lambda_i[i] * C[i];
    }
    
    // Calculate precursor concentration derivatives
    // dCᵢ/dt = βᵢ/Λ * n - λᵢ * Cᵢ
    std::vector<double> dC_dt(C.size());
    for (size_t i = 0; i < C.size(); ++i) {
        dC_dt[i] = (params.beta_i[i] / params.Lambda) * n - params.lambda_i[i] * C[i];
    }
    
    // Apply Euler's method: y_next = y + dt * dy/dt
    std::vector<double> y_next;
    y_next.reserve(y.size());
    
    // Update neutron density with bounds checking
    double n_next = n + dt * dn_dt;
    if (n_next < 0.0) {
        n_next = 0.0;  // Neutron density cannot be negative
    } else if (n_next > 1e6) {
        n_next = 1e6;  // Cap at reasonable maximum
    }
    y_next.push_back(n_next);
    
    // Update precursor concentrations with bounds checking
    for (size_t i = 0; i < C.size(); ++i) {
        double C_next = C[i] + dt * dC_dt[i];
        if (C_next < 0.0) {
            C_next = 0.0;  // Precursor concentrations cannot be negative
        } else if (C_next > 1e6) {
            C_next = 1e6;  // Cap at reasonable maximum
        }
        y_next.push_back(C_next);
    }
    
    return y_next;
}

/**
 * @brief Initialize state vector for reactor startup
 * 
 * Creates initial conditions assuming the reactor is at steady state
 * with the specified power level. At steady state, dCᵢ/dt = 0, so:
 * Cᵢ = (βᵢ/Λ) * n / λᵢ
 * 
 * @param params Reactor physical parameters
 * @param initial_power Initial power level (normalized)
 * @return Initial state vector
 */
std::vector<double> initialize_reactor_state(
    const ReactorParams& params,
    double initial_power)
{
    if (initial_power <= 0.0) {
        throw std::invalid_argument("Initial power must be positive");
    }
    
    std::vector<double> state;
    state.reserve(1 + params.beta_i.size());
    
    // Set neutron density (proportional to power)
    state.push_back(initial_power);
    
    // Calculate equilibrium precursor concentrations
    // At steady state: Cᵢ = (βᵢ/Λ) * n / λᵢ
    for (size_t i = 0; i < params.beta_i.size(); ++i) {
        double C_i = (params.beta_i[i] / params.Lambda) * initial_power / params.lambda_i[i];
        state.push_back(C_i);
    }
    
    return state;
}
