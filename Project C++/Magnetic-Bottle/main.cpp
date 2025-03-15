#include <SFML/Graphics.hpp>
#include "Simulation.h"
#include "Renderer.h"

int main()
{
    // Create window with antialiasing
    sf::ContextSettings settings;
    settings.antialiasingLevel = 8;
    sf::RenderWindow window(sf::VideoMode(1200, 800), "Magnetic Bottle Simulation", sf::Style::Default, settings);
    window.setFramerateLimit(60);

    // Initialize simulation and renderer
    Simulation simulation;
    Renderer renderer(&window, &simulation);

    sf::Clock clock;
    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
            
            // Handle key presses for interaction
            if (event.type == sf::Event::KeyPressed)
            {
                // Reset electron
                if (event.key.code == sf::Keyboard::R)
                    simulation.resetElectron();
                
                // Adjust magnetic field strength
                if (event.key.code == sf::Keyboard::Up)
                    simulation.adjustFieldStrength(0.1f);
                if (event.key.code == sf::Keyboard::Down)
                    simulation.adjustFieldStrength(-0.1f);
            }
        }

        // Update simulation
        float dt = clock.restart().asSeconds();
        simulation.update(dt);
        
        // Render
        window.clear(sf::Color(10, 10, 30));
        renderer.render();
        window.display();
    }

    return 0;
}