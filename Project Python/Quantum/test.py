import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

dx = 0.1
dy = 0.1
Nx = int(20/dx)
Ny = int(20/dy)
x = np.linspace(-10,10,Nx+1)
y = np.linspace(-10,10,Ny+1)

X,Y = np.meshgrid(x,y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig, ax = plt.subplots()
Prob = ax.imshow(Z, extent=[-10,10,-10,10], origin='lower', cmap='hot', alpha=1,interpolation='nearest')
cbar = plt.colorbar(Prob, ax=ax, label='Probability Density', pad=0.02)
plt.show()