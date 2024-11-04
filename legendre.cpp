#include <iostream>
#include <cmath>
using namespace std;

double legendre(int n, double x) {
    if (n == 0) {
        return 1;
    } else if (n == 1) {
        return x;
    } else {
        double l = (2.0*n - 1.0)/n * x * legendre(n - 1.0, x) - (n - 1.0)/n * legendre(n - 2, x);// Caution: use 2.0 instead of 2 to avoid integer division
        return l; 
    }
}

int main() {
    cout << "Legendre Polynomial" << endl;
    int N;
    cout << "Enter N: ";
    cin >> N;
    cout << "Enter x: ";
    double x_in;
    cin >> x_in;
    for (int i = 0; i <= N; i++) {
        cout << "P" << i << "(" << x_in << ") = " << legendre(i, x_in) << endl;
    }   
    // do {
    //     cout << "P" << N << "(" << x_in << ") = " << legendre(N, x_in) << endl;
    //     N++;
    // } while (N <= 10);

    return 0;
}