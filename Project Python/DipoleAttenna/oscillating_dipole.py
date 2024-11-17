import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.animation import FuncAnimation

import pycharge as pc

lim = 50e-9
grid_size = 1000
x, y, z = np.meshgrid(np.linspace(-lim, lim, grid_size), 0,
                      np.linspace(-lim, lim, grid_size), indexing='ij')

# Create the two oscillating charges with opposite directions
charge1 = pc.OscillatingCharge(origin=(-1e-9, 0, 0), direction=(1, 0, 0),
                               amplitude=2e-9, omega=7.49e+16)
charge2 = pc.OscillatingCharge(origin=(1e-9, 0, 0), direction=(-1, 0, 0),
                               amplitude=2e-9, omega=7.49e+16)

# Create a simulation that includes both charges
simulation = pc.Simulation([charge1, charge2])

fig, ax = plt.subplots(figsize=(5, 5))
ax.set_position([0, 0, 1, 1])
im = ax.imshow(np.zeros((grid_size, grid_size)), origin='lower',
               extent=[-lim, lim, -lim, lim], vmax=7)
ax.set_xticks([])
ax.set_yticks([])
im.set_norm(mpl.colors.LogNorm(vmin=1e5, vmax=1e8))

# Quiver plot setup for vector field
grid_size_quiver = 17
lim = 46e-9
x_quiver, y_quiver, z_quiver = np.meshgrid(
    np.linspace(-lim, lim, grid_size_quiver), 0,
    np.linspace(-lim, lim, grid_size_quiver), indexing='ij'
)
pos1 = ax.scatter(charge1.xpos(0), 0, s=5, c='red', marker='o')
pos2 = ax.scatter(charge2.xpos(0), 0, s=5, c='blue', marker='o')

def _update_animation(frame):
    text = f"\rProcessing frame {frame+1}/{n_frames}."
    sys.stdout.write(text)
    sys.stdout.flush()
    t = frame * dt

    # Calculate the electric field for both charges
    E_total = simulation.calculate_E(t=t, x=x, y=y, z=z, pcharge_field='Total')
    u = E_total[0][:, 0, :]
    v = E_total[2][:, 0, :]
    im.set_data(np.sqrt(u**2 + v**2).T)

    # Update the positions of the charges
    pos1.set_offsets((charge1.xpos(t), 0))
    pos2.set_offsets((charge2.xpos(t), 0))
    return im

def _init_animate():
    pass  # Required for FuncAnimation

n_frames = 48  # Number of frames in the animation
dt = 2 * np.pi / charge1.omega / n_frames
ani = FuncAnimation(fig, _update_animation,
                    frames=n_frames, blit=False, init_func=_init_animate)
ani.save('oscillating_dipole.gif',
         writer=animation.FFMpegWriter(fps=24), dpi=200)
