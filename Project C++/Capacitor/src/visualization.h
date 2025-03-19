#pragma once

#include <SFML/Graphics.hpp>
#include "simulator.h"

class Visualization {
public:
    // Constructor with window dimensions and pixel scale
    Visualization(int windowWidth, int windowHeight, int pixelScale);
    
    // Render the electric potential as a color map
    void renderPotential(sf::RenderWindow& window, const Simulator& simulator);
    
    // Render equipotential lines
    void renderEquipotentialLines(sf::RenderWindow& window, const Simulator& simulator, int numLines);
    
    // Render electric field lines
    void renderElectricField(sf::RenderWindow& window, const Simulator& simulator, int spacing);
    
    // Draw the capacitor plates
    void renderCapacitorPlates(sf::RenderWindow& window, int gridWidth, int gridHeight, 
                              int plateWidth, int plateGap);

private:
    int m_windowWidth;
    int m_windowHeight;
    int m_pixelScale;
    
    // Helper function to map potential value to color
    sf::Color getPotentialColor(double potential, double minPotential, double maxPotential);
    
    // Helper function to convert grid coordinates to window coordinates
    sf::Vector2f gridToWindow(int x, int y) const;
};