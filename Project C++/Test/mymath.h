#ifndef mymath
#define mymath

#include <iostream>

class MyMath{
    public:
    int Factorial(int n){
        if(n == 0){
            return 1;
        }
        return n * Factorial(n - 1);
    }
};

#endif
