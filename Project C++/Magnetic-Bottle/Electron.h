#pragma once
#include "Vector3.h"
#include <queue>
#include <vector>

class Electron
{
public:
    Electron();
    
    void reset(const Vector3& position, const Vector3& velocity);
    void update(const Vector3& force, float dt);
    
    Vector3 getPosition() const { return m_position; }
    Vector3 getVelocity() const { return m_velocity; }
    
    // For drawing the trajectory
    std::vector<Vector3> getTrajectoryPoints() const;
    
private:
    Vector3 m_position;
    Vector3 m_velocity;
    
    // Store recent positions for trajectory visualization
    static const int MAX_TRAIL_POINTS = 1000;
    std::queue<Vector3> m_trajectoryPoints;
};