import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Time step for the animation (s), max time to animate for (s).
dt, tmax = 0.01, 5
# Signal frequency (s-1), decay constant (s-1).
f, alpha = 2.5, 1
# These lists will hold the data to plot.
t, M, E, NE = [], [], [], []

# Draw an empty plot, but preset the plot x- and y-limits.
fig, ax = plt.subplots()
line1, = ax.plot([], [], linestyle='-')  # Set the line style to dashed
line2, = ax.plot([], [], linestyle='--')   # Set the line style to solid
line3, = ax.plot([], [], linestyle='--')  # Set the line style to dash-dot
ax.set_xlim(0, tmax)
ax.set_ylim(-1, 1)
ax.set_xlabel('t /s')
ax.set_ylabel('M (arb. units)')

def init():
    return line1, line2, line3

def animate(i, t, M, E, NE):
    """Draw the frame i of the animation."""

    # Append this time point and its data and set the plotted line data.
    T = i*dt
    t.append(T)
    M.append(np.sin(2*np.pi*f*T) * np.exp(-alpha*T))
    E.append(np.exp(-alpha*T))
    NE.append(-np.exp(-alpha*T))
    line1.set_data(t, M)
    line2.set_data(t, E)
    line3.set_data(t, NE)
    return line1, line2, line3

# Interval between frames in ms, total number of frames to use.
interval, nframes = 1000 * dt, int(tmax / dt)
# Animate once (set repeat=False so the animation doesn't loop).
ani = animation.FuncAnimation(fig, animate, frames=nframes, init_func=init,
                  fargs=(t, M, E, NE), repeat=False, interval=interval, blit=True)
plt.grid()
plt.show()