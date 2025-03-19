#include "visualization.h"
#include <cmath>
#include <vector>

Visualization::Visualization(int windowWidth, int windowHeight, int pixelScale)
    : m_windowWidth(windowWidth), m_windowHeight(windowHeight), m_pixelScale(pixelScale)
{
}

sf::Color Visualization::getPotentialColor(double potential, double minPotential, double maxPotential) {
    // Normalize potential to [0, 1]
    double normalized = (potential - minPotential) / (maxPotential - minPotential);
    
    // Use a blue-white-red color scale
    if (normalized < 0.5) {
        // Blue to white
        int blue = 255;
        int redGreen = static_cast<int>(normalized * 2 * 255);
        return sf::Color(redGreen, redGreen, blue);
    } else {
        // White to red
        int red = 255;
        int greenBlue = static_cast<int>((1.0 - (normalized - 0.5) * 2) * 255);
        return sf::Color(red, greenBlue, greenBlue);
    }
}

sf::Vector2f Visualization::gridToWindow(int x, int y) const {
    return sf::Vector2f(static_cast<float>(x * m_pixelScale), 
                        static_cast<float>(y * m_pixelScale));
}

void Visualization::renderPotential(sf::RenderWindow& window, const Simulator& simulator) {
    const auto& potential = simulator.getPotential();
    int gridWidth = potential.size();
    if (gridWidth == 0) return;
    int gridHeight = potential[0].size();
    
    double minPotential = simulator.getMinPotential();
    double maxPotential = simulator.getMaxPotential();
    
    sf::RectangleShape pixel(sf::Vector2f(m_pixelScale, m_pixelScale));
    
    for (int x = 0; x < gridWidth; ++x) {
        for (int y = 0; y < gridHeight; ++y) {
            pixel.setPosition(gridToWindow(x, y));
            pixel.setFillColor(getPotentialColor(potential[x][y], minPotential, maxPotential));
            window.draw(pixel);
        }
    }
}

void Visualization::renderEquipotentialLines(sf::RenderWindow& window, const Simulator& simulator, int numLines) {
    const auto& potential = simulator.getPotential();
    int gridWidth = potential.size();
    if (gridWidth == 0) return;
    int gridHeight = potential[0].size();
    
    double minPotential = simulator.getMinPotential();
    double maxPotential = simulator.getMaxPotential();
    double potentialStep = (maxPotential - minPotential) / (numLines + 1);
    
    // For each potential level we want to draw
    for (int i = 1; i <= numLines; ++i) {
        double targetPotential = minPotential + i * potentialStep;
        
        // Find points that are close to this potential level
        for (int x = 1; x < gridWidth - 1; ++x) {
            for (int y = 1; y < gridHeight - 1; ++y) {
                // Check if this point straddles the target potential
                if ((potential[x][y] <= targetPotential && potential[x+1][y] > targetPotential) ||
                    (potential[x][y] > targetPotential && potential[x+1][y] <= targetPotential) ||
                    (potential[x][y] <= targetPotential && potential[x][y+1] > targetPotential) ||
                    (potential[x][y] > targetPotential && potential[x][y+1] <= targetPotential)) {
                    
                    sf::CircleShape point(1);
                    point.setFillColor(sf::Color::White);
                    point.setPosition(gridToWindow(x, y));
                    window.draw(point);
                }
            }
        }
    }
}

void Visualization::renderElectricField(sf::RenderWindow& window, const Simulator& simulator, int spacing) {
    const auto& electricField = simulator.getElectricField();
    int gridWidth = electricField.size();
    if (gridWidth == 0) return;
    int gridHeight = electricField[0].size();
    
    double maxFieldStrength = simulator.getMaxFieldStrength();
    if (maxFieldStrength <= 0) return;
    
    for (int x = spacing; x < gridWidth - spacing; x += spacing) {
        for (int y = spacing; y < gridHeight - spacing; y += spacing) {
            double Ex = electricField[x][y].first;
            double Ey = electricField[x][y].second;
            double fieldStrength = std::sqrt(Ex*Ex + Ey*Ey);
            
            if (fieldStrength > 0.001 * maxFieldStrength) {  // Don't draw very small fields
                // Normalize the field vector
                double normalizedLength = 5.0 * fieldStrength / maxFieldStrength;
                Ex = Ex / fieldStrength * normalizedLength;
                Ey = Ey / fieldStrength * normalizedLength;
                
                // Draw arrow from (x,y) in the direction of the field
                sf::Vertex line[] = {
                    sf::Vertex(gridToWindow(x, y), sf::Color::Green),
                    sf::Vertex(gridToWindow(x + Ex, y + Ey), sf::Color::Green)
                };
                
                window.draw(line, 2, sf::Lines);
            }
        }
    }
}

void Visualization::renderCapacitorPlates(sf::RenderWindow& window, int gridWidth, int gridHeight, 
                                        int plateWidth, int plateGap) {
    int centerY = gridHeight / 2;
    int topPlateY = centerY - plateGap / 2;
    int bottomPlateY = centerY + plateGap / 2;
    int plateStartX = (gridWidth - plateWidth) / 2;
    int plateEndX = plateStartX + plateWidth;
    
    // Top plate (positive)
    sf::RectangleShape topPlate(sf::Vector2f(plateWidth * m_pixelScale, m_pixelScale));
    topPlate.setPosition(gridToWindow(plateStartX, topPlateY));
    topPlate.setFillColor(sf::Color::Red);
    window.draw(topPlate);
    
    // Bottom plate (negative)
    sf::RectangleShape bottomPlate(sf::Vector2f(plateWidth * m_pixelScale, m_pixelScale));
    bottomPlate.setPosition(gridToWindow(plateStartX, bottomPlateY));
    bottomPlate.setFillColor(sf::Color::Blue);
    window.draw(bottomPlate);
}