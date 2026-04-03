import numpy as np
import matplotlib.pyplot as plt

# Domain and grid
Lx, Ly = 1.0, 1.0
Nx, Ny = 1001, 1001
x = np.linspace(-Lx, Lx, Nx)
y = np.linspace(-Ly, Ly, Ny)
dx = x[1] - x[0]
dy = y[1] - y[0]
X, Y = np.meshgrid(x, y)

# Vacuum permittivity
epsilon0 = 8.854e-12

# Charge density rho(x, y) for two parallel plates
rho = np.zeros((Ny, Nx))

# Plate geometry
plate_length = 1.4
half_len = plate_length / 2
plate_sep = 0.4
plate_y_top = plate_sep / 2
plate_y_bottom = -plate_sep / 2
line_thickness = 2  # in grid points

ix = np.where(np.abs(x) <= half_len)[0]
iy_top = np.argmin(np.abs(y - plate_y_top))
iy_bottom = np.argmin(np.abs(y - plate_y_bottom))

# Opposite uniform line charges (+sigma and -sigma)
sigma = 4e-8  # C/m^2 (effective in this 2D slice model)
rho[iy_top - line_thickness:iy_top + line_thickness + 1, ix] = sigma / dy
rho[iy_bottom - line_thickness:iy_bottom + line_thickness + 1, ix] = -sigma / dy

# Dirichlet boundary condition: V = 0 at domain boundaries
V = np.zeros((Ny, Nx))

# Jacobi solver for Poisson equation
max_iter = 4000
tol = 1e-6

for it in range(max_iter):
    V_old = V.copy()

    # 5-point Laplacian stencil update
    V[1:-1, 1:-1] = 0.25 * (
        V_old[1:-1, 2:] + V_old[1:-1, :-2] +
        V_old[2:, 1:-1] + V_old[:-2, 1:-1] +
        (dx * dy) * rho[1:-1, 1:-1] / epsilon0
    )

    # Re-apply boundary condition
    V[0, :] = 0.0
    V[-1, :] = 0.0
    V[:, 0] = 0.0
    V[:, -1] = 0.0

    err = np.max(np.abs(V - V_old))
    if err < tol:
        print(f"Converged in {it + 1} iterations, max error = {err:.2e}")
        break
else:
    print(f"Reached max_iter = {max_iter}, final max error = {err:.2e}")

# Visualize potential only
fig, ax = plt.subplots(figsize=(7, 6), constrained_layout=True)

# Potential contour
cp = ax.contourf(X, Y, V, levels=80, cmap='viridis')
fig.colorbar(cp, ax=ax, label='Potential V (Volts, relative)')
ax.set_title('Potential Distribution')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')

# Draw capacitor plates
ax.plot(x[ix], np.full_like(x[ix], y[iy_top]), 'k-', lw=2, label='Plates')
ax.plot(x[ix], np.full_like(x[ix], y[iy_bottom]), 'k-', lw=2)
ax.legend(loc='upper right')
ax.set_aspect('equal')

plt.show()