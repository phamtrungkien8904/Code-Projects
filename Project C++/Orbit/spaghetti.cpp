#include <SFML/Graphics.hpp>
#include <vector>
#include <cmath>
#include <cstdlib>

// Simulation constants
const float G = 0.5f;              // Gravitational constant (simulation scale)
const float dt = 0.1f;             // Time step for integration
const float softening = 2.0f;      // Softening factor to prevent singularities

// Increase this factor to enhance the self-gravity between particles
const float stickyFactor = 0.1f;  // 2x stronger self-gravity

// Utility: compute vector length
float length(const sf::Vector2f &v) {
    return std::sqrt(v.x * v.x + v.y * v.y);
}

// Utility: normalize a vector
sf::Vector2f normalize(const sf::Vector2f &v) {
    float len = length(v);
    return (len != 0) ? sf::Vector2f(v.x / len, v.y / len) : sf::Vector2f(0, 0);
}

// Particle representing a constituent of the star
struct Particle {
    sf::Vector2f pos;
    sf::Vector2f vel;
    float mass;
    Particle(const sf::Vector2f &position, const sf::Vector2f &velocity, float m)
        : pos(position), vel(velocity), mass(m) {}
};

int main() {
    const int windowWidth = 800, windowHeight = 600;
    sf::RenderWindow window(sf::VideoMode(windowWidth, windowHeight), "Spaghettification Simulation");

    // ----- Set Up Render Texture for Background Stars -----
    sf::RenderTexture backgroundTexture;
    if (!backgroundTexture.create(windowWidth, windowHeight)) {
        return -1; // error handling
    }
    
    // Create a SFML shader for gravitational lens effect
    const std::string lensFragmentShader = R"(
        uniform sampler2D texture;
        uniform vec2 blackHolePos;      // normalized coordinates (0..1)
        uniform float eventHorizon;     // normalized radius of the event horizon
        uniform float lensRange;        // normalized width of the lensing annulus
        uniform float lensStrength;     // distortion strength

        void main()
        {
            vec2 uv = gl_TexCoord[0].xy;
            vec2 offset = uv - blackHolePos;
            float dist = length(offset);
            if(dist < eventHorizon) {
                // Inside event horizon: always black
                gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
            } else if(dist < eventHorizon + lensRange) {
                // Lensing applied only in a narrow annulus outside event horizon
                float factor = 1.0 + lensStrength * (eventHorizon + lensRange - dist) / lensRange;
                vec2 uv_new = blackHolePos + offset * factor;
                gl_FragColor = texture2D(texture, uv_new);
            } else {
                // Outside the effect region, show texture normally
                gl_FragColor = texture2D(texture, uv);
            }
        }
    )";
    
    sf::Shader lensShader;
    if (!lensShader.loadFromMemory(lensFragmentShader, sf::Shader::Fragment)) {
        return -1; // error handling
    }
    
    // ----- Define the Black Hole -----
    sf::Vector2f blackHolePos(windowWidth / 2.0f, windowHeight / 2.0f);
    float blackHoleMass = 1000.0f;  // Massive black hole for strong gravity

    // ----- Define the Star with High-Eccentricity Elliptical Orbit -----
    // Place the star's center at a position far from the black hole (apastron)
    sf::Vector2f starCenter(windowWidth / 2.0f, windowHeight / 2.0f - 300);
    sf::Vector2f offset = starCenter - blackHolePos;
    float distance = length(offset);
    // Calculate the circular orbital speed at this distance
    float orbitalSpeed = std::sqrt(G * blackHoleMass / distance);
    // Scale down the speed to produce a high-eccentricity elliptical orbit
    float eccentricityFactor = 0.7f; // Factor < 1 produces an elliptical orbit with low speed at apastron
    // Determine the perpendicular direction to the radius vector for the initial velocity
    sf::Vector2f orbitalDirection(-offset.y, offset.x);
    orbitalDirection = normalize(orbitalDirection);
    sf::Vector2f starVelocity = orbitalSpeed * eccentricityFactor * orbitalDirection;

    // ----- Create Particles Representing the Star -----
    std::vector<Particle> particles;
    // Increase starRadius for a larger star
    const float starRadius = 10.0f;
    const int numParticles = 600;

    for (int i = 0; i < numParticles; i++) {
        // Use sqrt to bias the random radius so more particles cluster near the center,
        // resulting in a rounder, more cohesive star.
        float randomR = starRadius * std::sqrt((float)std::rand() / RAND_MAX);
        float randomAngle = ((float)std::rand() / RAND_MAX) * 2 * 3.14159f;
        sf::Vector2f posOffset(randomR * std::cos(randomAngle), randomR * std::sin(randomAngle));
        sf::Vector2f pos = starCenter + posOffset;
        // All particles share the initial orbital velocity
        sf::Vector2f vel = starVelocity;
        // Increase particle mass to enhance self-gravity (and help them stick together)
        particles.push_back(Particle(pos, vel, 2.0f));
    }

    // ----- Prepare SFML Drawing Objects -----
    sf::CircleShape blackHoleShape(10);
    blackHoleShape.setFillColor(sf::Color::Black);
    blackHoleShape.setOrigin(10, 10);

    std::vector<sf::CircleShape> particleShapes(numParticles);
    for (int i = 0; i < numParticles; i++) {
        // Previously radius was 2, now set to 1 for smaller size
        particleShapes[i].setRadius(1);
        particleShapes[i].setFillColor(sf::Color(255, 220, 200));
        particleShapes[i].setOrigin(1, 1); // Adjust origin accordingly
    }

    std::vector<sf::CircleShape> accretionDiskShapes;  // Holds particles that form the disk

    // ----- Generate Background Stars -----
    const int numBackgroundStars = 1200;
    std::vector<sf::CircleShape> backgroundStars;
    for (int i = 0; i < numBackgroundStars; i++) {
        sf::CircleShape star(1);  // Small star
        // Use a white color but faded
        star.setFillColor(sf::Color(255, 255, 255, 100));
        float x = static_cast<float>(std::rand() % windowWidth);
        float y = static_cast<float>(std::rand() % windowHeight);
        star.setPosition(x, y);
        backgroundStars.push_back(star);
    }

    // ----- Main Simulation Loop -----
    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        
        // Compute forces on each particle
        std::vector<sf::Vector2f> forces(particles.size(), sf::Vector2f(0, 0));
        
        // Gravitational force from the black hole on each particle
        for (size_t i = 0; i < particles.size(); i++) {
            sf::Vector2f diff = blackHolePos - particles[i].pos;
            float r = length(diff);
            float forceMag = (G * blackHoleMass * particles[i].mass) / ((r * r) + softening * softening);
            forces[i] += forceMag * normalize(diff);
        }
        
        // Self-gravity: compute gravitational interactions among star particles
        for (size_t i = 0; i < particles.size(); i++) {
            for (size_t j = i + 1; j < particles.size(); j++) {
                sf::Vector2f diff = particles[j].pos - particles[i].pos;
                float r = length(diff);
                float forceMag = (G * stickyFactor * particles[i].mass * particles[j].mass) / ((r * r) + softening * softening);
                sf::Vector2f force = forceMag * normalize(diff);
                forces[i] += force;
                forces[j] -= force;  // Newton's third law
            }
        }
        
        // Update particle velocities and positions using Euler integration
        for (size_t i = 0; i < particles.size(); i++) {
            sf::Vector2f acceleration = forces[i] / particles[i].mass;
            particles[i].vel += acceleration * dt;
            particles[i].pos += particles[i].vel * dt;
        }
        
        // ----- Collision Resolution: Prevent Particles from Overlapping -----
        // Define the minimum allowed distance between particles (each particle is drawn with radius 2)
        const float minDist = 4.0f;  // Diameter of two particles
        for (size_t i = 0; i < particles.size(); i++) {
            for (size_t j = i + 1; j < particles.size(); j++) {
                sf::Vector2f diff = particles[j].pos - particles[i].pos;
                float r = length(diff);
                if (r < minDist && r != 0) {
                    // Calculate the overlap amount
                    float overlap = 0.5f * (minDist - r);
                    // Determine the normalized direction vector
                    sf::Vector2f normal = diff / r;
                    // Push the particles apart proportionally
                    particles[i].pos -= overlap * normal;
                    particles[j].pos += overlap * normal;

                    // Optional: Adjust velocities for a simple elastic collision response.
                    float v1n = particles[i].vel.x * normal.x + particles[i].vel.y * normal.y;
                    float v2n = particles[j].vel.x * normal.x + particles[j].vel.y * normal.y;
                    // Swap the normal components
                    float temp = v1n;
                    v1n = v2n;
                    v2n = temp;
                    // Update velocities along the normal direction
                    particles[i].vel += (v1n - (particles[i].vel.x * normal.x + particles[i].vel.y * normal.y)) * normal;
                    particles[j].vel += (v2n - (particles[j].vel.x * normal.x + particles[j].vel.y * normal.y)) * normal;
                }
            }
        }
        
        // Remove particles that have fallen into the black hole (inside the event horizon)
        const float eventHorizon = 20.0f;
        const float diskWidth = 10.0f;  // Spread the disk particles from eventHorizon to eventHorizon + diskWidth
        for (int i = particles.size() - 1; i >= 0; i--) {
            sf::Vector2f diff = particles[i].pos - blackHolePos;
            if (length(diff) < eventHorizon) {
                // Create an accretion disk particle with a smaller radius
                sf::CircleShape diskParticle(1);  // Smaller size than before (was 2)
                diskParticle.setFillColor(sf::Color(255, 140, 0, 200)); // Warm orange

                // Get a normalized direction and add a random offset within the diskWidth
                sf::Vector2f dir = normalize(diff);
                float randomOffset = ((float)std::rand() / RAND_MAX) * diskWidth;
                diskParticle.setPosition(blackHolePos + dir * (eventHorizon + randomOffset));
                diskParticle.setOrigin(1, 1);
                accretionDiskShapes.push_back(diskParticle);

                // Remove particle from simulation
                particles.erase(particles.begin() + i);
                particleShapes.erase(particleShapes.begin() + i);
            }
        }

        // Rotate accretion disk particles around the black hole
        for (auto &shape : accretionDiskShapes) {
            // Compute current offset from the black hole
            sf::Vector2f offset = shape.getPosition() - blackHolePos;
            // Rotate by a small angle (adjust as needed)
            float angle = 0.01f;  // in radians
            float cosA = std::cos(angle);
            float sinA = std::sin(angle);
            sf::Vector2f rotatedOffset(offset.x * cosA - offset.y * sinA,
                                        offset.x * sinA + offset.y * cosA);
            shape.setPosition(blackHolePos + rotatedOffset);
        }

        // ----- Render the Scene -----
        window.clear(sf::Color::Black);  // Clear window

        // Render background stars to the render texture
        backgroundTexture.clear(sf::Color::Black);
        for (const auto &star : backgroundStars) {
            backgroundTexture.draw(star);
        }
        backgroundTexture.display();

        // Set shader uniforms (using normalized coordinates)
        lensShader.setUniform("blackHolePos", sf::Glsl::Vec2(blackHolePos.x / windowWidth, blackHolePos.y / windowHeight));
        lensShader.setUniform("eventHorizon", 20.0f / windowWidth); // normalized event horizon radius
        // Use a narrow annular range (for example, 10 pixels normalized)
        lensShader.setUniform("lensRange", 10.0f / windowWidth);
        lensShader.setUniform("lensStrength", 0.2f); // Lower distortion for clarity

        // Draw the background texture with the lens shader applied
        sf::Sprite backgroundSprite(backgroundTexture.getTexture());
        window.draw(backgroundSprite, &lensShader);

        // Draw a black mask over the event horizon so that no stars show inside
        sf::CircleShape eventHorizonMask(20.0f);  // 20.0f matches the event horizon radius
        eventHorizonMask.setOrigin(20.0f, 20.0f);
        eventHorizonMask.setFillColor(sf::Color::Black);
        eventHorizonMask.setPosition(blackHolePos);
        window.draw(eventHorizonMask);

        // Draw the black hole core (optionally with an energy disk around its border)
        blackHoleShape.setPosition(blackHolePos);
        window.draw(blackHoleShape);

        // Draw each remaining particle (star components)
        for (size_t i = 0; i < particles.size(); i++) {
            particleShapes[i].setPosition(particles[i].pos);
            window.draw(particleShapes[i]);
        }

        // Draw the accretion disk particles
        for (const auto &diskParticle : accretionDiskShapes) {
            window.draw(diskParticle);
        }

        window.display();
    }
    
    return 0;
}
