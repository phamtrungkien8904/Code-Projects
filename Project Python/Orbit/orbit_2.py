import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def simulate_orbit(initial_position_1, initial_velocity_1, initial_position_2, initial_velocity_2, dt, tmax, GM, R):
    # Initial conditions for planet 1 (Earth)
    x1 = np.zeros(int(tmax / dt))
    y1 = np.zeros(int(tmax / dt))
    vx1 = np.zeros(int(tmax / dt))
    vy1 = np.zeros(int(tmax / dt))
    t = np.zeros(int(tmax / dt))

    # Initial conditions for planet 2 (Mars)
    x2 = np.zeros(int(tmax / dt))
    y2 = np.zeros(int(tmax / dt))
    vx2 = np.zeros(int(tmax / dt))
    vy2 = np.zeros(int(tmax / dt))

    # Set initial position and velocity for planet 1 (Earth)
    x1[0], y1[0] = initial_position_1
    vx1[0], vy1[0] = initial_velocity_1

    # Set initial position and velocity for planet 2 (Mars)
    x2[0], y2[0] = initial_position_2
    vx2[0], vy2[0] = initial_velocity_2

    # Set up the figure, the axis, and the plot elements we want to animate
    fig, ax = plt.subplots()
    center = plt.Circle((0, 0), R/20, color='r', fill=True)  # Static circle at (0,0)
    ax.add_patch(center)

    # Planet 1 (Earth)
    orbit_1, = ax.plot([], [], linestyle='-', color='b', lw=1)  # Orbit line
    planet_1 = plt.Circle((x1[0], y1[0]), R/25, color='b', fill=True)  # Planet 1 at initial position
    ax.add_patch(planet_1)
    line_1, = ax.plot([], [], linestyle='-', color='b', lw=3)  # Set the line style to solid

    # Planet 2 (Mars)
    orbit_2, = ax.plot([], [], linestyle='-', color='orange', lw=1)  # Orbit line
    planet_2 = plt.Circle((x2[0], y2[0]), R/25, color='orange', fill=True)  # Planet 2 at initial position
    ax.add_patch(planet_2)
    line_2, = ax.plot([], [], linestyle='-', color='orange', lw=3)  # Set the line style to solid

    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    r_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
    v_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)

    ax.set_xlim(-2*R, 2*R)
    ax.set_ylim(-2*R, 2*R)
    ax.set_xlabel('x /m')
    ax.set_ylabel('y /m')
    ax.set_aspect('equal')  # Scale x and y axes equally

    def init():
        time_text.set_text('')
        r_text.set_text('')
        v_text.set_text('')
        line_1.set_data([], [])
        orbit_1.set_data([], [])
        planet_1.set_center((x1[0], y1[0]))
        line_2.set_data([], [])
        orbit_2.set_data([], [])
        planet_2.set_center((x2[0], y2[0]))
        return orbit_1, planet_1, line_1, orbit_2, planet_2, line_2, time_text, r_text, v_text

    def animate(i):
        """Draw the frame i of the animation."""
        if i > 0:
            t[i] = t[i-1] + dt
            # Update position and velocity for planet 1 (Earth)
            r1 = np.array([x1[i-1], y1[i-1]])
            v1 = np.array([vx1[i-1], vy1[i-1]])
            a1 = -GM * r1 / np.linalg.norm(r1)**3
            v1 += a1 * dt
            r1 += v1 * dt
            x1[i], y1[i] = r1
            vx1[i], vy1[i] = v1

            # Update position and velocity for planet 2 (Mars)
            r2 = np.array([x2[i-1], y2[i-1]])
            v2 = np.array([vx2[i-1], vy2[i-1]])
            a2 = -GM * r2 / np.linalg.norm(r2)**3
            v2 += a2 * dt
            r2 += v2 * dt
            x2[i], y2[i] = r2
            vx2[i], vy2[i] = v2

        start = max(0, i - 100)
        line_1.set_data(x1[start:i+1], y1[start:i+1])
        orbit_1.set_data(x1[0:i+1], y1[0:i+1])
        planet_1.set_center((x1[i], y1[i]))

        line_2.set_data(x2[start:i+1], y2[start:i+1])
        orbit_2.set_data(x2[0:i+1], y2[0:i+1])
        planet_2.set_center((x2[i], y2[i]))

        # Update the time text
        time_text.set_text(f'Time = {t[i]/dt:.2f} days')
        r_text.set_text(f'r = {np.linalg.norm([x1[i], y1[i]])/AU:.2f} AU')
        v_text.set_text(f'v = {np.linalg.norm([vx1[i], vy1[i]]):.2f} m/s')  # Update velocity text

        return orbit_1, planet_1, line_1, orbit_2, planet_2, line_2, time_text, r_text, v_text


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
initial_position_1 = [AU, 0]  # 1 AU from the Sun (Earth)
initial_velocity_1 = [0, 29780]  # Approximate orbital speed of Earth in m/s
initial_position_2 = [1.524 * AU, 0]  # 1.524 AU from the Sun (Mars)
initial_velocity_2 = [0, 24007]  # Approximate orbital speed of Mars in m/s
dt = 24 * 60 * 60  # Time step in seconds (1 day)
tmax = 366 * 24 * 60 * 60  # One year in seconds
GM = 1.32712440018e20  # Gravitational constant * mass of the Sun (m^3/s^2)

simulate_orbit(initial_position_1, initial_velocity_1, initial_position_2, initial_velocity_2, dt, tmax, GM, R)

