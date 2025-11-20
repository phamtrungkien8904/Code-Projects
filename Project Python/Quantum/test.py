import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

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


H = 2*np.diag(np.ones(m),0) + np.diag(np.ones(m-1),1)
E, V = np.linalg.eigh(H)

print(H)