#include "MagneticField.h"
#include <cmath>

MagneticField::MagneticField()
    : m_ringRadius(100.0f), m_ringSeparation(300.0f), m_currentStrength(1.0f)
{
}

void MagneticField::setBottleParameters(float ringRadius, float ringSeparation, float currentStrength)
{
    m_ringRadius = ringRadius;
    m_ringSeparation = ringSeparation;
    m_currentStrength = currentStrength;
}

void MagneticField::adjustFieldStrength(float delta)
{
    m_currentStrength += delta;
    if (m_currentStrength < 0.1f)
        m_currentStrength = 0.1f;
}

Vector3 MagneticField::getFieldAt(const Vector3& position) const
{
    // Magnetic bottle consists of two current rings
    Vector3 ring1Center(-m_ringSeparation/2, 0, 0);
    Vector3 ring2Center(m_ringSeparation/2, 0, 0);
    
    Vector3 ring1Normal(1, 0, 0); // First ring normal points in +x direction
    Vector3 ring2Normal(-1, 0, 0); // Second ring normal points in -x direction
    
    // Combine fields from both rings
    Vector3 field1 = getRingFieldAt(position, ring1Center, ring1Normal, m_ringRadius);
    Vector3 field2 = getRingFieldAt(position, ring2Center, ring2Normal, m_ringRadius);
    
    return field1 + field2;
}

Vector3 MagneticField::getRingFieldAt(const Vector3& position, const Vector3& ringCenter, 
                                     const Vector3& ringNormal, float ringRadius) const
{
    // Calculate displacement vector from ring center to position
    Vector3 r = position - ringCenter;
    float distanceSquared = r.dot(r);
    
    if (distanceSquared < 1e-10f) // Avoid singularity at center
        return Vector3(0, 0, 0);

    float distance = std::sqrt(distanceSquared);
    
    // Project r onto ring axis
    float rDotAxis = r.dot(ringNormal);
    Vector3 rAxis = ringNormal * rDotAxis;
    Vector3 rPerp = r - rAxis;
    float rPerpMag = rPerp.magnitude();

    // Simplified magnetic field calculation for a current loop
    // This is a physics approximation for visualization purposes
    float z = rDotAxis;
    float rho = rPerpMag;
    float fieldFactor = MU0 * m_currentStrength * ringRadius * ringRadius / 
                     (2.0f * std::pow((ringRadius * ringRadius + distance * distance), 1.5f));

    // Components of the field
    float Bz = fieldFactor * (1 + 0.5f * z * z / (ringRadius * ringRadius + distance * distance));
    float Brho = fieldFactor * (z * rho / (ringRadius * ringRadius + distance * distance));

    // Convert to Cartesian coordinates
    Vector3 field;
    if (rPerpMag > 1e-10f) {
        Vector3 rPerpUnit = rPerp / rPerpMag;
        field = ringNormal * Bz + rPerpUnit * Brho;
    } else {
        field = ringNormal * Bz;
    }

    return field;
}

std::vector<std::vector<Vector3>> MagneticField::generateFieldLines(int numLines, int pointsPerLine) const
{
    std::vector<std::vector<Vector3>> fieldLines;
    
    // Generate starting points along a circle in the middle of the bottle
    float radius = m_ringRadius * 0.7f;
    for (int i = 0; i < numLines; ++i)
    {
        float angle = 2.0f * M_PI * i / numLines;
        Vector3 startPoint(0, radius * cos(angle), radius * sin(angle));
        
        std::vector<Vector3> fieldLine;
        Vector3 currentPoint = startPoint;
        fieldLine.push_back(currentPoint);
        
        // Trace field line in both directions
        for (int dir = -1; dir <= 1; dir += 2) {
            Vector3 point = startPoint;
            
            for (int j = 0; j < pointsPerLine / 2; ++j)
            {
                Vector3 field = getFieldAt(point);
                float fieldMag = field.magnitude();
                
                if (fieldMag < 1e-10f)
                    break;
                
                // Step along field direction
                Vector3 direction = field * (dir / fieldMag);
                point = point + direction * 5.0f;
                
                // Add point to the line (in correct order)
                if (dir < 0)
                    fieldLine.insert(fieldLine.begin(), point);
                else
                    fieldLine.push_back(point);
                
                // Stop if we've gone too far from the center
                if (point.magnitude() > m_ringSeparation * 1.5f)
                    break;
            }
        }
        
        fieldLines.push_back(fieldLine);
    }
    
    return fieldLines;
}