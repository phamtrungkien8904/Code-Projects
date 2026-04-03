# Drude Model
import numpy as np
import matplotlib.pyplot as plt

# 1D coordinate axes for x and y in the range [-2, 2].
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)

# Convert 1D axes into 2D coordinate grids.
X, Y = np.meshgrid(x, y)

# 2D Gaussian centered near (0.3, 0.3) with width sigma = 0.1 in both directions.
# This plays the role of a probability-density-like field.
Z = np.exp(-(X-0.3)**2/(2*0.1**2))*np.exp(-(Y-0.3)**2/(2*0.1**2))

# Create a wide figure to place 3D and 2D views side by side.
fig = plt.figure(figsize=(12, 5))

# Left panel: 3D surface representation of Z(x, y).
ax3d = fig.add_subplot(1, 2, 1, projection="3d")
ax3d.plot_surface(X, Y, Z, cmap="viridis")
ax3d.set_title("3D Surface Plot")
ax3d.set_xlabel("x")
ax3d.set_ylabel("y")
ax3d.set_zlabel("Probability Density")

# Right panel: filled contour (top view) of the same field.
ax2d = fig.add_subplot(1, 2, 2)
contour = ax2d.contourf(X, Y, Z, levels=50, cmap="viridis")
ax2d.set_title("2D Contour Plot")
ax2d.set_xlabel("x")
ax2d.set_ylabel("y")
fig.colorbar(contour, ax=ax2d, label="Probability Density")

# Improve spacing and render.
fig.tight_layout()
plt.show()