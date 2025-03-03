import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def simulate_orbit(initial_position_1, initial_velocity_1, initial_position_2, initial_velocity_2, initial_position_ship, initial_velocity_ship, dt, tmax, GM, R):
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

    # Initial conditions for spaceship
    x_ship = np.zeros(int(tmax / dt))
    y_ship = np.zeros(int(tmax / dt))
    vx_ship = np.zeros(int(tmax / dt))
    vy_ship = np.zeros(int(tmax / dt))

    # Set initial position and velocity for planet 1 (Earth)
    x1[0], y1[0] = initial_position_1
    vx1[0], vy1[0] = initial_velocity_1

    # Set initial position and velocity for planet 2 (Mars)
    x2[0], y2[0] = initial_position_2
    vx2[0], vy2[0] = initial_velocity_2

    # Set initial position and velocity for spaceship
    x_ship[0], y_ship[0] = initial_position_ship
    vx_ship[0], vy_ship[0] = initial_velocity_ship

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
    planet_2 = plt.Circle((x2[0], y2[0]), R/30, color='orange', fill=True)  # Planet 2 at initial position
    ax.add_patch(planet_2)
    line_2, = ax.plot([], [], linestyle='-', color='orange', lw=3)  # Set the line style to solid

    # Spaceship
    spaceship, = ax.plot([], [], linestyle='-', color='g', lw=1)  # Orbit line
    ship = plt.Circle((x_ship[0], y_ship[0]), R/50, color='g', fill=True)  # Spaceship at initial position
    ax.add_patch(ship)
    line_ship, = ax.plot([], [], linestyle='-', color='g', lw=3)  # Set the line style to solid

    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)


    ax.set_xlim(-2*R, 2*R)
    ax.set_ylim(-2*R, 2*R)
    ax.set_xlabel('x /m')
    ax.set_ylabel('y /m')
    ax.set_aspect('equal')  # Scale x and y axes equally

    def init():
        time_text.set_text('')
        line_1.set_data([], [])
        orbit_1.set_data([], [])
        planet_1.set_center((x1[0], y1[0]))
        line_2.set_data([], [])
        orbit_2.set_data([], [])
        planet_2.set_center((x2[0], y2[0]))
        ship.set_center((x_ship[0], y_ship[0]))
        spaceship.set_data([], [])
        line_ship.set_data([], [])
        return orbit_1, planet_1, line_1, orbit_2, planet_2, line_2, spaceship, ship, line_ship, time_text

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

            # Update position and velocity for spaceship
            r_ship = np.array([x_ship[i-1], y_ship[i-1]])
            v_ship = np.array([vx_ship[i-1], vy_ship[i-1]])
            a_ship = -GM * r_ship / np.linalg.norm(r_ship)**3 - GM*1e-6 * (r_ship - r2) / np.linalg.norm(r_ship - r2)**3
            v_ship += a_ship * dt
            r_ship += v_ship * dt
            x_ship[i], y_ship[i] = r_ship
            vx_ship[i], vy_ship[i] = v_ship

        start = max(0, i - 100)
        line_1.set_data(x1[start:i+1], y1[start:i+1])
        orbit_1.set_data(x1[0:i+1], y1[0:i+1])
        planet_1.set_center((x1[i], y1[i]))

        line_2.set_data(x2[start:i+1], y2[start:i+1])
        orbit_2.set_data(x2[0:i+1], y2[0:i+1])
        planet_2.set_center((x2[i], y2[i]))

        line_ship.set_data(x_ship[start:i+1], y_ship[start:i+1])
        spaceship.set_data(x_ship[0:i+1], y_ship[0:i+1])
        ship.set_center((x_ship[i], y_ship[i]))

        # Update the time text
        time_text.set_text(f'Time = {t[i]/(24*60*60):.2f} days')

        return orbit_1, planet_1, line_1, orbit_2, planet_2, line_2, spaceship, ship, line_ship, time_text


    # Interval between frames in ms, total number of frames to use.
    interval, nframes = 10, int(tmax / dt)
    # Animate once (set repeat=False so the animation doesn't loop).
    ani = animation.FuncAnimation(fig, animate, frames=nframes, init_func=init,
                                  repeat=False, interval=interval, blit=True)
    fig.suptitle('Hohmann Transfer Orbit Simulation')  # Set the name for the figure
    #plt.grid()
    plt.show()
    #ani.save('orbit.mp4')

# Constants
AU = 1.496e11  # Astronomical unit in meters
R = AU  # Scale the plot to 1 AU
initial_position_1 = [AU, 0]  # 1 AU from the Sun (Earth)
initial_velocity_1 = [0, 29780]  # Approximate orbital speed of Earth in m/s
theta = np.pi /4  # Angle between Earth and Mars
initial_position_2 = [1.524 * AU * np.cos(theta), 1.524 * AU * np.sin(theta)]  # 1.524 AU from the Sun (Mars)
initial_velocity_2 = [-24007* np.sin(theta), 24007* np.cos(theta)]  # Approximate orbital speed of Mars in m/s
initial_position_ship = [AU, 0]  # Initial position of the spaceship (same as Earth)
initial_velocity_ship = [0, 10000]  # Initial velocity of the spaceship (same as Earth)
dt =  60 * 60  # Time step in seconds (hrs)
tmax = 0.3* 366 * 24 * 60 * 60  # 0.7 years in seconds
GM = 1.32712440018e20  # Gravitational constant * mass of the Sun (m^3/s^2)

simulate_orbit(initial_position_1, initial_velocity_1, initial_position_2, initial_velocity_2, initial_position_ship, initial_velocity_ship, dt, tmax, GM, R)
