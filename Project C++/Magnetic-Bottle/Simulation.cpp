#include "Simulation.h"

Simulation::Simulation()
{
    // Set up magnetic bottle parameters
    m_magneticField.setBottleParameters(100.0f, 400.0f, 1.0f);
    
    // Initialize electron
    resetElectron();
}

void Simulation::update(float dt)
{
    // Scale time for better visualization
    float scaledDt = dt * TIME_SCALE;
    
    // Get current state
    Vector3 position = m_electron.getPosition();
    Vector3 velocity = m_electron.getVelocity();
    
    // Get magnetic field at current position
    Vector3 magneticField = m_magneticField.getFieldAt(position);
    
    // Calculate Lorentz force: F = q(v × B)
    Vector3 force = velocity.cross(magneticField) * ELECTRON_CHARGE;
    
    // Update electron
    m_electron.update(force, scaledDt);
}

void Simulation::resetElectron()
{
    // Place electron in the middle with velocity perpendicular to bottle axis
    Vector3 initPosition(0.0f, 30.0f, 0.0f);
    Vector3 initVelocity(0.0f, 0.0f, 300.0f); // Initial velocity perpendicular to field
    m_electron.reset(initPosition, initVelocity);
}

void Simulation::adjustFieldStrength(float delta)
{
    m_magneticField.adjustFieldStrength(delta);
}