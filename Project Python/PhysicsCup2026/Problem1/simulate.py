## Problem 1
# A small brick is squeezed between two parallel planes in zero-gravity. The planes are perpendicular to the axis $z$.
# The lower plane always stays in rest, whilst the upper one is moving with the constant velocity $\vec{v}$ along the axis $x$. 
# Initially the velocity of the brick $\vec{u}_0$ is perpendicular to $\vec{v}$ and lies in axis $y$.
# The friction between the brick and the planes is dry with same coefficient of kinetic friction.
# Given the initial acceleration of the brick $\vec{a}_0$, find the displacement of the brick $l_y$ along the $y$ axis after a long time.
# Numerical: $v = u_0 = 1$ m/s, $a_0 = 1\ \mathrm{m/s^2}$ with 4 digits
##

from math import sqrt
from numpy import zeros 
import csv
import matplotlib.pyplot as plt

# Inputs
alpha1 = 0.67632
alpha2 = 0.4

t_min = 0
t_max = 20
dt = 0.01
N = int((t_max - t_min)/dt)
t = zeros(N)
x = zeros(N)
y = zeros(N)
ux = zeros(N)
uy = zeros(N)
# Initial conditions
u0 = 1
v = 1


x[0] = 0
y[0] = 0
ux[0] = 0
uy[0] = u0
t[0] = 0
# Derivative function
for i in range(1, N):
    t[i] = t[i-1] + dt
    ux[i] = ux[i-1] + (alpha1*(v-ux[i-1])/sqrt(v**2 + ux[i-1]**2 + uy[i-1]**2) - alpha2*ux[i-1]/sqrt(uy[i-1]**2 + ux[i-1]**2))*dt
    uy[i] = uy[i-1] + (alpha1*(0-uy[i-1])/sqrt(v**2 + ux[i-1]**2 + uy[i-1]**2) - alpha2*uy[i-1]/sqrt(uy[i-1]**2 + ux[i-1]**2))*dt
    x[i] = x[i-1] + ux[i-1]*dt
    y[i] = y[i-1] + uy[i-1]*dt

# Track the peak displacement reached along the y-axis.
y_max = y.max()
print(f"Maximum y displacement: {y_max:.6f} m")
u_inf = ux.max()
print(f"Final x-velocity: {u_inf:.6f} m/s")

# Persist the simulation output for further analysis.
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t', 'x', 'y', 'ux', 'uy'])
    for i in range(N):
        writer.writerow([t[i], x[i], y[i], ux[i], uy[i]])

# Plot
plt.plot(x, y, label='y(t)')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Trajectory of the Brick')
plt.grid()
plt.show()