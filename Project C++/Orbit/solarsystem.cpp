#include <iostream>
#include <SFML/Graphics.hpp>
#include <cmath>
#include <vector>
#include <sstream>
#include <iomanip>

// Global constants
const int WINDOW_SIZE = 800;
const float AU = 150000000000;
const float SCALE = 50.0f/AU;  // Reduced scale to fit outer planets
const double GM = 6.67e-11 * 2e30; // Gravitational constant * mass of central star
const double dt = 100; // Time interval for simulation
const double EARTH_YEAR = 365.25 * 24 * 3600; // Earth year in seconds

// State contains position and velocity
struct State {
    double x, y;
    double vx, vy;
};

class Simulation {
public:
    // Convert simulation coordinates to screen coordinates
    sf::Vector2f toScreenCoords(double x, double y) {
        return sf::Vector2f(
            WINDOW_SIZE/2 + x * SCALE,
            WINDOW_SIZE/2 - y * SCALE
        );
    }
    
    // Update the object's state using a semi-implicit update method
    void planet_motion(State &state, double dt) {
        double r_squared = state.x*state.x + state.y*state.y;
        double r = sqrt(r_squared);
        double ax = -GM * state.x / (r*r*r);
        double ay = -GM * state.y / (r*r*r);
    
        state.x += state.vx * dt + 0.5 * ax * dt * dt;
        state.y += state.vy * dt + 0.5 * ay * dt * dt;
    
        double r_new_squared = state.x*state.x + state.y*state.y;
        double r_new = sqrt(r_new_squared);
        double ax_new = -GM * state.x / (r_new*r_new*r_new);
        double ay_new = -GM * state.y / (r_new*r_new*r_new);
    
        state.vx += 0.5 * (ax + ax_new) * dt;
        state.vy += 0.5 * (ay + ay_new) * dt;
    }
};

class Planet {
public:
    State state;
    sf::CircleShape shape;

    Planet(double x, double y, double vx, double vy, float radius, sf::Color color) {
        state = { x, y, vx, vy };
        shape = sf::CircleShape(radius);
        shape.setFillColor(color);
        shape.setOrigin(radius, radius);
    }
    
    // Update the planet's state and its on-screen position.
    void update(Simulation &sim, double dt) {
        sim.planet_motion(state, dt);
        shape.setPosition(sim.toScreenCoords(state.x, state.y));
    }
};

class SimulationEngine {
private:
    sf::RenderWindow window;
    Simulation sim;
    std::vector<Planet> planets;
    sf::CircleShape sun;
    sf::Font font;
    sf::Text timeText;
    double elapsedTime;
public:
    SimulationEngine() : window(sf::VideoMode(WINDOW_SIZE, WINDOW_SIZE), "Complete Solar System Simulation"), elapsedTime(0) {
        window.setFramerateLimit(60 * 1000);
        // Initialize the sun at the center
        sun = sf::CircleShape(12);
        sun.setFillColor(sf::Color::Yellow);
        sun.setOrigin(12, 12);
        sun.setPosition(WINDOW_SIZE/2, WINDOW_SIZE/2);
        
        // Load font for time display
        if (!font.loadFromFile("arial.ttf")) {
            // If Arial is not available, try a default system font
            if (!font.loadFromFile("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")) {
                std::cerr << "Error loading font. Time won't be displayed." << std::endl;
            }
        }
        
        // Set up time display text
        timeText.setFont(font);
        timeText.setCharacterSize(14);
        timeText.setFillColor(sf::Color::White);
        timeText.setPosition(10, 10);
    }
    
    // Add a planet by specifying its position, velocity, size, and color.
    void addPlanet(double x, double y, double vx, double vy, float radius, sf::Color color) {
        planets.emplace_back(x, y, vx, vy, radius, color);
    }
    
    // Run the simulation: update and render all planets.
    void run(double dt) {
        while (window.isOpen()) {
            sf::Event event;
            while (window.pollEvent(event)) {
                if (event.type == sf::Event::Closed)
                    window.close();
            }
            
            // Update all planets
            for (auto &planet : planets) {
                planet.update(sim, dt);
            }
            
            // Update elapsed time
            elapsedTime += dt;
            
            // Format time as years and days
            double years = elapsedTime / EARTH_YEAR;
            double days = (years - floor(years)) * 365.25;
            std::stringstream ss;
            ss << "Time: " << std::fixed << std::setprecision(0) << floor(years) 
               << " years, " << std::fixed << std::setprecision(1) << days << " days";
            timeText.setString(ss.str());
            
            // Draw frame
            window.clear(sf::Color(10, 10, 40)); // Dark blue background
            window.draw(sun);
            for (auto &planet : planets) {
                window.draw(planet.shape);
            }
            window.draw(timeText);
            window.display();
        }
    }
};

int main() {
    SimulationEngine engine;
    
    // Define orbital parameters for all planets
    // Mercury
    double r_mercury = 0.387 * AU;
    double v_mercury = sqrt(GM / r_mercury);
    engine.addPlanet(r_mercury, 0.0, 0.0, v_mercury, 2, sf::Color(192, 192, 192)); // Gray
    
    // Venus
    double r_venus = 0.723 * AU;
    double v_venus = sqrt(GM / r_venus);
    engine.addPlanet(0.0, r_venus, -v_venus, 0.0, 3.5, sf::Color(255, 198, 73)); // Golden-yellow
    
    // Earth
    double r_earth = 1.0 * AU;
    double v_earth = sqrt(GM / r_earth);
    engine.addPlanet(-r_earth, 0.0, 0.0, -v_earth, 4, sf::Color(0, 0, 255)); // Blue
    
    // Mars
    double r_mars = 1.524 * AU;
    double v_mars = sqrt(GM / r_mars);
    engine.addPlanet(0.0, -r_mars, v_mars, 0.0, 3, sf::Color(255, 0, 0)); // Red
    
    // Jupiter
    double r_jupiter = 5.203 * AU;
    double v_jupiter = sqrt(GM / r_jupiter);
    engine.addPlanet(r_jupiter, 0.0, 0.0, v_jupiter, 7, sf::Color(255, 140, 0)); // Orange
    
    
    engine.run(dt);
    return 0;
}