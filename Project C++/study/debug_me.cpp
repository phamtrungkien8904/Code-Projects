#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <string>
#include <sstream>
#include "Eigen/Dense"

// Funktion zur Definition des Potentials (harmonischer Oszillator)
double potential(double x, double k) {
    return 0.5 * k * x * x;
}

// Funktion zum Lesen der Parameter aus der Eingabedatei
void read_input(const std::string& filename, double& mass, double& k, double& x_min, double& x_max, int& N_points, int& N_eigenvalues) {
    std::ifstream file(filename);
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::string key;
        if (std::getline(iss, key, '=')) {
            double value;
            iss >> value;
            if (key == "mass") mass = value;
            else if (key == "k") k = value;
            else if (key == "x_min") x_min = value;
            else if (key == "x_max") x_max = value;
            else if (key == "N_points") N_points = static_cast<int>(value);
            else if (key == "N_eigenvalues") N_eigenvalues = static_cast<int>(value);
        }
    }
}

int main(int argc, char* argv[]) {
    // Überprüfen, ob die Eingabedatei angegeben wurde
    if (argc != 2) {
        std::cerr << "Verwendung: " << argv[0] << " <input_file>" << std::endl;
        return 1;
    }
    std::string input_file = argv[1];

    // Parameter aus der Eingabedatei lesen
    double mass, k, x_min, x_max;
    int N_points, N_eigenvalues;
    read_input(input_file, mass, k, x_min, x_max, N_points, N_eigenvalues);

    // Diskretisierung des Raums
    std::vector<double> x(N_points);
    double dx = (x_max - x_min) / (N_points - 1);
    for (int i = 0; i < N_points; ++i) {
        x[i] = x_min + i * dx;
    }

    // Aufbau der Hamilton-Matrix
    Eigen::MatrixXd H = Eigen::MatrixXd::Zero(N_points, N_points);
    for (int i = 0; i < N_points; ++i) {
        H(i, i) = potential(x[i], k) + 1.0 / (mass * dx * dx);  // Diagonalelemente
        if (i > 0) H(i, i - 1) = -0.5 / (mass * dx * dx);      // Untere Nebendiagonale
        if (i < N_points - 1) H(i, i + 1) = -0.5 / (mass * dx * dx);  // Obere Nebendiagonale
    }

    // Lösen des Eigenwertproblems
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> solver(H);
    Eigen::VectorXd eigenvalues = solver.eigenvalues();
    Eigen::MatrixXd eigenvectors = solver.eigenvectors();

    // Ausgabe der Eigenwerte auf das Terminal
    std::cout << "Die " << N_eigenvalues << " niedrigsten Eigenwerte sind:" << std::endl;
    for (int i = 0; i < N_eigenvalues; ++i) {
        std::cout << "Eigenwert " << i + 1 << ": " << eigenvalues(i) << std::endl;
    }

    // Schreiben der Eigenwerte in eine Datei
    std::ofstream output_file("eigenvalues.txt");
    output_file << "Eigenwerte:\n";
    for (int i = 0; i < N_eigenvalues; ++i) {
        output_file << "Eigenwert " << i + 1 << ": " << eigenvalues(i) << "\n";
    }
    output_file.close();
    std::cout << "Die Eigenwerte wurden in eigenvalues.txt gespeichert." << std::endl;

    return 0;
}