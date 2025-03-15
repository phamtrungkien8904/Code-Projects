#include "Renderer.h"
#include <sstream>
#include <iostream>

Renderer::Renderer(sf::RenderWindow* window, Simulation* simulation)
    : m_window(window), m_simulation(simulation), m_fieldLinesDirty(true)
{
    // Load font
    if (!m_font.loadFromFile("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")) {
        // If font loading fails, we'll continue without text
        std::cerr << "Could not load font!" << std::endl;
    }
    
    m_infoText.setFont(m_font);
    m_infoText.setCharacterSize(14);
    m_infoText.setFillColor(sf::Color::White);
    m_infoText.setPosition(10, 10);
}

void Renderer::render()
{
    renderMagneticBottle();
    renderMagneticField();
    renderElectron();
    renderElectronTrajectory();
    renderInfo();
}

sf::Vector2f Renderer::worldToScreen(const Vector3& worldPos)
{
    // Simple projection: x-z plane to screen with y component giving color intensity
    float screenX = m_window->getSize().x / 2 + worldPos.x;
    float screenY = m_window->getSize().y / 2 - worldPos.z; // Invert y for screen coordinates
    
    return sf::Vector2f(screenX, screenY);
}

void Renderer::renderMagneticBottle()
{
    // Get parameters from the simulation
    const MagneticField& field = m_simulation->getMagneticField();
    
    // Draw two circles representing the current loops
    sf::CircleShape ring1, ring2;
    
    // First ring
    ring1.setRadius(100);
    ring1.setOrigin(100, 100);
    ring1.setPosition(m_window->getSize().x / 2 - 200, m_window->getSize().y / 2);
    ring1.setFillColor(sf::Color::Transparent);
    ring1.setOutlineColor(sf::Color(50, 100, 200));
    ring1.setOutlineThickness(5);
    
    // Second ring
    ring2.setRadius(100);
    ring2.setOrigin(100, 100);
    ring2.setPosition(m_window->getSize().x / 2 + 200, m_window->getSize().y / 2);
    ring2.setFillColor(sf::Color::Transparent);
    ring2.setOutlineColor(sf::Color(50, 100, 200));
    ring2.setOutlineThickness(5);
    
    m_window->draw(ring1);
    m_window->draw(ring2);
}

void Renderer::renderMagneticField()
{
    // Generate field lines if needed
    if (m_fieldLinesDirty) {
        m_fieldLines.clear();
        
        const MagneticField& field = m_simulation->getMagneticField();
        auto fieldLinePoints = field.generateFieldLines(12, 100);
        
        for (const auto& line : fieldLinePoints) {
            std::vector<sf::Vertex> vertices;
            
            for (size_t i = 0; i < line.size(); ++i) {
                sf::Vector2f screenPos = worldToScreen(line[i]);
                
                // Color gradient based on field strength
                float fieldStrength = field.getFieldAt(line[i]).magnitude();
                float intensity = std::min(255.0f, fieldStrength * 100.0f);
                
                sf::Color color(
                    static_cast<sf::Uint8>(50 + intensity * 0.2),  // R
                    static_cast<sf::Uint8>(50 + intensity * 0.4),  // G
                    static_cast<sf::Uint8>(100 + intensity * 0.6)  // B
                );
                
                vertices.push_back(sf::Vertex(screenPos, color));
            }
            
            m_fieldLines.push_back(vertices);
        }
        
        m_fieldLinesDirty = false;
    }
    
    // Draw field lines
    for (const auto& line : m_fieldLines) {
        m_window->draw(line.data(), line.size(), sf::LineStrip);
    }
}

void Renderer::renderElectron()
{
    // Get electron position
    Vector3 position = m_simulation->getElectron().getPosition();
    sf::Vector2f screenPos = worldToScreen(position);
    
    // Draw electron
    sf::CircleShape electronShape(5);
    electronShape.setOrigin(5, 5);
    electronShape.setPosition(screenPos);
    electronShape.setFillColor(sf::Color(255, 100, 100));
    
    m_window->draw(electronShape);
}

void Renderer::renderElectronTrajectory()
{
    // Get electron trajectory
    std::vector<Vector3> trajectoryPoints = m_simulation->getElectron().getTrajectoryPoints();
    
    if (trajectoryPoints.size() < 2)
        return;
    
    // Create vertex array for trajectory
    std::vector<sf::Vertex> trajectory;
    
    for (size_t i = 0; i < trajectoryPoints.size(); ++i) {
        sf::Vector2f screenPos = worldToScreen(trajectoryPoints[i]);
        
        // Fade color based on position in trajectory
        float alpha = static_cast<float>(i) / trajectoryPoints.size();
        sf::Color color(255, 100, 100, static_cast<sf::Uint8>(alpha * 200));
        
        trajectory.push_back(sf::Vertex(screenPos, color));
    }
    
    m_window->draw(trajectory.data(), trajectory.size(), sf::LineStrip);
}

void Renderer::renderInfo()
{
    const Vector3& position = m_simulation->getElectron().getPosition();
    const Vector3& velocity = m_simulation->getElectron().getVelocity();
    
    std::stringstream ss;
    ss << "Electron Position: (" << position.x << ", " << position.y << ", " << position.z << ")" << std::endl;
    ss << "Electron Velocity: (" << velocity.x << ", " << velocity.y << ", " << velocity.z << ")" << std::endl;
    ss << "Velocity Magnitude: " << velocity.magnitude() << std::endl;
    ss << std::endl;
    ss << "Controls:" << std::endl;
    ss << "R - Reset electron" << std::endl;
    ss << "Up/Down - Adjust magnetic field strength" << std::endl;
    
    m_infoText.setString(ss.str());
    m_window->draw(m_infoText);
}