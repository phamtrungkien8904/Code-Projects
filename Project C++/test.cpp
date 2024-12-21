#include <iostream>
#include <vector>

using namespace std;

vector<double> squares(int n) {
    vector<double> result;
    for (int i = 0; i < n; i++) {
        result.push_back(i * i);
    }
    return result;
}

int main() {
    for (double d : squares(10)) {
        cout << d << " ";
    }
    cout << endl;
    return 0;
}