import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# 2D collision simulation (billiard, with spin + table slipping friction)


# Time steps
dt = 0.01
t_min = 0
t_max = 10
Nt = int((t_max - t_min) / dt) 


t = np.linspace(t_min, t_max, Nt + 1)

# Parameters
x_min = 0
x_max = 3.10
y_min = 0
y_max = 1.67
R = 57.15/1000  # radius of sphere

# Pockets (6 holes): 4 corners + 2 side pockets (middle of long rails)
pocket_radius = 2.2 * R
x_mid = 0.5 * (x_min + x_max)
pocket_centers = np.array(
    [
        [x_min, y_min],
        [x_mid, y_min],
        [x_max, y_min],
        [x_min, y_max],
        [x_mid, y_max],
        [x_max, y_max],
    ],
    dtype=float,
)


# Collision of N spheres
def engine(
    positions,
    velocities,
    omegas,
    num_balls,
    *,
    mu=0.2,
    g=9.81,
    e=1.0,
    eps=1e-12,
    pocket_centers=None,
    pocket_radius=None,
):
    """
    positions: array of shape (num_balls, 2) with [x, y] for each ball
    velocities: array of shape (num_balls, 2) with [vx, vy] for each ball
    omegas: array of shape (num_balls, 3) with [wx, wy, wz] for each ball (3D spin)
    num_balls: number of balls in simulation

    mu: kinetic (slipping) friction coefficient with the table. Applied only when vC != 0.
    g: gravitational acceleration
    e: coefficient of restitution for the normal impulse (1.0 = elastic)
    """
    m = 1.0
    I = (2.0 / 5.0) * m * R**2

    def _contact_velocity_xy(vxy, wxyz):
        # Contact point C between ball and table.
        # Rvec from center to contact: Rvec = -R k = (0, 0, -R)
        # vC = v + omega x Rvec = (vx - R*wy, vy + R*wx)
        return np.array([vxy[0] - R * wxyz[1], vxy[1] + R * wxyz[0]], dtype=float)

    def _apply_table_slip_friction(j):
        # If slipping: F = -mu * g * vhatC (per unit mass).
        # dvC/dt = -(7/2) * mu * g * vhatC for a solid sphere (I=2/5 mR^2).
        if mu <= 0.0:
            return

        vxy = np.array([v[j, 0], v[j, 1]], dtype=float)
        vC = _contact_velocity_xy(vxy, w[j])
        speed = float(np.hypot(vC[0], vC[1]))
        if speed <= eps:
            return

        vhat = vC / speed

        # Time to stop slipping (remaining) based on dvC/dt magnitude = (7/2) mu g
        tau_rem = (2.0 * speed) / (7.0 * mu * g)
        dt_eff = dt if dt <= tau_rem else tau_rem

        # Translational acceleration
        a = -mu * g * vhat
        v[j, 0] += a[0] * dt_eff
        v[j, 1] += a[1] * dt_eff

        # Angular acceleration from your torque law:
        # I dω/dt = Rvec × (-μ m g) vhatC, with Rvec = (0, 0, -R)
        Rvec = np.array([0.0, 0.0, -R], dtype=float)
        Fvec = -mu * m * g * np.array([vhat[0], vhat[1], 0.0], dtype=float)
        torque = np.cross(Rvec, Fvec)
        w[j] += (torque / I) * dt_eff

        # If we reached rolling-without-slipping within this step, enforce vC=0 exactly.
        if dt_eff < dt:
            w[j, 0] = -v[j, 1] / R
            w[j, 1] = v[j, 0] / R

    # Initialize arrays for positions over time
    x_all = np.zeros((num_balls, len(t)))
    y_all = np.zeros((num_balls, len(t)))
    w_all = np.zeros((num_balls, 3, len(t)))
    pocketed_step = np.full(num_balls, -1, dtype=int)
    
    # Set initial positions
    x_all[:, 0] = positions[:, 0]
    y_all[:, 0] = positions[:, 1]
    w_all[:, :, 0] = omegas
    
    # Current velocities (mutable)
    v = velocities.copy()
    w = omegas.copy()
    active = np.ones(num_balls, dtype=bool)

    if pocket_centers is None:
        pocket_centers = np.empty((0, 2), dtype=float)
    if pocket_radius is None:
        pocket_radius = 0.0

    def _maybe_pocket_balls(i):
        if pocket_centers.shape[0] == 0 or pocket_radius <= 0.0:
            return

        for j in range(num_balls):
            if not active[j]:
                continue
            dx = pocket_centers[:, 0] - x_all[j, i]
            dy = pocket_centers[:, 1] - y_all[j, i]
            if np.any(dx * dx + dy * dy <= pocket_radius * pocket_radius):
                active[j] = False
                pocketed_step[j] = i
                v[j, :] = 0.0
                w[j, :] = 0.0

    def _apply_pair_collision(j, k, i):
        if (not active[j]) or (not active[k]):
            return
        dx = x_all[k, i] - x_all[j, i]
        dy = y_all[k, i] - y_all[j, i]
        dist2 = dx * dx + dy * dy
        if dist2 <= 0.0:
            return
        dist = np.sqrt(dist2)
        if dist > 2 * R:
            return

        nx = dx / dist
        ny = dy / dist
        # Friction between balls is neglected (per spec): only update translational velocities.
        dvx = v[j, 0] - v[k, 0]
        dvy = v[j, 1] - v[k, 1]
        dvn = dvx * nx + dvy * ny
        if dvn <= 0.0:
            return

        factor = (1.0 + e) / 2.0
        v[j, 0] -= factor * dvn * nx
        v[j, 1] -= factor * dvn * ny
        v[k, 0] += factor * dvn * nx
        v[k, 1] += factor * dvn * ny

        overlap = 2 * R - dist
        if overlap > 0:
            x_all[j, i] -= overlap * nx / 2
            y_all[j, i] -= overlap * ny / 2
            x_all[k, i] += overlap * nx / 2
            y_all[k, i] += overlap * ny / 2

    def _apply_wall_bounce_no_friction(j, which):
        # Friction at cushions is neglected: purely reflect the normal component with restitution.
        if not active[j]:
            return
        if which == "left" or which == "right":
            v[j, 0] = -e * v[j, 0]
        elif which == "bottom" or which == "top":
            v[j, 1] = -e * v[j, 1]

    # Print initial slipping times (from vC0)
    if mu > 0.0:
        for j in range(num_balls):
            vC0 = _contact_velocity_xy(velocities[j], omegas[j])
            vC0_speed = float(np.hypot(vC0[0], vC0[1]))
            if vC0_speed > eps:
                tau = (2.0 / (7.0 * mu * g)) * vC0_speed
                print(f"Ball {j+1}: slipping time tau = {tau:.4f} s (|vC0|={vC0_speed:.4f})")
    
    # Optional air drag (linear damping). This makes even rolling balls stop over time.
    air_gamma_v = 0.8   # 1/s translational damping rate
    air_gamma_w = 0.8   # 1/s angular damping rate (optional, set 0 to disable)
    v_stop = 1e-3       # m/s snap-to-zero threshold
    w_stop = 1e-2       # rad/s snap-to-zero threshold

    def _apply_air_drag_full_dt():
        nonlocal v, w
        if air_gamma_v > 0.0:
            v *= np.exp(-air_gamma_v * dt)
            v[np.abs(v) < v_stop] = 0.0
        if air_gamma_w > 0.0:
            w *= np.exp(-air_gamma_w * dt)
            w[np.abs(w) < w_stop] = 0.0

    # Simulate step by step
    for i in range(1, len(t)):
        # Table friction acts continuously (if slipping)
        for j in range(num_balls):
            if active[j]:
                _apply_table_slip_friction(j)

        # Air drag acts continuously
        _apply_air_drag_full_dt()

        # Update positions for all balls
        x_all[:, i] = x_all[:, i-1] + v[:, 0] * dt
        y_all[:, i] = y_all[:, i-1] + v[:, 1] * dt

        # Pocket detection happens before wall bounces, so a ball can fall instead of bouncing.
        _maybe_pocket_balls(i)
        
        # Check for collisions between all pairs
        for j in range(num_balls):
            for k in range(j+1, num_balls):
                _apply_pair_collision(j, k, i)
        
        # Handle wall collisions (bounce)
        for j in range(num_balls):
            if not active[j]:
                continue
            # Left/right walls
            if x_all[j, i] - R <= x_min:
                x_all[j, i] = x_min + R
                _apply_wall_bounce_no_friction(j, "left")
            elif x_all[j, i] + R >= x_max:
                x_all[j, i] = x_max - R
                _apply_wall_bounce_no_friction(j, "right")
            
            # Bottom/top walls
            if y_all[j, i] - R <= y_min:
                y_all[j, i] = y_min + R
                _apply_wall_bounce_no_friction(j, "bottom")
            elif y_all[j, i] + R >= y_max:
                y_all[j, i] = y_max - R
                _apply_wall_bounce_no_friction(j, "top")

        w_all[:, :, i] = w
    
    return x_all, y_all, w_all, pocketed_step

