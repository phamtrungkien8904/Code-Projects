from math import sin, cos, radians
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Time step for the animation (s), max time to animate for (s).
dt, tmax = 0.01, 5
# These lists will hold the data to plot.
t, x, y, vx, vy = [], [], [], [], []
# Initial parameters.
v0 = 10
theta = radians(45)  # Convert angle to radians
g = 9.81
h0 = 5

# Initial conditions.
vx.append(v0 * cos(theta))
vy.append(v0 * sin(theta))
x.append(0)
y.append(h0)
t.append(0)

# Draw an empty plot, but preset the plot x- and y-limits.
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(0, 20)
ax.set_ylim(0, 20)
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')

# Create a text object to display the time
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def init():
    time_text.set_text('')
    return line, time_text

def animate(i, x, y):
    """Draw the frame i of the animation."""

    # Append this time point and its data and set the plotted line data.
    _t = i * dt
    t.append(_t)
    x.append(vx[0] * _t)
    y.append(y[0] + vy[0] * _t - 0.5 * g * _t**2)
    line.set_data(x, y)
    
    # Update the time text
    time_text.set_text(f'Time = {_t:.2f} s')
    
    return line, time_text

# Interval between frames in ms, total number of frames to use.
interval, nframes = 1000 * dt, int(tmax / dt)
# Animate once (set repeat=False so the animation doesn't loop).
ani = animation.FuncAnimation(fig, animate, frames=nframes, init_func=init,
                              fargs=(x, y), repeat=False, interval=interval, blit=True)
plt.grid()
plt.show()