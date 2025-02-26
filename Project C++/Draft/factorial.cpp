#include <iostream>
using namespace std;

int nFac(int n) {
    if (n == 0) {
        return 1;
    } else {
        return n * nFac(n - 1);
    }
    // Alternative: for loop
    // for (int i = n - 1; i > 0; i--) {
    //     n *= i;
    // }
    // return n;
}

int main() {
    cout << "Factorial N!" << endl;
    int N;
    cout << "Enter N: ";
    cin >> N;
    cout << N << "! = " << nFac(N) << endl;
    return 0;
}