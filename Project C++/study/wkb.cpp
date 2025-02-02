#include <iostream>
#include <cmath>
#include <vector>
#include <fstream>

const double hbar = 1.0545718e-34;
const double m = 9.10938356e-31;

double wkb_tunneling(double V0, double a, double E) {
    if (E >= V0) {
        return 1.0;
    }
    double kappa = sqrt(2 * m * (V0 - E)) / hbar;
    double exponent = -2 * kappa * a;
    return exp(exponent);
}

int main() {
    double V0 = 5.0;
    double a = 1e-9;
    V0 *= 1.60218e-19;
    int num_points = 100;
    std::vector<double> energies;
    std::vector<double> probabilities;
    for (int i = 0; i <= num_points; ++i) {
        double E = (i / static_cast<double>(num_points)) * V0;
        energies.push_back(E);
        probabilities.push_back(wkb_tunneling(V0, a, E));
    }
    std::ofstream output("wkb_tunneling.dat");
    if (output.is_open()) {
        for (size_t i = 0; i < energies.size(); ++i) {
            output << energies[i] / 1.60218e-19 << " " << probabilities[i] << "\n";
        }
        output.close();
        std::cout << "Ergebnisse gespeichert in 'wkb_tunneling.dat'." << std::endl;
    } else {
        std::cerr << "Fehler beim Oeffnen der Datei." << std::endl;
    }
    return 0;
}