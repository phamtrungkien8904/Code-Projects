import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(-10,10,21)
y = np.linspace(-10,10,21)

X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis')
# cbar = fig.colorbar(surf, ax=ax, label='Probability Density', pad=0.02, fraction=0.05, shrink=0.45, anchor=(0.0, 0.0))
plt.show()
