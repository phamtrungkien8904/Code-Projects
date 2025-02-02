#include <iostream> 
#include <vector>
using namespace std;

double vectorsum(const vector<double> &v) {
    double sum = 0;
    for (int i = 0; i < v.size(); i++) {
        sum += v[i];
    }
    return sum;
}

int main() {
    vector<double> v = {1.1, 2.2, 3.3, 4.4, 5.5};
    cout << "The sum of the vector is: " << vectorsum(v) << endl;
    return 0;
}