# Define initial conditions: cue ball + 15-ball rack
num_balls = 16

# Layout: x axis along table length, y axis along width
y_center = 0.5 * (y_min + y_max)

# Rack (15 balls) in a triangle, touching (center spacing = 2R)
rack_apex_x = x_max * 0.75
rack_apex_y = y_center
dx_row = np.sqrt(3.0) * R

rack_positions = []
for row in range(5):
    x = rack_apex_x + row * dx_row
    y_start = rack_apex_y - row * R
    for k in range(row + 1):
        rack_positions.append([x, y_start + 2.0 * R * k])

# Cue ball
cue_x = x_max * 0.25
cue_y = y_center + 2*R

positions = np.array([[cue_x, cue_y], *rack_positions], dtype=float)

velocities = np.zeros((num_balls, 2), dtype=float)
velocities[0] = [10.0, 0.0]  # cue ball initial speed

omegas = np.zeros((num_balls, 3), dtype=float)
omegas[0] = [0.0, -10.0 / R, 0.0]  # cue ball spin

x_all, y_all, w_all, pocketed_step = engine(
    positions,
    velocities,
    omegas,
    num_balls,
    pocket_centers=pocket_centers,
    pocket_radius=pocket_radius,
)

# Define colors for each ball (cue ball first)
colors = ['black', 'yellow', 'blue', 'red', 'purple', 'orange', 'green', 'maroon', 'black',
          'yellow', 'blue', 'red', 'purple', 'orange', 'green', 'maroon']


