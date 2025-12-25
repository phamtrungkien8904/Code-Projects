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

def collision(r1, v1, r2, v2, *, R=R, e=1.0, m1=1.0, m2=1.0, eps=1e-12, separate=True):
    """Resolve a 2D collision between two equal-radius balls.

    r1, r2: (3,) or (2,) positions (only x,y used)
    v1, v2: (3,) or (2,) velocities (only x,y updated)

    Returns updated (r1, v1, r2, v2).
    """
    r1 = np.asarray(r1, dtype=float).copy()
    r2 = np.asarray(r2, dtype=float).copy()
    v1 = np.asarray(v1, dtype=float).copy()
    v2 = np.asarray(v2, dtype=float).copy()

    dr = r2[:2] - r1[:2]
    dist2 = float(np.dot(dr, dr))
    if dist2 <= eps:
        n = np.array([1.0, 0.0], dtype=float)
        dist = 0.0
    else:
        dist = float(np.sqrt(dist2))
        n = dr / dist

    min_dist = 2.0 * float(R)
    if dist > min_dist + 1e-12:
        return r1, v1, r2, v2

    vrel = v2[:2] - v1[:2]
    vn = float(np.dot(vrel, n))
    if vn >= 0.0:
        # Separating: optionally just de-overlap
        if separate and dist < min_dist - 1e-12:
            overlap = min_dist - dist
            inv_m1 = 0.0 if m1 <= 0 else 1.0 / float(m1)
            inv_m2 = 0.0 if m2 <= 0 else 1.0 / float(m2)
            inv_sum = inv_m1 + inv_m2
            if inv_sum > 0.0:
                r1[:2] -= n * overlap * (inv_m1 / inv_sum)
                r2[:2] += n * overlap * (inv_m2 / inv_sum)
        return r1, v1, r2, v2

    inv_m1 = 0.0 if m1 <= 0 else 1.0 / float(m1)
    inv_m2 = 0.0 if m2 <= 0 else 1.0 / float(m2)
    inv_sum = inv_m1 + inv_m2
    if inv_sum <= 0.0:
        return r1, v1, r2, v2

    e = float(e)
    if e < 0.0:
        e = 0.0

    # Impulse magnitude
    j = -(1.0 + e) * vn / inv_sum
    impulse = j * n
    v1[:2] -= impulse * inv_m1
    v2[:2] += impulse * inv_m2

    if separate and dist < min_dist - 1e-12:
        overlap = min_dist - dist
        r1[:2] -= n * overlap * (inv_m1 / inv_sum)
        r2[:2] += n * overlap * (inv_m2 / inv_sum)

    return r1, v1, r2, v2


def motion(r01, v01, w01, r02, v02, w02, *, e=1.0):
    """Simulate two balls with spin + table slipping friction + ball-ball collision."""
    r1 = np.zeros((len(t), 3))
    r2 = np.zeros((len(t), 3))
    v1 = np.zeros((len(t), 3))
    v2 = np.zeros((len(t), 3))
    w1 = np.zeros((len(t), 3))
    w2 = np.zeros((len(t), 3))
    vC1 = np.zeros((len(t), 3))
    vC2 = np.zeros((len(t), 3))

    r1[0] = r01
    v1[0] = v01
    w1[0] = w01
    r2[0] = r02
    v2[0] = v02
    w2[0] = w02

    Rvec = np.array([0, 0, -R], dtype=float)
    vC1[0] = v1[0] + np.cross(w1[0], Rvec)
    vC2[0] = v2[0] + np.cross(w2[0], Rvec)


    eps = 1e-12

    for i in range(1, len(t)):
        # --- Ball 1 table friction (slip) ---
        vC1_norm = np.linalg.norm(vC1[i - 1])
        if vC1_norm < eps:
            vC1[i] = np.zeros(3)
            w1[i] = w1[i - 1]
            v1[i] = v1[i - 1]
        else:
            vC1_hat = vC1[i - 1] / vC1_norm
            vC1[i] = vC1[i - 1] + dt * (-(7 / 2) * mu * g * vC1_hat)
            w1[i] = w1[i - 1] + dt * (-(5 / 2) * mu * g / R * np.cross(np.array([0, 0, -1]), vC1_hat))
            v1[i] = v1[i - 1] + dt * (-mu * g * vC1_hat)

        # --- Ball 2 table friction (slip) ---
        vC2_norm = np.linalg.norm(vC2[i - 1])
        if vC2_norm < eps:
            vC2[i] = np.zeros(3)
            w2[i] = w2[i - 1]
            v2[i] = v2[i - 1]
        else:
            vC2_hat = vC2[i - 1] / vC2_norm
            vC2[i] = vC2[i - 1] + dt * (-(7 / 2) * mu * g * vC2_hat)
            w2[i] = w2[i - 1] + dt * (-(5 / 2) * mu * g / R * np.cross(np.array([0, 0, -1]), vC2_hat))
            v2[i] = v2[i - 1] + dt * (-mu * g * vC2_hat)

        # --- Integrate positions (using previous-step velocity, consistent with your original) ---
        r1[i] = r1[i - 1] + v1[i - 1] * dt
        r2[i] = r2[i - 1] + v2[i - 1] * dt

        # --- Ball-ball collision (2D), update velocities and separate centers ---
        r1_i, v1_i, r2_i, v2_i = collision(r1[i], v1[i], r2[i], v2[i], R=R, e=e, m1=m, m2=m, eps=eps)
        r1[i], v1[i], r2[i], v2[i] = r1_i, v1_i, r2_i, v2_i

        # After collision, recompute contact velocities so friction direction next step is correct.
        vC1[i] = v1[i] + np.cross(w1[i], Rvec)
        vC2[i] = v2[i] + np.cross(w2[i], Rvec)

    vC1_norm2 = vC1[:, 0] ** 2 + vC1[:, 1] ** 2
    vC2_norm2 = vC2[:, 0] ** 2 + vC2[:, 1] ** 2
    return r1[:, 0], r1[:, 1], r2[:, 0], r2[:, 1], vC1_norm2, vC2_norm2


