#include "Core"
#include "LU"
#include "Cholesky"
#include "QR"
#include "SVD"
#include "Geometry"
#include "Eigenvalues"
#include <iostream> 
#include <fstream>
using namespace Eigen;
using namespace std;

int main(){
    MatrixXd A(3,3);
    A << 2, -1, 2,
         -1, 2, -2,
         2, -2, 5;
    cout << "Here is the matrix A:\n" << A << endl;
    cout << "Here is the matrix A^T:\n" << A.transpose() << endl;
    cout << "Here is the matrix A^(-1):\n" << 7*A.inverse() << endl;
    cout << "Here is the determinant of A:\n" << A.determinant() << endl;
    cout << "Here is the eigenvalues of A:\n" << A.eigenvalues() << endl;
    cout << "Here is the trace of A:\n" << A.trace() << endl;
    cout << "Here is the matrix A^2:\n" << A*A << endl;
}
