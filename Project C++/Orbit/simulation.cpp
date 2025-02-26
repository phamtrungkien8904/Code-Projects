#include <SFML/Graphics.hpp>
#include <cmath>

const int WINDOW_SIZE = 800;
const float SCALE = 200.0f;  // Pixels per simulation unit

struct State {
    double x, y;    // Position
    double vx, vy;  // Velocity
};

// Convert simulation coordinates to screen coordinates
sf::Vector2f toScreenCoords(double x, double y) {
    return sf::Vector2f(
        WINDOW_SIZE/2 + x * SCALE,  // Center horizontally
        WINDOW_SIZE/2 - y * SCALE   // Center vertically (SFML y-axis is inverted)
    );
}

void verlet_step(State &state, double dt, double GM) {
    double r_squared = state.x * state.x + state.y * state.y + 1e-9;
    double r = sqrt(r_squared);
    double ax = -GM * state.x / (r * r * r);
    double ay = -GM * state.y / (r * r * r);

    state.x += state.vx * dt + 0.5 * ax * dt * dt;
    state.y += state.vy * dt + 0.5 * ay * dt * dt;

    double r_new_squared = state.x * state.x + state.y * state.y + 1e-9;
    double r_new = sqrt(r_new_squared);
    double ax_new = -GM * state.x / (r_new * r_new * r_new);
    double ay_new = -GM * state.y / (r_new * r_new * r_new);

    state.vx += 0.5 * (ax + ax_new) * dt;
    state.vy += 0.5 * (ay + ay_new) * dt;
}

int main() {
    sf::RenderWindow window(sf::VideoMode(WINDOW_SIZE, WINDOW_SIZE), "Asteroid Orbit Simulation");
    window.setFramerateLimit(60);

    const double GM = 1.0;
    const double dt = 0.01;
    State asteroid = {0.5, 0.0, 0.0, 1.0};

    // Create planet (center object)
    sf::CircleShape planet(10);
    planet.setFillColor(sf::Color::Blue);
    planet.setOrigin(10, 10);
    planet.setPosition(WINDOW_SIZE/2, WINDOW_SIZE/2);

    // Create asteroid representation
    sf::CircleShape asteroidShape(3);
    asteroidShape.setFillColor(sf::Color::White);
    asteroidShape.setOrigin(3, 3);

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Update asteroid position
        verlet_step(asteroid, dt, GM);

        // Convert simulation coordinates to screen coordinates
        sf::Vector2f screenPos = toScreenCoords(asteroid.x, asteroid.y);
        asteroidShape.setPosition(screenPos);

        // Draw frame
        window.clear();
        window.draw(planet);
        window.draw(asteroidShape);
        window.display();
    }

    return 0;
}