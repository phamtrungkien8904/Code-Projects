import numpy as np
import matplotlib.pyplot as plt

m = 3
n = 5
A = np.zeros((m, n), dtype=complex)
B = np.zeros((m, n), dtype=complex)
C = np.zeros((m, n), dtype=complex)

def func(x,t):
    C = np.zeros((m, n), dtype=complex)
    for i in range(m):
        for j in range(n):
            C[i,j] = i + j 
    return C[x][t]
C = func(1, 2)
print(C)