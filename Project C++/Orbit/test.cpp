#include <iostream>
#include <SFML/Graphics.hpp>
#include <cmath>
#include <vector>
#include <sstream>
#include <iomanip>

// Global constants
// Use the desktop mode for fullscreen
const sf::VideoMode DESKTOP = sf::VideoMode::getDesktopMode();
const int WINDOW_WIDTH = DESKTOP.width;
const int WINDOW_HEIGHT = DESKTOP.height;
const float AU = 150000000000;
const float SCALE = 250.0f/AU;  // Adjusted scale for fullscreen view
const double GM = 6.67e-11 * 2e30; // Gravitational constant * mass of central star
const double dt = 100; // Time interval for simulation
const double EARTH_YEAR = 365.25 * 24 * 3600; // Earth year in seconds
const double PI = 3.1415926535897932384;

// State contains position and velocity
struct State {
    double x, y;
    double vx, vy;
};

class Simulation {
public:
    sf::RenderWindow* windowPtr;
    
    Simulation() : windowPtr(nullptr) {}
    
    // Convert simulation coordinates to screen coordinates
    sf::Vector2f toScreenCoords(double x, double y) {
        if (!windowPtr) {
            // Fallback to constants if window pointer not set
            return sf::Vector2f(
                WINDOW_WIDTH/2 + x * SCALE,
                WINDOW_HEIGHT/2 - y * SCALE
            );
        }
        
        // Use actual window dimensions
        return sf::Vector2f(
            windowPtr->getSize().x/2 + x * SCALE,
            windowPtr->getSize().y/2 - y * SCALE
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
    std::string name;
    
    // Orbit tracking variables
    double initialX, initialY;    // Initial position
    double prevX, prevY;          // Previous position
    double orbitTime;             // Time to complete one orbit
    double timeSinceLastCross;    // Time since crossing initial position
    bool firstCross;              // Flag to skip first crossing (initial condition)
    int orbitsCompleted;          // Counter for completed orbits

    Object(double x, double y, double vx, double vy, float radius, sf::Color color, const std::string& objectName = "") {
        state = { x, y, vx, vy };
        shape = sf::CircleShape(radius);
        shape.setFillColor(color);
        shape.setOrigin(radius, radius);
        name = objectName;
        
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
    
    // Calculate current distance to the sun
    double getDistanceToSun() const {
        return sqrt(state.x * state.x + state.y * state.y);
    }
    
    // Calculate current velocity
    double getVelocity() const {
        return sqrt(state.vx * state.vx + state.vy * state.vy);
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

    // Check if orbit is bound (elliptical) or unbound (parabolic/hyperbolic)
    bool isClosedOrbit() const {
        // Calculate specific orbital energy
        double v_squared = state.vx * state.vx + state.vy * state.vy;
        double r = sqrt(state.x * state.x + state.y * state.y);
        double specificEnergy = 0.5 * v_squared - GM / r;
        
        // If energy < 0, orbit is elliptical (closed)
        // If energy >= 0, orbit is parabolic or hyperbolic (open)
        return specificEnergy < 0;
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
    sf::Text objectInfoText;  // Combined info text for all object data
    double elapsedTime;
public:
    SimulationEngine() : elapsedTime(0) {
        // Get information about monitors
        std::vector<sf::VideoMode> modes = sf::VideoMode::getFullscreenModes();
        
        // First create a non-fullscreen window so we can position it
        window.create(sf::VideoMode(800, 600), "Orbital Simulation");
        
        // Check if there's more than one monitor (simplified approach)
        sf::VideoMode secondScreenMode;
        bool hasSecondScreen = false;
        
        // Try to detect second screen - this is a simple approach
        // that assumes monitors are arranged horizontally
        if (modes.size() > 1) {
            // Assuming second screen is at position (primary_width, 0)
            window.setPosition(sf::Vector2i(DESKTOP.width, 0));
            
            // Get the desktop mode (should be the second screen now)
            secondScreenMode = sf::VideoMode::getDesktopMode();
            hasSecondScreen = true;
        }
        
        // Now recreate the window in fullscreen mode on the second screen if available
        if (hasSecondScreen) {
            window.close();
            window.create(secondScreenMode, "Orbital Simulation", sf::Style::Fullscreen);
        } else {
            // Fallback to primary screen fullscreen
            window.close();
            window.create(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "Orbital Simulation", sf::Style::Fullscreen);
        }
        
        window.setFramerateLimit(60 * 1000);
        
        // Calculate sun size proportional to screen size
        float sunRadius = std::min(window.getSize().x, window.getSize().y) * 0.02;
        
        // Initialize the sun at the center using the actual window size
        sun = sf::CircleShape(sunRadius);
        sun.setFillColor(sf::Color::Yellow);
        sun.setOrigin(sunRadius, sunRadius);
        sun.setPosition(window.getSize().x/2, window.getSize().y/2);
        
        // Load font for time display
        if (!font.loadFromFile("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")) {
            std::cerr << "Failed to load font\n";
        }
        
        // Set up time display text
        timeText.setFont(font);
        timeText.setCharacterSize(20);
        timeText.setFillColor(sf::Color::White);
        timeText.setPosition(20, 20);
        
        // Set up combined object info display text
        objectInfoText.setFont(font);
        objectInfoText.setCharacterSize(18);
        objectInfoText.setFillColor(sf::Color::White);
        objectInfoText.setPosition(20, 60);

        // Set the window pointer in the simulation
        sim.windowPtr = &window;
    }
    
    ~SimulationEngine() {
        // Make sure to close the window when done
        if (window.isOpen()) {
            window.close();
        }
    }
    
    // Add an object by specifying its position, velocity, size, and color.
    void addObject(double x, double y, double vx, double vy, float radius, sf::Color color, const std::string& name = "") {
        objects.emplace_back(x, y, vx, vy, radius, color, name);
    }
    
    // Update the combined object information display (period, distance, velocity)
    void updateObjectInfoDisplay() {
        std::stringstream ss;
        ss << "Object Information:" << std::endl;
        
        for (size_t i = 0; i < objects.size(); ++i) {
            std::string name = objects[i].name.empty() ? "Object " + std::to_string(i + 1) : objects[i].name;
            double period = objects[i].getPeriod();
            double distance = objects[i].getDistanceToSun() / AU;
            double velocity = objects[i].getVelocity() / 1000; // Convert to km/s
            
            // Display object name with its color
            ss << "• " << name << ":" << std::endl;
            
            // Display period information
            ss << "  Period: ";
            if (!objects[i].isClosedOrbit()) {
                ss << "infinity (open orbit)";
            } else if (period > 0.0) {
                ss << std::fixed << std::setprecision(2) << period << " years";
            } else {
                ss << "measuring...";
            }
            ss << std::endl;
            
            // Display distance and velocity
            ss << "  Distance: " << std::fixed << std::setprecision(3) << distance << " AU" << std::endl;
            ss << "  Velocity: " << std::fixed << std::setprecision(2) << velocity << " km/s" << std::endl;
            ss << std::endl;
        }
        
        objectInfoText.setString(ss.str());
    }
    
    // Run the simulation: update and render all objects.
    void run(double dt) {
        while (window.isOpen()) {
            sf::Event event;
            while (window.pollEvent(event)) {
                if (event.type == sf::Event::Closed || 
                    (event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::Escape)) {
                    window.close();
                }
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
            
            // Update combined object information display
            updateObjectInfoDisplay();
            
            // Draw frame
            window.clear(sf::Color(10, 10, 40)); // Dark blue background
            window.draw(sun);
            for (auto &object : objects) {
                window.draw(object.shape);
            }
            window.draw(timeText);
            window.draw(objectInfoText);
            window.display();
        }
    }
};

int main() {
    SimulationEngine engine;

    // Add the Earth
    engine.addObject(0.983 * AU, 0, 0, 29780, 5, sf::Color::Blue, "Earth");

    // Add Mars
    engine.addObject(1.381 * AU, 0, 0, 24100, 3, sf::Color::Red, "Mars");

    // Add Mercury
    engine.addObject(0.387 * AU, 0, 0, 47870, 2, sf::Color(192, 192, 192), "Mercury");
    
    // Add Venus
    engine.addObject(0.723 * AU, 0, 0, 35020, 4, sf::Color(255, 198, 73), "Venus");
    
    // Add a hyperbolic orbit object (escape velocity is sqrt(2)*circular velocity)
    double r_comet = 1.0 * AU;
    double v_escape = sqrt(2.0 * GM / r_comet) * 1.1; // 10% more than escape velocity
    engine.addObject(-r_comet, 0, 0, -v_escape, 2, sf::Color::Green, "Comet");

    engine.run(3*dt);
    return 0;
}