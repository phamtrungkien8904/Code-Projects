#pragma once

#include <vector>
#include <utility>

class Simulator {
public:
    // Constructor with grid dimensions and plate capacitor parameters
    Simulator(int width, int height, int plateWidth, int plateGap, double voltage);
    
    // Initialize the potential grid with boundary conditions
    void initialize();
    
    // Run Laplace equation solver for a number of iterations
    void solve(int iterations);
    
    // Calculate the electric field from the potential
    void calculateElectricField();
    
    // Getters for the simulation data
    const std::vector<std::vector<double>>& getPotential() const;
    const std::vector<std::vector<std::pair<double, double>>>& getElectricField() const;
    
    // Get min and max values for visualization scaling
    double getMaxPotential() const;
    double getMinPotential() const;
    double getMaxFieldStrength() const;

private:
    int m_width;            // Grid width
    int m_height;           // Grid height
    int m_plateWidth;       // Width of the capacitor plates
    int m_plateGap;         // Gap between the plates
    double m_voltage;       // Voltage between plates
    
    // Grid for the electric potential
    std::vector<std::vector<double>> m_potential;
    
    // Grid for the electric field (x and y components)
    std::vector<std::vector<std::pair<double, double>>> m_electricField;
    
    // Min/max values for visualization scaling
    double m_maxPotential;
    double m_minPotential;
    double m_maxFieldStrength;
};