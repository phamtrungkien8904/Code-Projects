# Drude Model
import numpy as np
import matplotlib.pyplot as plt


# Plot hexagonal grid
# 1D coordinate axes for x and y in the range [-2, 2].
# Resolution
N = 400
x = np.linspace(-1, 1, N+1)
y = np.linspace(-1, 1, N+1)

# Convert 1D axes into 2D coordinate grids.
X, Y = np.meshgrid(x, y)

# Gaussian
a = 0.2 # Distance between centers of adjacent Gaussians
spacing_x = a
spacing_y = a * np.sqrt(3)
sigma = 0.03
# Build an (N+1)x(N+1) matrix: 1 means a Gaussian center at that grid point.
# Hexagonal grid spacing: centers are separated by center_step in both x and y directions.

xc1 = np.arange(x.min(), x.max() + spacing_x, spacing_x)
yc2 = np.arange(y.min(), y.max() + spacing_y, spacing_y)
xc2 = xc1 + spacing_x / 2
yc1 = yc2 + spacing_y / 2
gaussian_pos = np.zeros((N + 1, N + 1), dtype=int)

dx = x[1] - x[0]
dy = y[1] - y[0]
ix1 = np.rint((xc1 - x[0]) / dx).astype(int)
ix2 = np.rint((xc2 - x[0]) / dx).astype(int)
iy1 = np.rint((yc1 - y[0]) / dy).astype(int)
iy2 = np.rint((yc2 - y[0]) / dy).astype(int)

# Keep only centers strictly inside the discretized domain to avoid edge pile-up.
ix1 = np.unique(ix1[(ix1 >= 0) & (ix1 <= N)])
ix2 = np.unique(ix2[(ix2 >= 0) & (ix2 <= N)])
iy1 = np.unique(iy1[(iy1 >= 0) & (iy1 <= N)])
iy2 = np.unique(iy2[(iy2 >= 0) & (iy2 <= N)])

# Two staggered sublattices that form the hexagonal center pattern.
gaussian_pos[np.ix_(iy2, ix1)] = 1
gaussian_pos[np.ix_(iy1, ix2)] = 1

# Coordinates of all positions marked with 1 in gaussian_pos.
iy0, ix0 = np.where(gaussian_pos == 1)
x0 = x[ix0]
y0 = y[iy0]
Z = np.zeros_like(X)


for xc, yc in zip(x0.ravel(), y0.ravel()):
    Z += np.exp(-(X-xc)**2/(2*sigma**2))*np.exp(-(Y-yc)**2/(2*sigma**2))

# Plot only filled contour (top view).
fig, ax = plt.subplots(figsize=(8, 6))
contour = ax.contourf(X, Y, Z, levels=50, cmap="hot")
ax.set_title("2D Contour Plot")
ax.set_xlabel("x")
ax.set_ylabel("y")
fig.colorbar(contour, ax=ax, label="Probability Density")

# Improve spacing and render.
fig.tight_layout()
plt.show()