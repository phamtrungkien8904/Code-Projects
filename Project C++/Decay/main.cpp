#include <SFML/Graphics.hpp>
#include <vector>
#include <random>
#include <cmath>
#include <iostream>
#include <sstream>
#include <iomanip>

// Constants for simulation
const int WINDOW_WIDTH = 1200;
const int WINDOW_HEIGHT = 800;
const int SIMULATION_WIDTH = 800;
const int GRAPH_WIDTH = 400;
const int PARTICLE_COUNT = 500;
const float DEFAULT_HALFLIFE = 5.0f; // seconds
const float SIMULATION_TIME = 30.0f; // seconds to display on graph

// Particle class
class Particle {
private:
    sf::Vector2f position;
    bool isTypeA; // true = A (red), false = B (blue)
    float decayProbability;
    float creationTime;

public:
    Particle(sf::Vector2f pos, float halfLife, float currentTime) 
        : position(pos), isTypeA(true), creationTime(currentTime) {
        // Calculate per-frame decay probability from half-life (in seconds)
        // P = 1 - exp(ln(0.5) * dt / T)
        decayProbability = 1.0f - std::pow(0.5f, 1.0f / (halfLife * 60.0f)); // assuming 60 fps
    }

    void update(float currentTime, std::mt19937& rng) {
        // Random movement
        std::uniform_real_distribution<float> dist(-0.5f, 0.5f);
        position.x += dist(rng);
        position.y += dist(rng);

        // Contain within simulation area
        if (position.x < 0) position.x = 0;
        if (position.x > SIMULATION_WIDTH) position.x = SIMULATION_WIDTH;
        if (position.y < 0) position.y = 0;
        if (position.y > WINDOW_HEIGHT) position.y = WINDOW_HEIGHT;

        // Check for decay (only if still type A)
        if (isTypeA) {
            std::uniform_real_distribution<float> decayDist(0.0f, 1.0f);
            if (decayDist(rng) < decayProbability) {
                isTypeA = false; // Decay from A to B
            }
        }
    }

    void draw(sf::RenderWindow& window) const {
        sf::CircleShape shape(4.0f);
        shape.setPosition(position);
        shape.setOrigin(4.0f, 4.0f);
        
        // Type A is red, Type B is blue
        if (isTypeA) {
            shape.setFillColor(sf::Color::Red);
        } else {
            shape.setFillColor(sf::Color::Blue);
        }
        
        window.draw(shape);
    }

    bool isA() const { return isTypeA; }
    float getCreationTime() const { return creationTime; }
    sf::Vector2f getPosition() const { return position; }
};

// Graph class to display decay curve
class DecayGraph {
private:
    std::vector<float> dataPoints;
    sf::VertexArray graphLine;
    sf::VertexArray axes;
    sf::Font font;
    sf::Text title;
    sf::Text xAxisLabel;
    sf::Text yAxisLabel;
    sf::Text halfLifeText;
    float maxTime;
    int maxParticles;

public:
    DecayGraph(float simulationTime, int particleCount) 
        : maxTime(simulationTime), maxParticles(particleCount) {
        
        // Initialize with empty data
        graphLine.setPrimitiveType(sf::LinesStrip);
        
        // Set up axes
        axes.setPrimitiveType(sf::Lines);
        
        // X-axis
        axes.append(sf::Vertex(sf::Vector2f(SIMULATION_WIDTH + 50, WINDOW_HEIGHT - 50), sf::Color::White));
        axes.append(sf::Vertex(sf::Vector2f(WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50), sf::Color::White));
        
        // Y-axis
        axes.append(sf::Vertex(sf::Vector2f(SIMULATION_WIDTH + 50, 50), sf::Color::White));
        axes.append(sf::Vertex(sf::Vector2f(SIMULATION_WIDTH + 50, WINDOW_HEIGHT - 50), sf::Color::White));
        
        // Load font
        if (!font.loadFromFile("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")) {
            std::cerr << "Error loading font!" << std::endl;
        }
        
        // Set up text elements
        title.setFont(font);
        title.setString("A Particles Remaining vs Time");
        title.setCharacterSize(18);
        title.setFillColor(sf::Color::White);
        title.setPosition(SIMULATION_WIDTH + 100, 10);
        
        xAxisLabel.setFont(font);
        xAxisLabel.setString("Time (s)");
        xAxisLabel.setCharacterSize(14);
        xAxisLabel.setFillColor(sf::Color::White);
        xAxisLabel.setPosition(WINDOW_WIDTH - 100, WINDOW_HEIGHT - 30);
        
        yAxisLabel.setFont(font);
        yAxisLabel.setString("A Particles");
        yAxisLabel.setCharacterSize(14);
        yAxisLabel.setFillColor(sf::Color::White);
        yAxisLabel.setPosition(SIMULATION_WIDTH + 10, 50);
        
        halfLifeText.setFont(font);
        halfLifeText.setCharacterSize(14);
        halfLifeText.setFillColor(sf::Color::Yellow);
        halfLifeText.setPosition(SIMULATION_WIDTH + 50, 400);
    }
    
