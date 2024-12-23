#include <iostream>
#include <algorithm>
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
    for (double d : squares(15)) {
        cout << d << " ";
    }
    cout << endl;
    vector<int> v = {1,3,4,2,5,7,9};
    sort(v.begin(), v.end());
    for (int i : v) {
        cout << i << " ";
    }
    cout << endl;
    return 0;
}

