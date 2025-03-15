#pragma once
#include <SFML/Graphics.hpp>
#include "Simulation.h"
#include <vector>

class Renderer
{
public:
    Renderer(sf::RenderWindow* window, Simulation* simulation);
    
    void render();
    
private:
    void renderMagneticBottle();
    void renderMagneticField();
    void renderElectron();
    void renderElectronTrajectory();
    void renderInfo();
    
    // Convert 3D coordinates to 2D screen coordinates
    sf::Vector2f worldToScreen(const Vector3& worldPos);
    
    sf::RenderWindow* m_window;
    Simulation* m_simulation;
    
    // Cache for field line visualization
    std::vector<std::vector<sf::Vertex>> m_fieldLines;
    bool m_fieldLinesDirty;
    
    // Text for info display
    sf::Font m_font;
    sf::Text m_infoText;
};