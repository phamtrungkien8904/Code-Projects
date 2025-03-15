#pragma once
#include "Vector3.h"
#include <vector>

class MagneticField
{
public:
    MagneticField();
    
    // Calculate the magnetic field at a given position
    Vector3 getFieldAt(const Vector3& position) const;
    
    // Set parameters for the magnetic bottle
    void setBottleParameters(float ringRadius, float ringSeparation, float currentStrength);
    
    // Adjust the field strength
    void adjustFieldStrength(float delta);
    
    // Generate field lines for visualization
    std::vector<std::vector<Vector3>> generateFieldLines(int numLines, int pointsPerLine) const;
    
private:
    // Calculate magnetic field from a single current ring
    Vector3 getRingFieldAt(const Vector3& position, const Vector3& ringCenter, 
                           const Vector3& ringNormal, float ringRadius) const;
    
    float m_ringRadius;       // Radius of each ring
    float m_ringSeparation;   // Distance between rings
    float m_currentStrength;  // Current flowing in the rings (proportional to field strength)
    
    const float MU0 = 1.0f;   // Simplified magnetic constant for visualization
};