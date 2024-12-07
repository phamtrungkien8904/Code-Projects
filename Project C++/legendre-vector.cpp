#include <iostream>
#include <vector>
using namespace std;

vector<double> legendre(int n, double x) {
    vector<double> l;
    if (n == 0) {
        l.push_back(1);
    } else if (n == 1) {
        l.push_back(x);
    } else {
        l.push_back(1);
        l.push_back(x);
        for (int i = 2; i <= n; i++) {
            double l_i = (2.0 * i - 1.0) / i * x * l[i - 1] - (i - 1.0) / i * l[i - 2];
            l.push_back(l_i);
        }
    }
    return l;
}

int main(){
    vector <double> leg = legendre(10, 2.0);
    cout << "Legendre Polynomial" << endl;
    for (auto i = 0; i < leg.size(); i++) {
        cout << "P" << i << "(0.5) = " << leg[i] << endl;
    };
    return 0;
}
