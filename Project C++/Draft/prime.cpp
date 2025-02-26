#include <bits/stdc++.h>
using namespace std;


int main() {
    int count = 0;
    int n;
    cout << "Prime numbers below: ";
    cin >> n;
    
    // Initialize a vector of bools to keep track of prime numbers
     vector<bool> is_prime(n + 1, true);
    is_prime[0] = is_prime[1] = false;

    // Sieve of Eratosthenes algorithm
    for (int i = 2; i * i <= n; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= n; j += i) {
                is_prime[j] = false;
            }
        }
    }

    // Print all prime numbers and count them
    for (int i = 2; i <= n; i++) {
        if (is_prime[i]) {
            cout << i << " ";
            count++;
        }
    }
    cout << endl <<"There are " << count <<" prime numbers" << endl;
    return 0;
}