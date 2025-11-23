import numpy as np
import matplotlib.pyplot as plt

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
C = func(1,2)
V = np.zeros(4)
for i in range(4):
    V[i] = i**2

H = 2*np.diag(np.ones(4) + V,0) + np.diag(np.ones(4-1),1) + np.diag(np.ones(4-1),-1)
H[2][0] = 1


print(V)
print(H)


