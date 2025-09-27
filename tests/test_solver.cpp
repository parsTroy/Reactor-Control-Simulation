#include <gtest/gtest.h>
#include <vector>
#include <cmath>
#include "kinetics_solver.h"

/**
 * @brief Test suite for kinetics solver
 * 
 * These tests verify that our point kinetics solver correctly implements
 * the mathematical equations and produces physically reasonable results.
 */
class KineticsSolverTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Create reactor parameters for testing
        params.Lambda = 1e-5;  // 10 microseconds
        params.beta = 0.0065;  // 0.65% delayed neutrons
        
        // 6-group delayed neutron parameters for U-235
        params.beta_i = {0.000215, 0.001424, 0.001274, 0.002568, 0.000748, 0.000273};
        params.lambda_i = {0.0124, 0.0305, 0.111, 0.301, 1.14, 3.01};
        
        dt = 0.001;  // 1 millisecond time step
    }
    
    ReactorParams params;
    double dt;
};

/**
 * @brief Test that positive reactivity increases neutron density
 * 
 * This is a fundamental test - when we insert positive reactivity,
 * the neutron population should grow exponentially.
 */
TEST_F(KineticsSolverTest, PositiveReactivityIncreasesNeutronDensity) {
    // Initialize reactor at steady state
    auto state = initialize_reactor_state(params, 1.0);
    double initial_neutron_density = state[0];
    
    // Insert positive reactivity (0.001 = 1 mk)
    double reactivity = 0.001;
    
    // Run simulation for 1 second
    double time = 0.0;
    for (int i = 0; i < 1000; ++i) {
        state = step_point_kinetics(time, dt, state, params, reactivity);
        time += dt;
    }
    
    double final_neutron_density = state[0];
    
    // Neutron density should have increased
    EXPECT_GT(final_neutron_density, initial_neutron_density);
    
    // Should have grown significantly (at least 10x)
    EXPECT_GT(final_neutron_density / initial_neutron_density, 10.0);
}

/**
 * @brief Test that negative reactivity decreases neutron density
 * 
 * When we insert negative reactivity, the neutron population should
 * decrease exponentially.
 */
TEST_F(KineticsSolverTest, NegativeReactivityDecreasesNeutronDensity) {
    // Initialize reactor at steady state
    auto state = initialize_reactor_state(params, 1.0);
    double initial_neutron_density = state[0];
    
    // Insert negative reactivity (-0.001 = -1 mk)
    double reactivity = -0.001;
    
    // Run simulation for 1 second
    double time = 0.0;
    for (int i = 0; i < 1000; ++i) {
        state = step_point_kinetics(time, dt, state, params, reactivity);
        time += dt;
    }
    
    double final_neutron_density = state[0];
    
    // Neutron density should have decreased
    EXPECT_LT(final_neutron_density, initial_neutron_density);
    
    // Should have decreased significantly (at least 10x)
    EXPECT_LT(final_neutron_density / initial_neutron_density, 0.1);
}

/**
 * @brief Test that zero reactivity maintains steady state
 * 
 * With zero reactivity, the reactor should remain at steady state
 * (neutron density should remain approximately constant).
 */
TEST_F(KineticsSolverTest, ZeroReactivityMaintainsSteadyState) {
    // Initialize reactor at steady state
    auto state = initialize_reactor_state(params, 1.0);
    double initial_neutron_density = state[0];
    
    // Zero reactivity
    double reactivity = 0.0;
    
    // Run simulation for 1 second
    double time = 0.0;
    for (int i = 0; i < 1000; ++i) {
        state = step_point_kinetics(time, dt, state, params, reactivity);
        time += dt;
    }
    
    double final_neutron_density = state[0];
    
    // Neutron density should remain approximately the same
    // (within 5% tolerance due to numerical errors)
    double relative_change = std::abs(final_neutron_density - initial_neutron_density) / initial_neutron_density;
    EXPECT_LT(relative_change, 0.05);
}

/**
 * @brief Test that state vector has correct size
 * 
 * The state vector should contain 1 neutron density + M precursor concentrations
 * where M is the number of delayed neutron groups.
 */
TEST_F(KineticsSolverTest, StateVectorHasCorrectSize) {
    auto state = initialize_reactor_state(params, 1.0);
    
    // Should have 1 + number of delayed neutron groups
    size_t expected_size = 1 + params.beta_i.size();
    EXPECT_EQ(state.size(), expected_size);
    
    // All values should be positive
    for (double value : state) {
        EXPECT_GT(value, 0.0);
    }
}
