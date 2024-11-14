import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



def simulate_orbit(initial_position, initial_velocity, dt, tmax, GM, R):
    # Initial conditions
    x = np.zeros(int(tmax / dt))
    y = np.zeros(int(tmax / dt))
    vx = np.zeros(int(tmax / dt))
    vy = np.zeros(int(tmax / dt))
    t = np.zeros(int(tmax / dt))

    # Set initial position and velocity
    x[0], y[0] = initial_position
    vx[0], vy[0] = initial_velocity

    # Set up the figure, the axis, and the plot element we want to animate
    fig, ax = plt.subplots()
    dashed, = ax.plot([], [], linestyle='--', lw=1)  # Dashed line for the radius
    orbit, = ax.plot([], [], linestyle='--', color='c',lw=1)  # Orbit line
    ball = plt.Circle((x[0], y[0]), R/20, color='b', fill=True)  # Ball at initial position
    line, = ax.plot([], [], linestyle='-', color='b', lw=2.5)  # Set the line style to solid
    center = plt.Circle((0, 0), R/20, color='r', fill=True)  # Static circle at (0,0)
    ax.add_patch(ball)
    ax.add_patch(center)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    r_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
    v_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)  # Velocity text

    ax.set_xlim(-2*R, 2*R)
    ax.set_ylim(-2*R, 2*R)
    ax.set_xlabel('x /m')
    ax.set_ylabel('y /m')
    ax.set_aspect('equal')  # Scale x and y axes equally

    def init():
        time_text.set_text('')
        r_text.set_text('')
        v_text.set_text('')
        line.set_data(x, y)  # Set the full orbit data for the line
        dashed.set_data(x, y)  # Set the full orbit data for the dashed line
        orbit.set_data(x, y)  # Set the full orbit data for the orbit
        ball.set_center((x[0], y[0]))
        return line, dashed, orbit, ball, time_text, r_text, v_text

    def animate(i):
        """Draw the frame i of the animation."""
        if i > 0:
            t[i] = t[i-1] + dt
            r = np.array([x[i-1], y[i-1]])
            v = np.array([vx[i-1], vy[i-1]])
            a = -GM * r / np.linalg.norm(r)**3
            v += a * dt
            r += v * dt
            x[i], y[i] = r
            vx[i], vy[i] = v

        start = max(0, i - 100)
        line.set_data(x[start:i+1], y[start:i+1])
        dashed.set_data([0, x[i]], [0, y[i]])
        orbit.set_data(x[0:i+1], y[0:i+1])
        ball.set_center((x[i], y[i]))

        # Update the time text
        time_text.set_text(f'Time = {t[i]/dt:.2f} days')
        r_text.set_text(f'r = {np.linalg.norm([x[i], y[i]])/10e11:.2f} e11 m')
        v_text.set_text(f'v = {np.linalg.norm([vx[i], vy[i]]):.2f} m/s')  # Update velocity text

        return orbit, dashed, line, ball, time_text, r_text, v_text  # Return line after orbit and dashed

    # Interval between frames in ms, total number of frames to use.
    interval, nframes = 10, int(tmax / dt)
    # Animate once (set repeat=False so the animation doesn't loop).
    ani = animation.FuncAnimation(fig, animate, frames=nframes, init_func=init,
                                  repeat=False, interval=interval, blit=True)
    plt.grid()
    plt.show()

# Constants
AU = 1.496e11  # Astronomical unit in meters
R = AU  # Scale the plot to 1 AU
initial_position = [AU, 0]  # 1 AU from the Sun
initial_velocity = [0, 29780]  # Approximate orbital speed of Earth in m/s
dt = 24* 60 * 60  # Time step in seconds (1 hour)
tmax = 365 * 24 * 60 * 60  # One year in seconds
GM = 1.32712440018e20  # Gravitational constant * mass of the Sun (m^3/s^2)

simulate_orbit(initial_position, initial_velocity, dt, tmax, GM, R)

