#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <cmath>
#include <iostream>

// Constants
const float PI = 3.14159265358979323846f;
const float DEG_TO_RAD = PI / 180.0f;
const float RAD_TO_DEG = 180.0f / PI;

// Physics parameters
const float bead_mass = 1.0f;   // Mass of the bead
const float rod_mass = 5.0f;    // Mass of the rod
const float rod_length = 200.0f; // Length of the rod
const float initial_velocity = 300.0f; // Initial velocity of the bead
const float impact_point = 0.5f; // Impact point as a fraction of the rod length (0.0 to 1.0)

// Simulation parameters
const float delta_time = 0.01f; // Time step for the simulation

struct Bead {
    sf::CircleShape shape;
    sf::Vector2f velocity;
};

struct Rod {
    sf::RectangleShape shape;
    float angular_velocity;
    float angle;
};

void initialize(Bead& bead, Rod& rod, const sf::Vector2f& window_center) {
    // Initialize bead
    bead.shape.setRadius(10.0f);
    bead.shape.setFillColor(sf::Color::Red);
    bead.velocity = sf::Vector2f(initial_velocity, 0.0f);
    bead.shape.setPosition(window_center.x - rod_length / 2.0f, window_center.y);

    // Initialize rod
    rod.shape.setSize(sf::Vector2f(rod_length, 10.0f));
    rod.shape.setFillColor(sf::Color::Blue);
    rod.angular_velocity = 0.0f;
    rod.angle = 0.0f;
    rod.shape.setOrigin(rod_length / 2.0f, 5.0f);
    rod.shape.setPosition(window_center);
}

void update(Bead& bead, Rod& rod) {
    // Update bead position
    bead.shape.move(bead.velocity * delta_time);

    // Check for collision
    sf::Vector2f bead_position = bead.shape.getPosition();
    sf::Vector2f rod_position = rod.shape.getPosition();
    float relative_position = (bead_position.x - (rod_position.x - rod_length / 2.0f)) / rod_length;

    if (relative_position >= 0.0f && relative_position <= 1.0f) {
        // Calculate new velocities after elastic collision
        float collision_point = relative_position * rod_length;
        float rod_moi = rod_mass * rod_length * rod_length / 12.0f; // Moment of inertia

        float rod_impact_velocity = rod.angular_velocity * collision_point;
        float total_mass = bead_mass + rod_mass;
        float impulse = 2.0f * (bead.velocity.x - rod_impact_velocity) / (total_mass * collision_point);

        bead.velocity.x -= impulse * rod_mass / bead_mass;
        rod.angular_velocity += impulse * bead_mass * collision_point / rod_moi;

        // Move bead out of collision
        bead.shape.setPosition(bead_position.x + bead.velocity.x * delta_time, bead_position.y);
    }

    // Update rod angle
    rod.angle += rod.angular_velocity * delta_time * RAD_TO_DEG;
    rod.shape.setRotation(rod.angle);
}

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Physics Simulation");
    window.setFramerateLimit(6000);

    sf::Vector2f window_center(window.getSize().x / 2.0f, window.getSize().y / 2.0f);

    Bead bead;
    Rod rod;
    initialize(bead, rod, window_center);

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
        }

        update(bead, rod);

        window.clear(sf::Color::White);
        window.draw(bead.shape);
        window.draw(rod.shape);
        window.display();
    }

    return 0;
}