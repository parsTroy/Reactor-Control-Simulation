#ifndef KINETICS_SOLVER_H
#define KINETICS_SOLVER_H

#include <vector>

/**
 * @brief Reactor parameters for point kinetics calculations
 * 
 * This structure contains all the physical parameters needed to solve
 * the point kinetics equations. These parameters are specific to the
 * reactor design and fuel composition.
 */
struct ReactorParams {
    double Lambda;                    // Neutron generation time (seconds)
    double beta;                      // Total delayed neutron fraction
    std::vector<double> beta_i;       // Delayed neutron fraction for each group
    std::vector<double> lambda_i;     // Precursor decay constant for each group
    
    // Constructor with default values for a typical PWR
    ReactorParams() : Lambda(1e-5), beta(0.0065) {
        // Default 6-group delayed neutron parameters for U-235
        beta_i = {0.000215, 0.001424, 0.001274, 0.002568, 0.000748, 0.000273};
        lambda_i = {0.0124, 0.0305, 0.111, 0.301, 1.14, 3.01};
    }
};

/**
 * @brief Single step of point kinetics integration
 * 
 * This function implements one time step of the point kinetics equations
 * using Euler's method. The state vector contains neutron density followed
 * by delayed neutron precursor concentrations.
 * 
 * @param t Current time (seconds)
 * @param dt Time step size (seconds)
 * @param y Current state vector [n, C1, C2, ..., CM]
 * @param params Reactor physical parameters
 * @param rho Current reactivity (dimensionless)
 * @return Next state vector after time step dt
 */
std::vector<double> step_point_kinetics(
    double t,
    double dt,
    const std::vector<double>& y,
    const ReactorParams& params,
    double rho
);

/**
 * @brief Initialize state vector for reactor startup
 * 
 * Creates initial conditions for reactor simulation. The neutron density
 * is set to a small positive value, and precursor concentrations are
 * calculated assuming equilibrium conditions.
 * 
 * @param params Reactor physical parameters
 * @param initial_power Initial power level (normalized)
 * @return Initial state vector
 */
std::vector<double> initialize_reactor_state(
    const ReactorParams& params,
    double initial_power = 1.0
);

#endif // KINETICS_SOLVER_H
