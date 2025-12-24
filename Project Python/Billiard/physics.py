import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


## Pool ball with spin 

# Time steps
dt = 0.01
t_min = 0
t_max =5
Nt = int((t_max - t_min) / dt) 


t = np.linspace(t_min, t_max, Nt + 1)

# Parameters
x_min = 0
x_max = 10
y_min = 0
y_max = 10
m = 1.0  # mass of ball
g = 9.81  # m/s^2 (magnitude)
R = 0.1  # radius of ball
mu = 0.2  # kinetic friction coefficient with table

def motion(r0,v0, w0):
    r = np.zeros((len(t), 3))
    v = np.zeros((len(t), 3))
    w = np.zeros((len(t), 3))
    vC = np.zeros((len(t), 3))  # contact point velocity
    r[0] = r0
    v[0] = v0
    w[0] = w0
    vC[0] = v0 + np.cross(w0, np.array([0,0,-R]))

    # Slipping time
    tau = 2 / (7 * mu * g) * np.linalg.norm(vC[0])

    eps = 1e-12

    for i in range(1, len(t)):

        vC_norm = np.linalg.norm(vC[i - 1])
        if vC_norm < eps:
            # No slipping: with this simple model we stop applying kinetic friction.
            vC[i] = np.zeros(3)
            w[i] = w[i - 1]
            v[i] = v[i - 1]
            r[i] = r[i - 1] + v[i - 1] * dt
            continue

        vC_hat = vC[i - 1] / vC_norm

        # Contact point velocity decays linearly during slipping:
        #   dvC/dt = -(7/2) * mu * g * vC_hat
        vC[i] = vC[i - 1] + dt * (-(7 / 2) * mu * g * vC_hat)

        # Angular acceleration from torque: I = (2/5) m R^2
        #   dw/dt = (5/2) * (mu * g / R) * (k x vC_hat)
        w[i] = w[i - 1] + dt * (-(5 / 2) * mu * g / R**2 * np.cross(np.array([0, 0, -R]), vC_hat))

        # Linear acceleration from friction:
        #   dv/dt = -mu * g * vC_hat
        v[i] = v[i - 1] + dt * (-mu * g * vC_hat)
        r[i] = r[i - 1] + v[i - 1] * dt
    return r[:,0], r[:,1], tau

    


r0 = [3, 5, 0]
v0 = [2, 2, 0]
w0 = [0, 0, 10]

x, y, tau = motion(r0=r0, v0=v0, w0=w0)


print(tau)








fig, ax = plt.subplots()
line1, = ax.plot([], [], lw=2, color='blue', label='Trajectory')  # Trajectory track
circle = plt.Circle((0, 0),R, color='red')  # Projectile circle
ax.add_patch(circle)   
ax.set_title('Projectile Motion')

# Dashed line in the direction of v0 passing through r0 (in x-y plane)
aim_line, = ax.plot([], [], linestyle='--', color='black', lw=1, label='v0 direction')


ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal', adjustable='box')
ax.set_ylabel("Height y")
ax.set_xlabel("Position x")
time_text = ax.text(0.02, 0.95,  "", transform=ax.transAxes)

# Track length
N = 1000  # Number of points to show in the track

def _set_aim_line():
    x0, y0 = float(r0[0]), float(r0[1])
    vx, vy = float(v0[0]), float(v0[1])
    eps = 1e-12
    if abs(vx) < eps and abs(vy) < eps:
        aim_line.set_data([], [])
        return

    candidates = []  # list of (s, x, y)
    if abs(vx) >= eps:
        for xb in (x_min, x_max):
            s = (xb - x0) / vx
            yb = y0 + s * vy
            if y_min - 1e-9 <= yb <= y_max + 1e-9:
                candidates.append((s, xb, yb))
    if abs(vy) >= eps:
        for yb in (y_min, y_max):
            s = (yb - y0) / vy
            xb = x0 + s * vx
            if x_min - 1e-9 <= xb <= x_max + 1e-9:
                candidates.append((s, xb, yb))

    if len(candidates) < 2:
        aim_line.set_data([], [])
        return

    candidates.sort(key=lambda item: item[0])
    _, x1, y1 = candidates[0]
    _, x2, y2 = candidates[-1]
    aim_line.set_data([x1, x2], [y1, y2])

def animate(i):
    # Show only the last N points of the trajectory
    start_idx = max(0, i - N)
    line1.set_data(x[start_idx:i], y[start_idx:i])  # Draw trajectory track up to current position
    circle.set_center((x[i], y[i]))  # Update projectile position

    if i == 1:
        _set_aim_line()

    time_text.set_text(f't={t[i]:.1f}s')
    return line1, aim_line, circle, time_text

###########
###########

nframes = int(Nt)
interval = 1000 * dt
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
plt.show()