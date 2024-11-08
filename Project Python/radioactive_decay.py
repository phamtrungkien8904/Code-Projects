# Method to solve ordinary differential equations using finite difference method

from math import sin, cos, pi
from numpy import zeros 
import matplotlib.pyplot as plt

# Inputs
ub = 10
lb = 0
h = 0.1
N = int((ub - lb)/h)
x = zeros(N)
y = zeros(N)
analytical = zeros(N)

# Initial conditions
x[0] = 0
y[0] = 2
analytical[0] = 2

# Derivative function
for i in range(1, N):
    y[i] = y[i-1] + h*sin(5*x[i-1]) # dy/dx = sin(5x)
    x[i] = x[i-1] + h
    analytical[i] = -1/5*(cos(5*x[i]) - 11) # Analytical solution

# Plot
plt.plot(x, y, label='Numerical')
plt.plot(x, analytical, label='Analytical')
plt.legend(['Numerical', 'Analytical'])
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.title('Finite Difference')
plt.show()