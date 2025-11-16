import numpy as np

m = 3
n = 5
A = np.zeros((m, n),dtype=complex)
B = np.zeros((m, n),dtype=complex)

def func(x,t):
    C = np.zeros((m, n),dtype=complex)
    for i in range(m):
        for k in range(n):
            C[i][k] = i + 1j*k 
    return C[x][t]
C = func(1, 2)

print(C)