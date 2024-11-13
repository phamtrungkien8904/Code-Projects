from math import sin, cos, radians, sqrt
import numpy as np 
from numpy import zeros
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Inputs
tmax = 10
tmin = 0
dt = 0.001
N = int((tmax - tmin)/dt)
x = zeros(N)
vx = zeros(N)
y = zeros(N)
vy = zeros(N)
t = zeros(N)

# Initial parameters.
GM = 2
v0 = 1
theta = 0 

# Initial conditions.
t[0] = 0
x[0] = 2
vx[0] = v0 * sin(theta)
y[0] = 0
vy[0] = v0 * cos(theta)

# Draw an empty plot, but preset the plot x- and y-limits.
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')

# Create a text object to display the time
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
r_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)


def init():
    time_text.set_text('')
    r_text.set_text('')
    line.set_data([], [])
    return line, time_text, r_text

def animate(i, x, y, t, vx, vy, dt):
    """Draw the frame i of the animation."""

    # Update this time point and its data and set the plotted line data.
    if i > 0:
        t[i] = t[i-1] + dt
        vx[i] = vx[i-1] - GM * x[i-1] * dt / sqrt(x[i-1]**2 + y[i-1]**2)**3
        x[i] = x[i-1] + dt * vx[i-1]
        vy[i] = vy[i-1] - GM * y[i-1] * dt / sqrt(x[i-1]**2 + y[i-1]**2)**3
        y[i] = y[i-1] + dt * vy[i-1]

    # Stop the animation if y reaches 0

    line.set_data(x[:i+1], y[:i+1])
    
    # Update the time text
    time_text.set_text(f'Time = {t[i]:.2f} s')
    r_text.set_text(f'r = {sqrt(x[i]**2 + y[i]**2):.2f} m')

    
    return line, time_text, r_text

# Interval between frames in ms, total number of frames to use.
interval, nframes = 1000 * dt, int(tmax / dt)
# Animate once (set repeat=False so the animation doesn't loop).
ani = animation.FuncAnimation(fig, animate, frames=nframes, init_func=init,
                              fargs=(x, y, t, vx, vy, dt), repeat=False, interval=interval, blit=True)
plt.grid()
plt.show()