fig, ax = plt.subplots()

# Draw pockets
for (px, py) in pocket_centers:
    ax.add_patch(plt.Circle((px, py), pocket_radius, color='black'))

# Create lines and spheres for each ball
lines = []
circles = []
for i in range(num_balls):
    line, = ax.plot([], [], lw=2, color=colors[i % len(colors)], alpha=0.5, label=f'Ball {i+1}')
    lines.append(line)
    circle = plt.Circle((x_all[i, 0], y_all[i, 0]), R, color=colors[i % len(colors)])
    ax.add_patch(circle)
    circles.append(circle)

ax.set_title(f'Collision Simulation - {num_balls} Balls')



ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_ylabel("Position y")
ax.set_xlabel("Position x")
ax.set_aspect('equal')
time_text = ax.text(0.02, 0.95,  "", transform=ax.transAxes)
pocket_text = ax.text(0.02, 0.90, "", transform=ax.transAxes)

# Track length
N = 200  # Number of points to show in the track

def animate(i):
    # Show only the last N points of the trajectories
    start_idx = max(0, i - N)
    
    pocketed_now = []
    for j in range(num_balls):
        is_pocketed = pocketed_step[j] != -1 and i >= pocketed_step[j]
        if is_pocketed:
            lines[j].set_data([], [])
            circles[j].set_visible(False)
            pocketed_now.append(j + 1)
            continue

        circles[j].set_visible(True)
        lines[j].set_data(x_all[j, start_idx:i], y_all[j, start_idx:i])
        circles[j].set_center((x_all[j, i], y_all[j, i]))
        
    time_text.set_text(f't={t[i]:.2f}s')
    pocket_text.set_text('Pocketed: ' + (', '.join(map(str, pocketed_now)) if pocketed_now else 'None'))
    return (*lines, *circles, time_text, pocket_text)

###########
###########

nframes = int(Nt)
interval =  1000*dt
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
plt.show()


# ani.save('gifs/tunnel.gif', writer='pillow', fps=30, dpi = 200) # Size  
