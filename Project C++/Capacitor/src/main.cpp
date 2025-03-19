#include <SFML/Graphics.hpp>
#include "simulator.h"
#include "visualization.h"
#include <iostream>

int main() {
    // Simulation parameters
    const int GRID_WIDTH = 200;
    const int GRID_HEIGHT = 200;
    const int PLATE_WIDTH = 80;
    const int PLATE_GAP = 40;
    const double VOLTAGE = 10.0;
    
    // Display parameters
    const int PIXEL_SCALE = 4;
    const int WINDOW_WIDTH = GRID_WIDTH * PIXEL_SCALE;
    const int WINDOW_HEIGHT = GRID_HEIGHT * PIXEL_SCALE;
    
    // Create window
    sf::RenderWindow window(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "Plate Capacitor Simulation");
    window.setFramerateLimit(30);
    
    // Create simulator and visualization
    Simulator simulator(GRID_WIDTH, GRID_HEIGHT, PLATE_WIDTH, PLATE_GAP, VOLTAGE);
    Visualization visualization(WINDOW_WIDTH, WINDOW_HEIGHT, PIXEL_SCALE);
    
    // Initialize the simulation
    simulator.initialize();
    
    // Main loop
    bool showPotential = true;
    bool showEquipotential = true;
    bool showElectricField = true;
    int iterations = 0;
    const int MAX_ITERATIONS = 10000;
    const int ITERATIONS_PER_FRAME = 50;
    
    while (window.isOpen()) {
        // Handle events
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            } else if (event.type == sf::Event::KeyPressed) {
                switch (event.key.code) {
                    case sf::Keyboard::Escape:
                        window.close();
                        break;
                    case sf::Keyboard::P:
                        showPotential = !showPotential;
                        break;
                    case sf::Keyboard::E:
                        showEquipotential = !showEquipotential;
                        break;
                    case sf::Keyboard::F:
                        showElectricField = !showElectricField;
                        break;
                    default:
                        break;
                }
            }
        }
    }
}