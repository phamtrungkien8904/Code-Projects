from math import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt

# Initial conditions
GM = 1.0
tmax = 10
dt = 0.01
x = np.zeros(int(tmax / dt))
y = np.zeros(int(tmax / dt))
vx = np.zeros(int(tmax / dt))
vy = np.zeros(int(tmax / dt))
t = np.zeros(int(tmax / dt))



# Initial conditions
x[0], y[0] = [1.0, 0.0]
vx[0], vy[0] = [0.0, 1.0]


# Derivative function
for i in range(1, int(tmax / dt)):
    t[i] = t[i-1] + dt
    r = np.array([x[i-1], y[i-1]])
    v = np.array([vx[i-1], vy[i-1]])
    a = -GM * r / np.linalg.norm(r)**3
    v += a * dt
    r += v * dt
    x[i], y[i] = r
    vx[i], vy[i] = v


# Plot
plt.plot(x, y, label='Numerical')
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.grid()
plt.show()