#include "simulator.h"
#include <cmath>
#include <algorithm>

Simulator::Simulator(int width, int height, int plateWidth, int plateGap, double voltage)
    : m_width(width), m_height(height), m_plateWidth(plateWidth), m_plateGap(plateGap),
      m_voltage(voltage), m_maxPotential(voltage), m_minPotential(-voltage), m_maxFieldStrength(0.0)
{
    // Initialize grids
    m_potential.resize(width, std::vector<double>(height, 0.0));
    m_electricField.resize(width, std::vector<std::pair<double, double>>(height, {0.0, 0.0}));
}

void Simulator::initialize() {
    // Calculate positions for the plates
    int centerY = m_height / 2;
    int topPlateY = centerY - m_plateGap / 2;
    int bottomPlateY = centerY + m_plateGap / 2;
    int plateStartX = (m_width - m_plateWidth) / 2;
    int plateEndX = plateStartX + m_plateWidth;
    
    // Set boundary conditions (fixed potentials at the plates)
    for (int x = plateStartX; x < plateEndX; ++x) {
        // Top plate (positive potential)
        if (topPlateY >= 0) {
            m_potential[x][topPlateY] = m_voltage / 2;
        }
        
        // Bottom plate (negative potential)
        if (bottomPlateY < m_height) {
            m_potential[x][bottomPlateY] = -m_voltage / 2;
        }
    }
}

void Simulator::solve(int iterations) {
    // Array to keep track of boundary points (plates) that shouldn't change
    std::vector<std::vector<bool>> isBoundary(m_width, std::vector<bool>(m_height, false));
    
    // Mark boundary points
    int centerY = m_height / 2;
    int topPlateY = centerY - m_plateGap / 2;
    int bottomPlateY = centerY + m_plateGap / 2;
    int plateStartX = (m_width - m_plateWidth) / 2;
    int plateEndX = plateStartX + m_plateWidth;
    
    for (int x = plateStartX; x < plateEndX; ++x) {
        if (topPlateY >= 0) {
            isBoundary[x][topPlateY] = true;
        }
        if (bottomPlateY < m_height) {
            isBoundary[x][bottomPlateY] = true;
        }
    }
    
    // Iterative solution of Laplace's equation
    for (int iter = 0; iter < iterations; ++iter) {
        for (int x = 1; x < m_width - 1; ++x) {
            for (int y = 1; y < m_height - 1; ++y) {
                // Skip boundary points
                if (isBoundary[x][y]) continue;
                
                // Update potential at each point (average of neighbors)
                m_potential[x][y] = 0.25 * (
                    m_potential[x+1][y] + m_potential[x-1][y] +
                    m_potential[x][y+1] + m_potential[x][y-1]
                );
            }
        }
    }
    
    // Update min/max potential values for visualization
    m_maxPotential = m_voltage / 2;
    m_minPotential = -m_voltage / 2;
}

void Simulator::calculateElectricField() {
    m_maxFieldStrength = 0.0;
    
    // Calculate the electric field as the negative gradient of the potential
    for (int x = 1; x < m_width - 1; ++x) {
        for (int y = 1; y < m_height - 1; ++y) {
            // Central difference for gradient (Ex = -dV/dx, Ey = -dV/dy)
            double Ex = -(m_potential[x+1][y] - m_potential[x-1][y]) / 2.0;
            double Ey = -(m_potential[x][y+1] - m_potential[x][y-1]) / 2.0;
            
            // Store the field components
            m_electricField[x][y] = {Ex, Ey};
            
            // Calculate field strength and update max value
            double fieldStrength = std::sqrt(Ex*Ex + Ey*Ey);
            m_maxFieldStrength = std::max(m_maxFieldStrength, fieldStrength);
        }
    }
}

const std::vector<std::vector<double>>& Simulator::getPotential() const {
    return m_potential;
}

const std::vector<std::vector<std::pair<double, double>>>& Simulator::getElectricField() const {
    return m_electricField;
}

double Simulator::getMaxPotential() const {
    return m_maxPotential;
}

double Simulator::getMinPotential() const {
    return m_minPotential;
}

double Simulator::getMaxFieldStrength() const {
    return m_maxFieldStrength;
}