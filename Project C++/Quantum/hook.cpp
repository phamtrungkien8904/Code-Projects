// Spring motion
#include <iostream>
#include <cmath>
#include <fstream>
#include <tuple>

using namespace std;

// Single FEM step for spring motion
tuple<double, double, double> spring(double k, double m, double x, double v, double t, double dt) {
    double a = -k * x / m - 50.1 * v / m; // Acceleration with damping
    v += a * dt; // Update velocity
    x += v * dt; // Update position
    t += dt;
    return {x, v, t};
}

// Write the position and time to a file

int main(int NArgc, char *Argv[]) {
    ofstream file("data.csv");
    file << "# Time(s), Position(m), Velocity(m/s)" << endl;
    double k = 10.0; // Spring constant
    double m = 1.0;  // Mass
    double x0 = 1.0; // Initial displacement
    double t_min = 0.0; // Minimum time
    double t_max = 10.0; // Maximum time
    double N = atof(Argv[1]); // Number of time steps
    double dt = (t_max - t_min) / N; // Time step
    double x = x0;
    double v = 0.0;
    double t = t_min;

    file << t << ", " << x << ", " << v << endl;
    for (int i = 0; i < static_cast<int>(N); ++i) {
        tie(x, v, t) = spring(k, m, x, v, t, dt);
        file << t << ", " << x << ", " << v << endl;
    }

    cout << "Data written to data.csv" << endl;
    return 0;
}

