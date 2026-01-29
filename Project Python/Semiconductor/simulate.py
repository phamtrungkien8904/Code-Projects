import numpy as np

# Simple 2D diffusion model for a PN junction (toy simulation)
# This models carrier diffusion, not full drift-diffusion or Poisson coupling.

nx, ny = 200, 100
dx, dy = 1.0, 1.0
dt = 0.1
steps = 800
D = 1.0  # diffusion coefficient
mu = 0.5  # mobility (toy value)
V_applied = 10.0  # applied voltage across the device (toy value)

# Concentration grid
n = np.zeros((ny, nx), dtype=float)

# Initial PN profile: left (P) low n, right (N) high n
n[:, : nx // 2] = 0.1
n[:, nx // 2 :] = 1.0

def step(u):
    lap = (
        (np.roll(u, 1, axis=0) - 2 * u + np.roll(u, -1, axis=0)) / dy**2
        + (np.roll(u, 1, axis=1) - 2 * u + np.roll(u, -1, axis=1)) / dx**2
    )

    # Apply a constant electric field from the voltage across the x-direction
    Lx = dx * (nx - 1)
    Ex = -V_applied / Lx

    # Upwind scheme for drift (advection) term
    if Ex >= 0:
        dudx = (u - np.roll(u, 1, axis=1)) / dx
    else:
        dudx = (np.roll(u, -1, axis=1) - u) / dx

    drift = -mu * Ex * dudx

    return u + D * dt * lap + dt * drift

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(figsize=(8, 4))
im = ax.imshow(n, origin="lower", cmap="viridis", aspect="auto", vmin=0.0, vmax=1.0)
cbar = plt.colorbar(im, ax=ax, label="Carrier concentration")
title = ax.set_title("PN Diffusion: step 0")
ax.set_xlabel("x")
ax.set_ylabel("y")

def apply_boundaries(u):
    # Dirichlet boundaries: fixed concentrations at left/right contacts
    u[:, 0] = 0.1
    u[:, -1] = 1.0
    # Neumann boundaries (zero-gradient) at top/bottom
    u[0, :] = u[1, :]
    u[-1, :] = u[-2, :]
    return u

def update(frame):
    global n
    n = step(n)
    n = apply_boundaries(n)
    im.set_data(n)
    title.set_text(f"PN Diffusion: step {frame + 1}")
    return im, title

ani = FuncAnimation(fig, update, frames=steps, interval=30, blit=False, repeat=False)

plt.tight_layout()
plt.show()

# Save final concentration to a CSV for visualization
np.savetxt("pn_diffusion_final.csv", n, delimiter=",")

print("Simulation complete. Output: pn_diffusion_final.csv")