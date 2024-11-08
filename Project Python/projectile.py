from math import sin, cos, pi
from numpy import zeros 
import matplotlib.pyplot as plt

# Inputs
ub = 2
lb = 0
dt = 0.01
N = int((ub - lb)/dt)
x = zeros(N)
vx = zeros(N)
y = zeros(N)
vy = zeros(N)
t = zeros(N)
analytical_x = zeros(N)
analytical_y = zeros(N)

# Initial parameters
v0 = 10
theta = 45
g = 9.81
h0 = 10

# Initial conditions
x[0] = 0
vx[0] = v0*cos(theta)
y[0] = h0
vy[0] = v0*sin(theta)
t[0] = 0
analytical_x[0] = x[0] + vx[0]*t[0]
analytical_y[0] = y[0] + vy[0]*t[0] - 0.5*g*t[0]**2 


# Derivative function
for i in range(1, N):
    t[i] = t[i-1] + dt
    vx[i] = vx[i-1]
    x[i] = x[i-1] + dt*vx[i-1]
    vy[i] = vy[i-1] - g*dt
    y[i] = y[i-1] + dt*vy[i-1]
    analytical_x[i] = x[0] + vx[0]*t[i]
    analytical_y[i] = y[0] + vy[0]*t[i] - 0.5*g*t[i]**2


# Plot
plt.plot(x, y, label='Numerical')
plt.plot(analytical_x, analytical_y, label='Analytical')
plt.legend(['Numerical', 'Analytical'])
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.title('Projectile Motion')
plt.show()