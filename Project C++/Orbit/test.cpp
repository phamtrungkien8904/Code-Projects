#include <iostream>
#include <SFML/Graphics.hpp>
#include <cmath>
#include <vector>
#include <sstream>
#include <iomanip>

// Global constants
const int WINDOW_SIZE = 800;
const float AU = 150000000000;
const float SCALE = 200.0f/AU;  // Reduced scale to fit outer objects
const double GM = 6.67e-11 * 2e30; // Gravitational constant * mass of central star
const double dt = 100; // Time interval for simulation
const double EARTH_YEAR = 365.25 * 24 * 3600; // Earth year in seconds
const double PI = 3.14159265358979323846;

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
    void object_motion(State &state, double dt) {
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

class Object {
public:
    State state;
    sf::CircleShape shape;
    
    // Orbit tracking variables
    double initialX, initialY;    // Initial position
    double prevX, prevY;          // Previous position
    double orbitTime;             // Time to complete one orbit
    double timeSinceLastCross;    // Time since crossing initial position
    bool firstCross;              // Flag to skip first crossing (initial condition)
    int orbitsCompleted;          // Counter for completed orbits

    Object(double x, double y, double vx, double vy, float radius, sf::Color color) {
        state = { x, y, vx, vy };
        shape = sf::CircleShape(radius);
        shape.setFillColor(color);
        shape.setOrigin(radius, radius);
        
        // Initialize orbit tracking
        initialX = x;
        initialY = y;
        prevX = x;
        prevY = y;
        orbitTime = 0.0;
        timeSinceLastCross = 0.0;
        firstCross = true;
        orbitsCompleted = 0;
    }
    
    // Update the object's state and check for orbit completion
    void update(Simulation &sim, double dt) {
        // Store previous position
        prevX = state.x;
        prevY = state.y;
        
        // Update position
        sim.object_motion(state, dt);
        shape.setPosition(sim.toScreenCoords(state.x, state.y));
        
        // Update time tracking
        timeSinceLastCross += dt;
        
        // Check if object has crossed its initial position
        if (hasCompletedOrbit()) {
            if (!firstCross) {
                // Record orbit time when we complete a full orbit
                orbitTime = timeSinceLastCross;
                orbitsCompleted++;
            } else {
                // Skip the first crossing (initial condition)
                firstCross = false;
            }
            timeSinceLastCross = 0.0;
        }
    }
    
    // Check if the object has completed an orbit
    bool hasCompletedOrbit() {
        // If we're too close to origin, don't check
        if (std::abs(prevX) < 0.01 * AU && std::abs(prevY) < 0.01 * AU) {
            return false;
        }
        
        // Calculate angle between initial position vector and current position vector
        double angleInitial = atan2(initialY, initialX);
        double angleCurrent = atan2(state.y, state.x);
        double anglePrev = atan2(prevY, prevX);
        
        // Normalize angles to [0, 2π]
        if (angleInitial < 0) angleInitial += 2 * PI;
        if (angleCurrent < 0) angleCurrent += 2 * PI;
        if (anglePrev < 0) anglePrev += 2 * PI;
        
        // Check if we've crossed the initial angle
        bool crossed = false;
        
        // Case 1: Normal crossing
        if (anglePrev < angleInitial && angleCurrent >= angleInitial) {
            crossed = true;
        }
        // Case 2: Crossing at 0/2π boundary
        else if (anglePrev > angleCurrent && 
                ((anglePrev < angleInitial && 0 <= angleInitial) || 
                 (angleInitial < angleCurrent && angleCurrent <= 2*PI))) {
            crossed = true;
        }
        
        // Additional check: make sure we've moved a significant amount
        if (crossed) {
            // Must have traveled at least 1/3 of orbit before detecting a crossing
            if (timeSinceLastCross > 0.3 * EARTH_YEAR) {
                return true;
            }
        }
        
        return false;
    }
    
    // Get period in Earth years
    double getPeriod() const {
        if (orbitTime > 0.0) {
            return orbitTime / EARTH_YEAR;
        }
        // If we haven't completed an orbit, return 0
        return 0.0;
    }
};

class SimulationEngine {
private:
    sf::RenderWindow window;
    Simulation sim;
    std::vector<Object> objects;
    sf::CircleShape sun;
    sf::Font font;
    sf::Text timeText;
    sf::Text periodText;  // New text for period display
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
        
        // Set up period display text
        periodText.setFont(font);
        periodText.setCharacterSize(14);
        periodText.setFillColor(sf::Color::White);
        periodText.setPosition(10, 40);
    }
    
    // Add an object by specifying its position, velocity, size, and color.
    void addObject(double x, double y, double vx, double vy, float radius, sf::Color color) {
        objects.emplace_back(x, y, vx, vy, radius, color);
    }
    
    // Update the orbital period display
    void updatePeriodDisplay() {
        std::stringstream ss;
        ss << "Orbital Periods (Earth years):" << std::endl;
        
        for (size_t i = 0; i < objects.size(); ++i) {
            double period = objects[i].getPeriod();
            ss << "Object " << (i + 1) << ": ";
            
            if (period > 0.0) {
                ss << std::fixed << std::setprecision(2) << period;
                ss << " (orbits: " << objects[i].orbitsCompleted << ")";
            } else {
                ss << "measuring...";
            }
            ss << std::endl;
        }
        
        periodText.setString(ss.str());
    }
    
    // Run the simulation: update and render all objects.
    void run(double dt) {
        while (window.isOpen()) {
            sf::Event event;
            while (window.pollEvent(event)) {
                if (event.type == sf::Event::Closed)
                    window.close();
            }
            
            // Update all objects
            for (auto &object : objects) {
                object.update(sim, dt);
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
            
            // Update period display
            updatePeriodDisplay();
            
            // Draw frame
            window.clear(sf::Color(10, 10, 40)); // Dark blue background
            window.draw(sun);
            for (auto &object : objects) {
                window.draw(object.shape);
            }
            window.draw(timeText);
            window.draw(periodText);
            window.display();
        }
    }
};

int main() {
    SimulationEngine engine;
    
    // Example object
    double r1 = 1* AU;
    double v1 = sqrt(0.2*GM / r1);
    engine.addObject(r1, 0.0, 0.0, v1, 2, sf::Color(192, 192, 192)); // Gray
    
    engine.run(3*dt);
    return 0;
}