def motion_no_friction_no_spin(r01, v01, r02, v02, *, e=1.0):
    """Two-ball motion with no table friction and no spin (still resolves ball-ball collisions)."""
    r1 = np.zeros((len(t), 3))
    r2 = np.zeros((len(t), 3))
    v1 = np.zeros((len(t), 3))
    v2 = np.zeros((len(t), 3))

    r1[0] = r01
    r2[0] = r02
    v1[0] = v01
    v2[0] = v02

    eps = 1e-12
    for i in range(1, len(t)):
        # Constant velocities (no table friction), but collisions can change v.
        v1[i] = v1[i - 1]
        v2[i] = v2[i - 1]

        r1[i] = r1[i - 1] + v1[i - 1] * dt
        r2[i] = r2[i - 1] + v2[i - 1] * dt

        r1_i, v1_i, r2_i, v2_i = collision(r1[i], v1[i], r2[i], v2[i], R=R, e=e, m1=m, m2=m, eps=eps)
        r1[i], v1[i], r2[i], v2[i] = r1_i, v1_i, r2_i, v2_i

    return r1[:, 0], r1[:, 1], r2[:, 0], r2[:, 1]

    




r01 = [2, 5.1, 0]
v01 = [5, 0, 0]
w01 = [0, 0, 50]
r02 = [5, 5, 0]
v02 = [0, 0, 0]
w02 = [0, 0, 0]

x1, y1, x2, y2, vC1_norm, vC2_norm = motion(
    r01=r01,
    v01=v01,
    w01=w01,
    r02=r02,
    v02=v02,
    w02=w02,
    e=1.0,
)

# Dashed reference: no table friction + no spin
x1_nf, y1_nf, x2_nf, y2_nf = motion_no_friction_no_spin(
    r01=r01,
    v01=v01,
    r02=r02,
    v02=v02,
    e=1.0,
)



    


plt.plot(t, vC1_norm, label='Ball 1 |vC|^2')
plt.plot(t, vC2_norm, label='Ball 2 |vC|^2')
plt.xlabel('t (s)')
plt.ylabel('|vC|^2 (m^2/s^2)')
plt.title('Contact Point Velocity over Time')
plt.grid()
plt.legend()
plt.show()


fig, ax = plt.subplots()
line1, = ax.plot([], [], lw=2, color='blue')  # Trajectory ball 1 (with friction+spin)
line2, = ax.plot([], [], lw=2, color='red')   # Trajectory ball 2 (with friction+spin)
line1_nf, = ax.plot([], [], lw=1.5, color='blue', linestyle='--', alpha=0.6)  # No friction/spin
line2_nf, = ax.plot([], [], lw=1.5, color='red', linestyle='--', alpha=0.6)   # No friction/spin
circle1 = plt.Circle((0, 0),R, color='blue')  # Projectile circle
circle2 = plt.Circle((0, 0),R, color='red')  # Target circle
ax.add_patch(circle1)   
ax.add_patch(circle2)
ax.set_title('Projectile Motion')


ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal', adjustable='box')
ax.set_ylabel("Height y")
ax.set_xlabel("Position x")
time_text = ax.text(0.02, 0.95,  "", transform=ax.transAxes)




def animate(i):
    # Show only the last N points of the trajectory
    
    # Track length
    N = 1000  # Number of points to show in the track
    start_idx = max(0, i - N)
    line1.set_data(x1[start_idx:i], y1[start_idx:i])  # Draw trajectory track up to current position
    circle1.set_center((x1[i], y1[i]))  # Update projectile position

    line2.set_data(x2[start_idx:i], y2[start_idx:i])  # Draw trajectory track up to current position
    circle2.set_center((x2[i], y2[i]))  # Update projectile position

    line1_nf.set_data(x1_nf[start_idx:i], y1_nf[start_idx:i])
    line2_nf.set_data(x2_nf[start_idx:i], y2_nf[start_idx:i])

    time_text.set_text(f't={t[i]:.1f}s')
    return line1, line2, line1_nf, line2_nf, circle1, circle2, time_text

###########
###########

nframes = int(Nt)
interval = 1000 * dt
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
plt.show()