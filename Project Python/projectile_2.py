from math import sin, cos, radians
import numpy as np 
from numpy import zeros
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Inputs
tmax = 10
tmin = 0
dt = 0.01
N = int((tmax - tmin)/dt)
x = zeros(N)
vx = zeros(N)
y = zeros(N)
vy = zeros(N)
t = zeros(N)

# Initial parameters.
v0 = 10
theta = radians(45)  # Convert angle to radians
g = 9.81
h0 = 5

# Initial conditions.
t[0] = 0
x[0] = 0
vx[0] = v0 * cos(theta)
y[0] = h0
vy[0] = v0 * sin(theta)

# Draw an empty plot, but preset the plot x- and y-limits.
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(0, 20)
ax.set_ylim(0, 20)
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')

# Create a text object to display the time
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
x_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
y_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)

def init():
    time_text.set_text('')
    x_text.set_text('')
    y_text.set_text('')
    line.set_data([], [])
    return line, time_text, x_text, y_text

def animate(i, x, y, t, vx, vy, dt, g):
    """Draw the frame i of the animation."""

    # Update this time point and its data and set the plotted line data.
    if i > 0:
        t[i] = t[i-1] + dt
        vx[i] = vx[i-1]
        x[i] = x[i-1] + dt * vx[i-1]
        vy[i] = vy[i-1] - g * dt
        y[i] = y[i-1] + dt * vy[i-1]

    # Stop the animation if y reaches 0
    if y[i] <= 0:
        ani.event_source.stop()
        y[i] = 0  # Ensure y does not go below 0

    line.set_data(x[:i+1], y[:i+1])
    
    # Update the time text
    time_text.set_text(f'Time = {t[i]:.2f} s')
    x_text.set_text(f'x = {x[i]:.2f} m')
    y_text.set_text(f'y = {y[i]:.2f} m')
    
    return line, time_text, x_text, y_text

# Interval between frames in ms, total number of frames to use.
interval, nframes = 1000 * dt, int(tmax / dt)
# Animate once (set repeat=False so the animation doesn't loop).
ani = animation.FuncAnimation(fig, animate, frames=nframes, init_func=init,
                              fargs=(x, y, t, vx, vy, dt, g), repeat=False, interval=interval, blit=True)
plt.grid()
plt.show()