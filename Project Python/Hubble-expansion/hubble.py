# Hubble Expansion Simulation
from math import sin, cos, pi
import numpy as np
from numpy import zeros
import matplotlib.pyplot as plt


# Inputs
ub = 10
lb = 0
dt = 0.01
N = int((ub - lb)/dt)
r = zeros(N)
v = zeros(N)
t = zeros(N)
rho = zeros(N)


# Initial parameters
r0 = 0.1
G = 1
k = -1
rho[0] = 4*pi*r0**3/3


# Initial conditions
r[0] = r0
v[0] = 0



# Derivative function
for i in range(1, N):
    t[i] = t[i-1] + dt
    v[i] = v[i-1] + r[i-1]*np.sqrt(8*pi*G*rho[i-1]/3 - k/r[i-1]**2)*dt
    r[i] = r[i-1] + dt*v[i-1]
    rho[i] = rho[0]*(r0/r[i])**3




# Plot
plt.plot(t, r, label='Numerical')
plt.legend()
plt.xlabel('$t$')
plt.ylabel('$r$')
plt.title('Hubble Expansion Simulation')
plt.grid()
plt.show()