    void updateHalfLifeText(float halfLife) {
        std::stringstream ss;
        ss << "Half-life: " << halfLife << " seconds";
        halfLifeText.setString(ss.str());
    }

    void update(float currentTime, int remainingAParticles) {
        // Store the data point
        if (currentTime <= maxTime) {
            dataPoints.push_back(remainingAParticles);
            
            // Update the graph line
            graphLine.clear();
            
            float xScale = (GRAPH_WIDTH - 100) / maxTime;
            float yScale = (WINDOW_HEIGHT - 100) / (float)maxParticles;
            
            for (size_t i = 0; i < dataPoints.size(); i++) {
                float x = SIMULATION_WIDTH + 50 + (i * currentTime / dataPoints.size()) * xScale;
                float y = WINDOW_HEIGHT - 50 - dataPoints[i] * yScale;
                graphLine.append(sf::Vertex(sf::Vector2f(x, y), sf::Color::Green));
            }
        }
    }

    void draw(sf::RenderWindow& window) {
        window.draw(axes);
        window.draw(graphLine);
        window.draw(title);
        window.draw(xAxisLabel);
        window.draw(yAxisLabel);
        window.draw(halfLifeText);
        
        // Draw tick marks and labels for X-axis
        for (int i = 0; i <= 5; i++) {
            float x = SIMULATION_WIDTH + 50 + i * (GRAPH_WIDTH - 100) / 5;
            float timeValue = i * maxTime / 5;
            
            // Tick mark
            sf::VertexArray tick(sf::Lines, 2);
            tick[0].position = sf::Vector2f(x, WINDOW_HEIGHT - 50);
            tick[1].position = sf::Vector2f(x, WINDOW_HEIGHT - 45);
            tick[0].color = tick[1].color = sf::Color::White;
            window.draw(tick);
            
            // Tick label
            sf::Text tickLabel;
            tickLabel.setFont(font);
            std::stringstream ss;
            ss << timeValue;
            tickLabel.setString(ss.str());
            tickLabel.setCharacterSize(12);
            tickLabel.setFillColor(sf::Color::White);
            tickLabel.setPosition(x - 5, WINDOW_HEIGHT - 40);
            window.draw(tickLabel);
        }
        
        // Draw tick marks and labels for Y-axis
        for (int i = 0; i <= 5; i++) {
            float y = WINDOW_HEIGHT - 50 - i * (WINDOW_HEIGHT - 100) / 5;
            int particleCount = i * maxParticles / 5;
            
            // Tick mark
            sf::VertexArray tick(sf::Lines, 2);
            tick[0].position = sf::Vector2f(SIMULATION_WIDTH + 50, y);
            tick[1].position = sf::Vector2f(SIMULATION_WIDTH + 45, y);
            tick[0].color = tick[1].color = sf::Color::White;
            window.draw(tick);
            
            // Tick label
            sf::Text tickLabel;
            tickLabel.setFont(font);
            std::stringstream ss;
            ss << particleCount;
            tickLabel.setString(ss.str());
            tickLabel.setCharacterSize(12);
            tickLabel.setFillColor(sf::Color::White);
            tickLabel.setPosition(SIMULATION_WIDTH + 20, y - 6);
            window.draw(tickLabel);
        }
        
        // Draw the theoretical decay curve
        sf::VertexArray theoreticalCurve(sf::LinesStrip);
        float xScale = (GRAPH_WIDTH - 100) / maxTime;
        float yScale = (WINDOW_HEIGHT - 100) / (float)maxParticles;
        
        for (int i = 0; i <= 100; i++) {
            float t = i * maxTime / 100.0f;
            float x = SIMULATION_WIDTH + 50 + t * xScale;
            float y = WINDOW_HEIGHT - 50 - maxParticles * std::pow(0.5f, t / DEFAULT_HALFLIFE) * yScale;
            theoreticalCurve.append(sf::Vertex(sf::Vector2f(x, y), sf::Color(255, 255, 0, 100)));
        }
        
        window.draw(theoreticalCurve);
    }
};

