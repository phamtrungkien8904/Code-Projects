# Imports for sparse-matrix time evolution of the 2D Schrodinger equation.
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import splu
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
from matplotlib import animation

# Number of grid points per axis.
N = 1000

# Create a uniform 2D grid over [-2, 2] x [-2, 2].
# The '*1j' form tells NumPy to create exactly N points including endpoints.
X, Y = np.mgrid[-2:2:N*1j,-2:2:N*1j]

# Physical parameters (dimensionless units).
m = 1.0
hbar = 1.0
q = 1.0
k = 42.0

# Gaussian initial wave function centered at (x0, y0).
x0, y0 = -1.55, 0.0
sigma = 0.18
psi0 = np.exp(-((X - x0) ** 2 + (Y - y0) ** 2) / (2 * sigma**2)) * np.exp(1j * k * (X - x0))


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

def double_slit_potential(
    x,
    y,
    barrier_x=-0.7,
    barrier_half_width=0.06,
    slit_width=0.16,
    slit_separation=0.52,
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


def solenoid_core_potential(x, y, x_c=0.15, y_c=0.0, radius=0.12, v0=15000.0):
    """Impenetrable core representing a confined-flux solenoid region."""
    r2 = (x - x_c) ** 2 + (y - y_c) ** 2
    V = np.zeros_like(x, dtype=float)
    V[r2 <= radius**2] = v0
    return V


def aharonov_bohm_vector_potential(
    x,
    y,
    alpha,
    x_c=0.15,
    y_c=0.0,
    core_radius=0.12,
):
    """
    Vector potential for a thin flux tube with reduced flux alpha = Phi / Phi0.
    Outside the core: A_phi = Phi/(2*pi*r), with Phi0 = 2*pi*hbar/q.
    """
    xr = x - x_c
    yr = y - y_c
    r2 = xr**2 + yr**2
    r2_safe = np.maximum(r2, core_radius**2)

    # Phi/(2*pi) = alpha * hbar / q in these units.
    pref = alpha * hbar / q
    ax = -pref * yr / r2_safe
    ay = pref * xr / r2_safe
    return ax, ay


def build_hamiltonian_with_gauge(v_grid, ax_grid, ay_grid, dx, dy, m, hbar, q):
    """Gauge-covariant finite-difference Hamiltonian using link-variable phases."""
    n_full = v_grid.shape[0]
    n_in = n_full - 2

    v_in = v_grid[1:-1, 1:-1]
    ax_in = ax_grid[1:-1, 1:-1]
    ay_in = ay_grid[1:-1, 1:-1]

    tx = hbar**2 / (2.0 * m * dx**2)
    ty = hbar**2 / (2.0 * m * dy**2)

    rows = []
    cols = []
    data = []

    def idx(i, j):
        return i * n_in + j

    for i in range(n_in):
        for j in range(n_in):
            p = idx(i, j)
            diag = 2.0 * tx + 2.0 * ty + v_in[i, j]

            # +x neighbor
            if i < n_in - 1:
                phase_x = np.exp(-1j * q * ax_in[i, j] * dx / hbar)
                rows.append(p)
                cols.append(idx(i + 1, j))
                data.append(-tx * phase_x)

            # -x neighbor
            if i > 0:
                phase_xm = np.exp(1j * q * ax_in[i - 1, j] * dx / hbar)
                rows.append(p)
                cols.append(idx(i - 1, j))
                data.append(-tx * phase_xm)

            # +y neighbor
            if j < n_in - 1:
                phase_y = np.exp(-1j * q * ay_in[i, j] * dy / hbar)
                rows.append(p)
                cols.append(idx(i, j + 1))
                data.append(-ty * phase_y)

            # -y neighbor
            if j > 0:
                phase_ym = np.exp(1j * q * ay_in[i, j - 1] * dy / hbar)
                rows.append(p)
                cols.append(idx(i, j - 1))
                data.append(-ty * phase_ym)

            rows.append(p)
            cols.append(p)
            data.append(diag)

    h_in = sparse.csr_matrix((data, (rows, cols)), shape=(n_in**2, n_in**2), dtype=complex)
    return h_in


def evolve_case(v_grid, alpha, psi_initial, times, dx, dy):
    """Run Crank-Nicolson evolution for one magnetic-flux value alpha."""
    n_full = v_grid.shape[0]
    n_in = n_full - 2
    dt_local = times[1] - times[0]

    ax, ay = aharonov_bohm_vector_potential(X, Y, alpha=alpha)
    h_in = build_hamiltonian_with_gauge(v_grid, ax, ay, dx, dy, m=m, hbar=hbar, q=q)

    i_in = sparse.identity(n_in**2, format='csc', dtype=complex)
    a_mat = (i_in + 1j * dt_local * h_in / (2.0 * hbar)).tocsc()
    b_mat = (i_in - 1j * dt_local * h_in / (2.0 * hbar)).tocsr()
    solver = splu(a_mat)

    psi_in = psi_initial[1:-1, 1:-1].reshape(n_in**2).astype(complex)
    psi_t = np.zeros((len(times), n_full, n_full), dtype=complex)
    psi_t[0, 1:-1, 1:-1] = psi_in.reshape(n_in, n_in)

    for it in range(1, len(times)):
        psi_in = solver.solve(b_mat @ psi_in)
        psi_t[it, 1:-1, 1:-1] = psi_in.reshape(n_in, n_in)

    prob = np.abs(psi_t) ** 2
    norms_local = np.sum(prob, axis=(1, 2)) * dx * dy
    return prob, norms_local


# Compose AB setup: slit splitter + impenetrable solenoid core.
V = double_slit_potential(X, Y) + solenoid_core_potential(X, Y)

# Inspect the double-slit barrier profile.
plt.figure(figsize=(6, 5))
plt.pcolormesh(X, Y, V, shading='auto', cmap='magma')
plt.colorbar(label='V(x,y)')
plt.title('Double-Slit Potential')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

# Time grid for evolution.
t_max = 0.6
n_steps = 240
times = np.linspace(0.0, t_max, n_steps)
dt = times[1] - times[0]

# Run two cases to reveal the AB phase shift in the interference pattern.
alpha_ref = 0.0
alpha_ab = 0.35

prob_ref, norms_ref = evolve_case(V, alpha_ref, psi0, times, dx, dy)
prob_ab, norms_ab = evolve_case(V, alpha_ab, psi0, times, dx, dy)

# Optional diagnostic: norm should stay approximately constant in time.
print(f"alpha={alpha_ref:.2f} norm range: [{norms_ref.min():.6f}, {norms_ref.max():.6f}]")
print(f"alpha={alpha_ab:.2f} norm range: [{norms_ab.min():.6f}, {norms_ab.max():.6f}]")

# Simple diagnostic for trajectory/spread through slits and reflections.
x_mean_ref = np.sum(prob_ref * X[None, :, :], axis=(1, 2)) * dx * dy
x_mean_ab = np.sum(prob_ab * X[None, :, :], axis=(1, 2)) * dx * dy
print(
    f"<x> alpha={alpha_ref:.2f}: start {x_mean_ref[0]:.3f}, end {x_mean_ref[-1]:.3f}, "
    f"min {x_mean_ref.min():.3f}, max {x_mean_ref.max():.3f}"
)
print(
    f"<x> alpha={alpha_ab:.2f}: start {x_mean_ab[0]:.3f}, end {x_mean_ab[-1]:.3f}, "
    f"min {x_mean_ab.min():.3f}, max {x_mean_ab.max():.3f}"
)



# Animate probability density |psi(x,y,t)|^2 for the flux-on case.
fig, ax = plt.subplots(figsize=(6, 5))

# Visualization-only scaling so the packet does not look like it vanishes as it spreads.
vmax_vis = np.percentile(prob_ab, 99.7)
img = ax.imshow(
    prob_ab[0],
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
    img.set_data(prob_ab[frame])
    time_text.set_text(f't = {times[frame]:.2f}')
    return (img, time_text)

anim = animation.FuncAnimation(fig, update, frames=n_steps, interval=80, blit=False)
plt.show()

# Detector-screen intensity profiles at a fixed x position to the right.
# Compare alpha=0 and alpha!=0 to show AB fringe displacement.
x_screen_target = X.max() - 0.25
x_axis = X[:, 0]
y_axis = Y[0, :]
screen_idx = np.argmin(np.abs(x_axis - x_screen_target))
x_screen = x_axis[screen_idx]
if hasattr(np, 'trapezoid'):
    i_y_ref = np.trapezoid(prob_ref[:, screen_idx, :], times, axis=0)
    i_y_ab = np.trapezoid(prob_ab[:, screen_idx, :], times, axis=0)
else:
    i_y_ref = np.trapz(prob_ref[:, screen_idx, :], times, axis=0)
    i_y_ab = np.trapz(prob_ab[:, screen_idx, :], times, axis=0)

plt.figure(figsize=(7, 4))
plt.plot(y_axis, i_y_ref, color='black', lw=2, label=f'alpha={alpha_ref:.2f}')
plt.plot(y_axis, i_y_ab, color='crimson', lw=2, label=f'alpha={alpha_ab:.2f}')
plt.title(f'Aharonov-Bohm Fringe Shift at x = {x_screen:.3f}')
plt.xlabel('y')
plt.ylabel('I(y) = integral |psi(x_screen, y, t)|^2 dt')
plt.grid(alpha=0.25)
plt.legend()
plt.tight_layout()
plt.show()