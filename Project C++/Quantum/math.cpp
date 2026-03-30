#include "eigen\Eigen\Dense"
#include <iostream>
#include <cmath>
#include <fstream>
#include <tuple>
#include <vector>

using namespace std;
using namespace Eigen;

// Find Eigenvalues and eigenvectors of a matrix
int main() {
    Matrix3d A;
    A << 1, 2, 3,
         0, 1, 4,
         5, 6, 0;

    EigenSolver<Matrix3d> es(A);
    cout << "The eigenvalues of A are:" << endl << es.eigenvalues() << endl;
    cout << "The eigenvectors of A are:" << endl << es.eigenvectors() << endl;

    return 0;
}

