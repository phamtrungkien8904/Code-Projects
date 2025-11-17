import numpy as np

#!/usr/bin/env python3
"""
wave-packet.py

Simple 1D free-particle Gaussian wave packet propagation using spectral (FFT) method.
Produces an animated density |psi(x,t)|^2 and the real/imag parts for visualization.

Usage: run the file with Python. Requires numpy and matplotlib.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Physical / numerical parameters (units: hbar = 1, m = 1)
hbar = 1.0
m = 1.0

# Spatial grid
L = 200.0         # domain size
N = 2048          # number of grid points (power of two recommended)
x = np.linspace(-L / 2, L / 2, N, endpoint=False)
dx = x[1] - x[0]

# Fourier-space (wave numbers) for kinetic operator
k = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)   # angular wave number
kinetic_phase = lambda dt: np.exp(-1j * (hbar * k**2) / (2.0 * m) * dt)

# Initial Gaussian wave packet parameters
x0 = -30.0         # initial center position
k0 = 2.0           # average momentum (wave number)
sigma = 5.0        # spatial width

def gaussian_packet(x, x0, k0, sigma):
    norm = (1.0 / (sigma * np.sqrt(np.pi)))**0.5  # normalization prefactor (L2)
    psi = np.exp(-(x - x0)**2 / (4.0 * sigma**2)) * np.exp(1j * k0 * (x - x0))
    # The chosen norm ensures integral |psi|^2 dx = 1 when squared with dx normalization below.
    return psi

# Initialize wavefunction and normalize discretely
psi0 = gaussian_packet(x, x0, k0, sigma)
# discrete normalization
psi0 /= np.sqrt(np.sum(np.abs(psi0)**2) * dx)

# Time-stepping parameters
dt = 0.05
n_steps = 2000
frames = 400         # how many frames to animate
steps_per_frame = max(1, n_steps // frames)

# Precompute kinetic propagator for dt
prop = kinetic_phase(dt * steps_per_frame)

# Prepare figure
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(x.min(), x.max())
ax.set_ylim(0, 1.1 * np.max(np.abs(psi0)**2))
ax.set_xlabel("x")
ax.set_ylabel(r"$|\psi(x,t)|^2$")

line_density, = ax.plot([], [], lw=2, color='C0', label=r"$|\psi|^2$")
line_re, = ax.plot([], [], lw=1, color='C1', alpha=0.6, label='Re(psi)')
line_im, = ax.plot([], [], lw=1, color='C2', alpha=0.6, label='Im(psi)')
ax.legend(loc='upper right')

psi = psi0.copy()
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def init():
    line_density.set_data([], [])
    line_re.set_data([], [])
    line_im.set_data([], [])
    time_text.set_text('')
    return line_density, line_re, line_im, time_text

def update(frame):
    global psi
    # Evolve by steps_per_frame using spectral method (free particle)
    # Apply exact propagator in k-space: psi(x,t+dt) = IFFT( exp(-i k^2 dt / (2m)) * FFT(psi) )
    psi_k = np.fft.fft(psi)
    psi_k *= prop
    psi = np.fft.ifft(psi_k)

    density = np.abs(psi)**2
    line_density.set_data(x, density)
    line_re.set_data(x, psi.real)
    line_im.set_data(x, psi.imag)
    t = (frame + 1) * steps_per_frame * dt
    time_text.set_text(f"t = {t:.2f}")
    return line_density, line_re, line_im, time_text

ani = animation.FuncAnimation(fig, update, frames=frames, init_func=init,
                              blit=True, interval=30, repeat=False)

# To save the animation, uncomment the next line (requires ffmpeg or imagemagick)
# ani.save('wave_packet.mp4', dpi=150, writer='ffmpeg', fps=30)

plt.show()