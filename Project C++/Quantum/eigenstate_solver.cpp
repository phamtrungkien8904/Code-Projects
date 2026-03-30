#include "eigen/Eigen/Dense"

#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using Eigen::MatrixXd;
using Eigen::SelfAdjointEigenSolver;
using Eigen::VectorXd;
using std::cout;
using std::endl;
using std::ofstream;
using std::string;
using std::vector;

static void write_vector_csv(const string& file_name, const vector<double>& data) {
    ofstream file(file_name);
    file << std::setprecision(16);
    for (size_t i = 0; i < data.size(); ++i) {
        file << data[i];
        if (i + 1 < data.size()) {
            file << ',';
        }
    }
    file << '\n';
}

static void write_matrix_csv(const string& file_name, const MatrixXd& matrix) {
    ofstream file(file_name);
    file << std::setprecision(16);
    for (int r = 0; r < matrix.rows(); ++r) {
        for (int c = 0; c < matrix.cols(); ++c) {
            file << matrix(r, c);
            if (c + 1 < matrix.cols()) {
                file << ',';
            }
        }
        file << '\n';
    }
}

int main() {
    const double hbar = 1.0;
    const double m = 1.0;

    const double dx = 0.005;
    const double x_min = -10.0;
    const double x_max = 10.0;

    const int Nx = static_cast<int>((x_max - x_min) / dx);
    vector<double> x(Nx + 1);
    for (int i = 0; i <= Nx; ++i) {
        x[i] = x_min + i * dx;
    }

    const int n_inner = Nx - 1;
    vector<double> x_inner(n_inner);
    vector<double> V(n_inner, 0.0);

    // Semi-harmonic oscillator potential.
    for (int i = 0; i < n_inner; ++i) {
        const double xi = x[i + 1];
        x_inner[i] = xi;

        double Vi = (xi < -1.0) ? 20.0 : 0.0;
        Vi = (xi > -1.0 && xi < 1.0) ? 0.0 : Vi;
        Vi = (xi > 0.0) ? 20.0 * xi * xi : Vi;
        V[i] = Vi;
    }

    const double lamb = hbar * hbar / (2.0 * m * dx * dx);
    MatrixXd H = MatrixXd::Zero(n_inner, n_inner);

    for (int i = 0; i < n_inner; ++i) {
        H(i, i) = 2.0 * lamb + V[i];
        if (i + 1 < n_inner) {
            H(i, i + 1) = -lamb;
            H(i + 1, i) = -lamb;
        }
    }

    SelfAdjointEigenSolver<MatrixXd> solver(H);
    if (solver.info() != Eigen::Success) {
        std::cerr << "Eigenvalue decomposition failed." << endl;
        return 1;
    }

    VectorXd E = solver.eigenvalues();
    MatrixXd psi_cols = solver.eigenvectors();
    MatrixXd psi_rows = psi_cols.transpose();

    vector<double> E_out(E.size());
    for (int i = 0; i < E.size(); ++i) {
        E_out[i] = E(i);
    }

    write_vector_csv("x_inner.csv", x_inner);
    write_vector_csv("potential.csv", V);
    write_vector_csv("eigenvalues.csv", E_out);
    write_matrix_csv("psi.csv", psi_rows);

    cout << "Wrote x_inner.csv, potential.csv, eigenvalues.csv, and psi.csv" << endl;
    return 0;
}
