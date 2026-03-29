# Imports for sparse-matrix eigenvalue solution of the 2D time-independent SchrÃ¶dinger equation.
import numpy as np
from scipy.sparse.linalg import splu
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
from matplotlib import animation  # Imported for potential animations in later extensions.
from mpl_toolkits.mplot3d import Axes3D  # Enables 3D plotting.
from matplotlib.animation import PillowWriter  # For saving animations as GIFs.
from scipy import sparse

# Number of grid points per axis.
N = 500

# Create a uniform 2D grid over [-2, 2] x [-2, 2].
# The '*1j' form tells NumPy to create exactly N points including endpoints.
X, Y = np.mgrid[-2:2:N*1j,-2:2:N*1j]

# Physical parameters (dimensionless units here).
m = 1.0
omega = 1.0
hbar = 1.0
k = 50.0

# Gaussian initial wave function centered at (x0, y0).
x0, y0 = -1.0, 0.0
sigma = 0.2
# Unnormalized Gaussian packet.
# psi0 = np.exp(-((X - x0)**2 + (Y - y0)**2) / (2 * sigma**2))
psi0 = np.exp(-((X - x0)**2) / (2 * sigma**2))* np.exp(1j * k * (X-x0))  # Added a phase factor for some initial momentum in x-direction.


# Normalize so that sum |psi0|^2 dA = 1.
dx = X[1, 0] - X[0, 0]
dy = Y[0, 1] - Y[0, 0]
norm = np.sqrt(np.sum(np.abs(psi0)**2) * dx * dy)
psi0 = psi0 / norm 

# Quick check/visualization of the initial probability density.
plt.figure(figsize=(5, 4))
plt.pcolormesh(X, Y, np.abs(psi0)**2, cmap='viridis', shading='auto')
plt.colorbar(label='|psi0|^2')
plt.title('Gaussian Initial Wave Function')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

# Define the 2D harmonic oscillator potential V(x, y) = 1/2 * m * omega^2 * (x^2 + y^2).
# def harmonic_oscillator(x, y, m=m, omega=omega):
#     return 0.5 * m * omega**2 * (x**2 + y**2)

def free_particle(x, y):
    return np.zeros_like(x)

def double_slit_potential(
    x,
    y,
    barrier_x=0.0,
    barrier_half_width=0.05,
    slit_width=0.05,
    slit_separation=0.2,
    v0=10000.0,
):
    """Vertical barrier with two open slits centered at y=+-slit_separation/2."""
    barrier_region = np.abs(x - barrier_x) <= barrier_half_width
    slit_1 = np.abs(y - slit_separation / 2.0) <= slit_width / 2.0
    slit_2 = np.abs(y + slit_separation / 2.0) <= slit_width / 2.0
    slit_opening = slit_1 | slit_2

    V = np.zeros_like(x, dtype=float)
    V[barrier_region & (~slit_opening)] = v0
    return V

    

# Evaluate potential on the full 2D grid using the chosen (m, omega).
# V = harmonic_oscillator(X, Y, m=m, omega=omega)
V = double_slit_potential(X, Y)

# Inspect the double-slit barrier profile.
plt.figure(figsize=(6, 5))
plt.pcolormesh(X, Y, V, shading='auto', cmap='magma')
plt.colorbar(label='V(x,y)')
plt.title('Double-Slit Potential')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

# Build sparse finite-difference operators for the Hamiltonian H = T + U.

# 1D second-derivative stencil coefficients [1, -2, 1].
diag = np.ones([N])
diags = np.array([diag, -2*diag, diag])

# Sparse tridiagonal 1D Laplacian block with finite-difference scaling.
# Including 1/dx^2 keeps the physical length scale consistent as N changes.
D = sparse.spdiags(diags, np.array([-1, 0, 1]), N, N) / (dx**2)

# 2D kinetic operator using Kronecker sum of 1D operators.
T = -(hbar**2) / (2 * m) * sparse.kronsum(D, D)

# Potential operator as diagonal sparse matrix on flattened grid values.
U = sparse.diags(V.reshape(N**2), (0))

# Total Hamiltonian matrix.
H = T + U

# Time evolution with Crank-Nicolson under the full potential.

