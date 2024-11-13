import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def simulate_orbit(initial_position, initial_velocity, dt=0.01, tmax=20.0, GM=1.0):
    # Initial conditions
    x = np.zeros(int(tmax / dt))
    y = np.zeros(int(tmax / dt))
    vx = np.zeros(int(tmax / dt))
    vy = np.zeros(int(tmax / dt))
    t = np.zeros(int(tmax / dt))

    # Set initial position and velocity
    x[0], y[0] = initial_position
    vx[0], vy[0] = initial_velocity

    fig, ax = plt.subplots()
    line, = ax.plot([], [], linestyle='-', lw=2)  # Set the line style to solid
    ball = plt.Circle((x[0], y[0]), 0.05)
    center = plt.Circle((0, 0), 0.1, color='r', fill=True)  # Static circle at (0,0)
    ax.add_patch(ball)
    ax.add_patch(center)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    r_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
    v_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)  # Velocity text

    # Plot y = sin(x) from x = -1 to x = 1
    x_sin = np.linspace(-1, 1, 400)
    y_sin = np.sin(x_sin)
    ax.plot(x_sin, y_sin, 'g-', lw=2)  # Green line for y = sin(x)

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_xlabel('x /m')
    ax.set_ylabel('y /m')
    ax.set_aspect('equal')  # Scale x and y axes equally

    def init():
        time_text.set_text('')
        r_text.set_text('')
        v_text.set_text('')
        line.set_data([], [])
        ball.set_center((x[0], y[0]))
        return line, ball, time_text, r_text, v_text

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
        ball.set_center((x[i], y[i]))

        # Update the time text
        time_text.set_text(f'Time = {t[i]:.2f} s')
        r_text.set_text(f'r = {np.linalg.norm([x[i], y[i]]):.2f} m')
        v_text.set_text(f'v = {np.linalg.norm([vx[i], vy[i]]):.2f} m/s')  # Update velocity text

        return line, ball, time_text, r_text, v_text

    # Interval between frames in ms, total number of frames to use.
    interval, nframes = 1000 * dt, int(tmax / dt)
    # Animate once (set repeat=False so the animation doesn't loop).
    ani = animation.FuncAnimation(fig, animate, frames=nframes, init_func=init,
                                  repeat=False, interval=interval, blit=True)
    plt.grid()
    plt.show()
