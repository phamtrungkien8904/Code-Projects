import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
GM = 1.0  # Gravitational constant times mass of the central object
dt = 0.01  # Time step
tmax = 20.0  # Maximum time

# Initial conditions
x = np.zeros(int(tmax / dt))
y = np.zeros(int(tmax / dt))
vx = np.zeros(int(tmax / dt))
vy = np.zeros(int(tmax / dt))
t = np.zeros(int(tmax / dt))

# Set initial position and velocity
x[0], y[0] = 1.0, 0.0
vx[0], vy[0] = 0.0, 1.1

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
r_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
v_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)  # Velocity text

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')

def init():
    time_text.set_text('')
    r_text.set_text('')
    v_text.set_text('')
    line.set_data([], [])
    return line, time_text, r_text, v_text

def animate(i, x, y, t, vx, vy, dt):
    """Draw the frame i of the animation."""

    # Update this time point and its data and set the plotted line data.
    if i > 0:
        t[i] = t[i-1] + dt
        r = np.array([x[i-1], y[i-1]])
        v = np.array([vx[i-1], vy[i-1]])
        a = -GM * r / np.linalg.norm(r)**3
        v += a * dt
        r += v * dt
        x[i], y[i] = r
        vx[i], vy[i] = v

    line.set_data(x[:i+1], y[:i+1])
    
    # Update the time text
    time_text.set_text(f'Time = {t[i]:.2f} s')
    r_text.set_text(f'r = {np.linalg.norm([x[i], y[i]]):.2f} m')
    v_text.set_text(f'v = {np.linalg.norm([vx[i], vy[i]]):.2f} m/s')  # Update velocity text

    return line, time_text, r_text, v_text

# Interval between frames in ms, total number of frames to use.
interval, nframes = 1000 * dt, int(tmax / dt)
# Animate once (set repeat=False so the animation doesn't loop).
ani = animation.FuncAnimation(fig, animate, frames=nframes, init_func=init,
                              fargs=(x, y, t, vx, vy, dt), repeat=False, interval=interval, blit=True)
plt.grid()
plt.show()