# Time grid for evolution.
t_max = 0.5
n_steps = 220
times = np.linspace(0.0, t_max, n_steps)
dt = times[1] - times[0]

# Crank-Nicolson on the interior grid with hard-wall boundaries.
# This imposes psi=0 at the box edges and produces reflection (bounce-back).
N_in = N - 2
if N_in < 2:
    raise ValueError("N must be at least 4 to use hard-wall boundary evolution.")

# Interior operators (boundaries fixed to zero -> Dirichlet walls).
diag_in = np.ones(N_in)
D_in = sparse.spdiags([diag_in, -2 * diag_in, diag_in], [-1, 0, 1], N_in, N_in) / (dx**2)
L_in = sparse.kronsum(D_in, D_in)
V_in = V[1:-1, 1:-1].reshape(N_in**2)
H_in = -(hbar**2) / (2 * m) * L_in + sparse.diags(V_in, 0)

I_in = sparse.identity(N_in**2, format='csc')
A = (I_in + 1j * dt * H_in / (2 * hbar)).tocsc()
B = (I_in - 1j * dt * H_in / (2 * hbar)).tocsr()
solve_A = splu(A)

psi_in = psi0[1:-1, 1:-1].reshape(N_in**2).astype(complex)
psi_t_grid = np.zeros((n_steps, N, N), dtype=complex)
psi_t_grid[0, 1:-1, 1:-1] = psi_in.reshape(N_in, N_in)

for i in range(1, n_steps):
    psi_in = solve_A.solve(B @ psi_in)
    psi_t_grid[i, 1:-1, 1:-1] = psi_in.reshape(N_in, N_in)

prob_t = np.abs(psi_t_grid) # 2 is the probability density |psi|^2 at each time step on the grid.

# Optional diagnostic: norm should stay approximately constant in time.
norms = np.sum(prob_t, axis=(1, 2)) * dx * dy
print(f"Discrete norm range over time: [{norms.min():.6f}, {norms.max():.6f}]")

# Simple diagnostic for trajectory/spread through slits and reflections.
x_mean = np.sum(prob_t * X[None, :, :], axis=(1, 2)) * dx * dy
print(
    f"<x>: start {x_mean[0]:.3f}, end {x_mean[-1]:.3f}, "
    f"min {x_mean.min():.3f}, max {x_mean.max():.3f}"
)



# Animate probability density |psi(x,y,t)|^2.
fig, ax = plt.subplots(figsize=(6, 5))

# Visualization-only scaling so the packet does not look like it vanishes as it spreads.
vmax_vis = np.percentile(prob_t, 99.7)
img = ax.imshow(
    prob_t[0],
    origin='lower',
    extent=[X.min(), X.max(), Y.min(), Y.max()],
    cmap='viridis',
    aspect='equal',
    norm=PowerNorm(gamma=0.6, vmin=0.0, vmax=vmax_vis)
 )
cbar = plt.colorbar(img, ax=ax, label='|psi(x,y,t)|^2')
time_text = ax.set_title(f't = {times[0]:.2f}')
ax.set_xlabel('x')
ax.set_ylabel('y')

def update(frame):
    img.set_data(prob_t[frame])
    time_text.set_text(f't = {times[frame]:.2f}')
    return (img, time_text)

anim = animation.FuncAnimation(fig, update, frames=n_steps, interval=80, blit=False)
plt.show()

# Detector-screen intensity profile I(y) at a fixed x position to the right of the slits.
# I(y) is time-integrated probability density on that screen line.
x_screen_target = X.max() - 0.25
x_axis = X[:, 0]
y_axis = Y[0, :]
screen_idx = np.argmin(np.abs(x_axis - x_screen_target))
x_screen = x_axis[screen_idx]
if hasattr(np, 'trapezoid'):
    I_y = np.trapezoid(prob_t[:, screen_idx, :], times, axis=0)
else:
    I_y = np.trapz(prob_t[:, screen_idx, :], times, axis=0)

plt.figure(figsize=(7, 4))
plt.plot(y_axis, I_y, color='navy', lw=2)
plt.title(f'Screen Probability Profile I(y) at x = {x_screen:.3f}')
plt.xlabel('y')
plt.ylabel('I(y) = integral |psi(x_screen, y, t)|^2 dt')
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()