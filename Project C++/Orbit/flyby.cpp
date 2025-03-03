#include <iostream>
#include <SFML/Graphics.hpp>
#include <cmath>

const int WINDOW_SIZE = 800;
const float AU = 150000000000;
const float SCALE = 100.0f/AU;  // Pixels per simulation unit
const double pi = 3.14159265;
const double GM = 6.67e-11 * 2e30;
const double theta = 1.101; // Mars-Earth Angle
const double dt = 100; // Time interval


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

void planet_motion(State &state, double dt) {
    double r_squared = state.x * state.x + state.y * state.y;
    double r = sqrt(r_squared);
    double ax = -GM * state.x / (r * r * r);
    double ay = -GM * state.y / (r * r * r);

    state.x += state.vx * dt + 0.5 * ax * dt * dt;
    state.y += state.vy * dt + 0.5 * ay * dt * dt;

    double r_new_squared = state.x * state.x + state.y * state.y;
    double r_new = sqrt(r_new_squared);
    double ax_new = -GM * state.x / (r_new * r_new * r_new);
    double ay_new = -GM * state.y / (r_new * r_new * r_new);

    state.vx += 0.5 * (ax + ax_new) * dt;
    state.vy += 0.5 * (ay + ay_new) * dt;
}

void rocket_motion(State &state, State &swinger, double dt) {
    double ratio = 1e-3;
    double r_squared = state.x * state.x + state.y * state.y;
    double r = sqrt(r_squared);
    double distance = sqrt(pow(state.x - swinger.x,2) + pow(state.y - swinger.y,2));
    double ax = -GM * state.x / (r * r * r) - GM*ratio *(state.x - swinger.x)/pow(distance,3);
    double ay = -GM * state.y / (r * r * r) - GM*ratio *(state.y - swinger.y)/pow(distance,3);

    state.x += state.vx * dt + 0.5 * ax * dt * dt;
    state.y += state.vy * dt + 0.5 * ay * dt * dt;

    double r_new_squared = state.x * state.x + state.y * state.y;
    double r_new = sqrt(r_new_squared);
    double distance_new = sqrt(pow(state.x - swinger.x,2) + pow(state.y - swinger.y,2));
    double ax_new = -GM * state.x / (r_new * r_new * r_new) - GM*ratio *(state.x - swinger.x)/pow(distance_new,3);
    double ay_new = -GM * state.y / (r_new * r_new * r_new) - GM*ratio *(state.y - swinger.y)/pow(distance_new,3);

    state.vx += 0.5 * (ax + ax_new) * dt;
    state.vy += 0.5 * (ay + ay_new) * dt;
}

int main() {
    sf::RenderWindow window(sf::VideoMode(WINDOW_SIZE, WINDOW_SIZE), "earth Orbit Simulation");
    window.setFramerateLimit(60*1000);



    // Create objects and initial parameters {x0, y0, vx0, vy0}
    double R1 = 1*AU;
    double v1 = sqrt(GM/R1);
    State earth = {0.0, -R1, v1, 0};
    
    double R2 = 2*AU;
    double v2 = sqrt(GM/R2);
    State mars = {R2*sin(theta), -R2*cos(theta), v2*cos(theta), v2*sin(theta)};

    double R3 = 1*AU;
    double v3 = sqrt(2*GM*(2*AU)/(1*AU*3*AU));
    State rocket = {0.0, -R3, 1.001*v3, 0.0};

    // Create planet (center object)
    sf::CircleShape sun(10);
    sun.setFillColor(sf::Color::Yellow);
    sun.setOrigin(10, 10);
    sun.setPosition(WINDOW_SIZE/2, WINDOW_SIZE/2);

    // Create earth representation
    sf::CircleShape earthShape(3);
    earthShape.setFillColor(sf::Color::Blue);
    earthShape.setOrigin(3, 3);

    // Create earth representation
    sf::CircleShape marsShape(3);
    marsShape.setFillColor(sf::Color::Red);
    marsShape.setOrigin(3, 3);

    // Create earth representation
    sf::CircleShape rocketShape(3);
    rocketShape.setFillColor(sf::Color::White);
    rocketShape.setOrigin(3, 3);





    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Update earth position
        planet_motion(earth, dt);
        planet_motion(mars, dt);
        rocket_motion(rocket, mars, dt);


        // Convert simulation coordinates to screen coordinates
        sf::Vector2f screenPos1 = toScreenCoords(earth.x, earth.y);
        sf::Vector2f screenPos2 = toScreenCoords(mars.x, mars.y);
        sf::Vector2f screenPos3 = toScreenCoords(rocket.x, rocket.y);

        earthShape.setPosition(screenPos1);
        marsShape.setPosition(screenPos2);
        rocketShape.setPosition(screenPos3);
        // Draw frame
        window.clear();
        window.draw(sun);
        window.draw(earthShape);
        window.draw(marsShape);
        window.draw(rocketShape);
        window.display();
    }
    return 0;
}