int main() {
    // Create the window
    sf::RenderWindow window(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "Radioactive Decay Simulation");
    window.setFramerateLimit(60);
    
    // Set up random number generator
    std::random_device rd;
    std::mt19937 rng(rd());
    std::uniform_real_distribution<float> distX(0.0f, SIMULATION_WIDTH);
    std::uniform_real_distribution<float> distY(0.0f, WINDOW_HEIGHT);
    
    // Create particles
    std::vector<Particle> particles;
    
    for (int i = 0; i < PARTICLE_COUNT; i++) {
        particles.emplace_back(sf::Vector2f(distX(rng), distY(rng)), DEFAULT_HALFLIFE, 0.0f);
    }
    
    // Create graph
    DecayGraph graph(SIMULATION_TIME, PARTICLE_COUNT);
    graph.updateHalfLifeText(DEFAULT_HALFLIFE);
    
    // Simulation clock
    sf::Clock clock;
    
    // Main game loop
    while (window.isOpen()) {
        // Process events
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
        }
        
        // Update simulation
        float currentTime = clock.getElapsedTime().asSeconds();
        
        for (auto& particle : particles) {
            particle.update(currentTime, rng);
        }
        
        // Count type A particles
        int aParticlesCount = 0;
        for (const auto& particle : particles) {
            if (particle.isA()) {
                aParticlesCount++;
            }
        }
        
        // Update graph
        graph.update(currentTime, aParticlesCount);
        
        // Clear the window
        window.clear(sf::Color(20, 20, 20));
        
        // Draw separator line
        sf::VertexArray separator(sf::Lines, 2);
        separator[0].position = sf::Vector2f(SIMULATION_WIDTH, 0);
        separator[1].position = sf::Vector2f(SIMULATION_WIDTH, WINDOW_HEIGHT);
        separator[0].color = separator[1].color = sf::Color(100, 100, 100);
        window.draw(separator);
        
        // Draw particles
        for (const auto& particle : particles) {
            particle.draw(window);
        }
        
        // Draw graph
        graph.draw(window);
        
        // Display remaining particles count
        sf::Font font;
        if (font.loadFromFile("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")) {
            sf::Text countText;
            countText.setFont(font);
            std::stringstream ss;
            ss << "A Particles: " << aParticlesCount << " / " << PARTICLE_COUNT;
            countText.setString(ss.str());
            countText.setCharacterSize(18);
            countText.setFillColor(sf::Color::White);
            countText.setPosition(20, 20);
            window.draw(countText);
            
            // Display elapsed time
            sf::Text timeText;
            timeText.setFont(font);
            ss.str("");
            ss << "Time: " << std::fixed << std::setprecision(1) << currentTime << "s";
            timeText.setString(ss.str());
            timeText.setCharacterSize(18);
            timeText.setFillColor(sf::Color::White);
            timeText.setPosition(20, 50);
            window.draw(timeText);
        }
        
        // Display the window
        window.display();
    }
    
    return 0;
}