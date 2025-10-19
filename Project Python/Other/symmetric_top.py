import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter

# Dynamic Parameters
M = 1  # Mass of M
R = 0.5  # Radius of M
g = np.array([0, 0, -9.81])  # Acceleration due to gravity
L = 1.5  # Length from CM to O
I = 0.5 * M * R**2
omega = 50
theta = np.pi / 6

# Initial Data
dt = 0.001  # Time resolution
N_orbit0 = 300

# Initial position and velocity
r0 = L * np.array([np.sin(theta), 0, np.cos(theta)])
v0 = np.array([0, 0, 0])
r1 = np.array([0, 0, 0])

# Prepare orbit arrays
orbit_array0 = np.zeros((3, N_orbit0))
orbit_array0[:, -1] = r0
orbit_array1 = np.zeros((3, N_orbit0))
orbit_array1[:, -1] = r1
orbit_array2 = np.zeros((3, N_orbit0))
orbit_array2[:, -1] = 2 * r0

# Create the figure
fig = plt.figure('Symmetric Top', figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d', facecolor='white')

# Plot initial points and orbits
hf0, = ax.plot([r0[0]], [r0[1]], [r0[2]], 'ro', markersize=2)
hf_orbit0, = ax.plot(orbit_array0[0, :], orbit_array0[1, :], orbit_array0[2, :], 'ko', markersize=1)
hf1, = ax.plot([r1[0]], [r1[1]], [r1[2]])
hf2, = ax.plot([2 * r0[0]], [2 * r0[1]], [2 * r0[2]])
hstick, = ax.plot([r0[0], r1[0]], [r0[1], r1[1]], [r0[2], r1[2]], 'r-', linewidth=4)
hvec, = ax.plot([r0[0], 2 * r0[0]], [r0[1], 2 * r0[1]], [r0[2], 2 * r0[2]], 'k--', linewidth=2)

# Draw axis lines
ax.plot([-3, 3], [0, 0], [0, 0], 'k-', linewidth=1)
ax.plot([0, 0], [-3, 3], [0, 0], 'k-', linewidth=1)
ax.plot([0, 0], [0, 0], [0, 3], 'k-', linewidth=1)

# Draw a circle at the top
center = 0.75 * r0
radius = R
theta0 = np.linspace(0, 2 * np.pi, 100)
v = np.linalg.svd(r0.reshape(1, -1))[2][1:3].T
points = center[:, np.newaxis] + radius * (v[:, 0:1] * np.cos(theta0) + v[:, 1:2] * np.sin(theta0))
hcirclefill = ax.plot(points[0, :], points[1, :], points[2, :], 'b-', alpha=0.5)
hcircleline, = ax.plot(points[0, :], points[1, :], points[2, :], 'r-', linewidth=2)

# Animation setup
def update(ts):
    global r0, v0
    t = ts * dt

    # Cylinder motion
    C = np.cross(r0, g)
    v0 = M * C * np.linalg.norm(r0) / (I * omega)
    r0 += v0 * dt

    # Update orbit arrays
    orbit_array0[:, :-1] = orbit_array0[:, 1:]
    orbit_array0[:, -1] = r0
    orbit_array1[:, :-1] = orbit_array1[:, 1:]
    orbit_array1[:, -1] = r1
    orbit_array2[:, :-1] = orbit_array2[:, 1:]
    orbit_array2[:, -1] = 2 * r0

    # Update plots
    hf0.set_data(orbit_array0[0, -1], orbit_array0[1, -1])
    hf0.set_3d_properties(orbit_array0[2, -1])
    hf_orbit0.set_data(orbit_array0[0, :], orbit_array0[1, :])
    hf_orbit0.set_3d_properties(orbit_array0[2, :])
    hf1.set_data(orbit_array1[0, -1], orbit_array1[1, -1])
    hf1.set_3d_properties(orbit_array1[2, -1])
    hf2.set_data(orbit_array2[0, -1], orbit_array2[1, -1])
    hf2.set_3d_properties(orbit_array2[2, -1])
    hstick.set_data([orbit_array0[0, -1], orbit_array1[0, -1]], [orbit_array0[1, -1], orbit_array1[1, -1]])
    hstick.set_3d_properties([orbit_array0[2, -1], orbit_array1[2, -1]])
    hvec.set_data([orbit_array0[0, -1], orbit_array2[0, -1]], [orbit_array0[1, -1], orbit_array2[1, -1]])
    hvec.set_3d_properties([orbit_array0[2, -1], orbit_array2[2, -1]])

    # Update circle position
    center = 0.75 * orbit_array0[:, -1]
    points = center[:, np.newaxis] + radius * (v[:, 0:1] * np.cos(theta0) + v[:, 1:2] * np.sin(theta0))
    hcirclefill[0].set_data(points[0, :], points[1, :])
    hcirclefill[0].set_3d_properties(points[2, :])
    hcircleline.set_data(points[0, :], points[1, :])
    hcircleline.set_3d_properties(points[2, :])

    return hf0, hf_orbit0, hf1, hf2, hstick, hvec, hcirclefill[0], hcircleline

# Animate and save video
ani = FuncAnimation(fig, update, frames=int(20 / dt), blit=False)
writer = FFMpegWriter(fps=30)
# ani.save('SymmetricTop.mp4', writer=writer)

plt.xlabel('$x$ (m)')
plt.ylabel('$y$ (m)')
ax.set_zlabel('$z$ (m)')
ax.set_title('Simulation')
ax.grid(True)
plt.show()