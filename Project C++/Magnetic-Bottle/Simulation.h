#pragma once
#include "MagneticField.h"
#include "Electron.h"

class Simulation
{
public:
    Simulation();
    
    void update(float dt);
    void resetElectron();
    void adjustFieldStrength(float delta);
    
    const MagneticField& getMagneticField() const { return m_magneticField; }
    const Electron& getElectron() const { return m_electron; }
    
private:
    MagneticField m_magneticField;
    Electron m_electron;
    
    const float ELECTRON_CHARGE = -1.0f; // Simplified electron charge
    const float TIME_SCALE = 0.5f;       // Scale factor for time steps
};