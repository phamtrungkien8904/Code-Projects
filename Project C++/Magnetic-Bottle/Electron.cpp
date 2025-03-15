#include "Electron.h"

Electron::Electron()
    : m_position(0, 0, 0), m_velocity(0, 0, 0)
{
}

void Electron::reset(const Vector3& position, const Vector3& velocity)
{
    m_position = position;
    m_velocity = velocity;
    
    // Clear trajectory
    std::queue<Vector3> empty;
    std::swap(m_trajectoryPoints, empty);
    m_trajectoryPoints.push(position);
}

void Electron::update(const Vector3& force, float dt)
{
    // Apply force (F = ma, assuming unit mass)
    m_velocity = m_velocity + force * dt;
    
    // Update position
    m_position = m_position + m_velocity * dt;
    
    // Add position to trajectory
    m_trajectoryPoints.push(m_position);
    
    // Keep trajectory to a manageable size
    if (m_trajectoryPoints.size() > MAX_TRAIL_POINTS)
        m_trajectoryPoints.pop();
}

std::vector<Vector3> Electron::getTrajectoryPoints() const
{
    std::vector<Vector3> points;
    std::queue<Vector3> temp = m_trajectoryPoints; // Copy the queue
    
    while (!temp.empty()) {
        points.push_back(temp.front());
        temp.pop();
    }
    
    return points;
}