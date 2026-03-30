// Spring motion
#include <iostream>
#include <cmath>
#include <fstream>

using namespace std;


double spring(double k, double m, double x0, double t) {
    double omega = sqrt(k / m);
    return x0 * cos(omega * t);
}

// Write the position and time to a file

int main(int NArgc, char *Argv[]) {
    ofstream file("data.csv");
    file << "# Time(s), Position(m)" << endl;
    double k = 10.0; // Spring constant
    double m = 1.0;  // Mass
    double x0 = 1.0; // Initial displacement
    double t_min = 0.0; // Minimum time
    double t_max = 10.0; // Maximum time
    double N = atof(Argv[1]); // Number of time steps
    double dt = (t_max - t_min) / N; // Time step
    for (double t = t_min; t <= t_max; t += dt) {
        double x = spring(k, m, x0, t);
        file << t << ", " << x << endl;
    };
    cout << "Data written to data.csv" << endl;
    return 0;
}

