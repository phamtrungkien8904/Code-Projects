# Solve Schrödinger equation for every 1D system using Finite Difference Method and Eigenvalue Decomposition
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Free quantum wave packet in harmonic oscillator potential

# Constant
hbar = 1.0  # Reduced Planck's constant
m = 5.0    # Particle mass



# Time steps
dt = 0.1
t_min = 0
t_max = 40
Nt = int((t_max - t_min) / dt) 
dx = 0.005
x_min = -10
x_max = 10
Nx = int((x_max - x_min) / dx) 

# Parameters

k = 0  # wave number at center of packet
# w = hbar * k**2 / (2 * m)  # angular frequency
p = hbar * k  # momentum
V0 = p**2/(2*m)  # Kinetic energy
x0 = -10  # Initial position
K = 1  # Spring constant

t = np.linspace(t_min, t_max, Nt + 1)
x = np.linspace(x_min, x_max, Nx + 1)


# Potential function
V = np.zeros(Nx-1)
for i in range(Nx-1):
    # V[i] = 0.5 * K * (x[i]**2)  # Harmonic oscillator potential
    V[i] = -5 if np.abs(x[i])<5 else 0  # infinite well potential
    # V[i]=-0.5 if (np.abs(x[i])<5 and np.abs(x[i])>0.1) else 0 # Double-well potential
    # V[i] = -100 if np.abs(x[i])<0.1 else 0  # Delta-Function potential

plt.plot(x[1:-1], V, lw=2, label='V(x)')
plt.legend()
plt.show()


# Halmiltonian matrix
lamb = hbar**2/(2*m*dx**2)
H =lamb*(np.diag(2*np.ones(Nx-1) + V/lamb,0) + (-1)*np.diag(np.ones(Nx-2),1) + (-1)*np.diag(np.ones(Nx-2),-1))
E,psi = np.linalg.eigh(H)  # Eigenvalue decomposition
psi = psi.T  
# Plot Eigenstates
# plt.plot(x[1:-1], np.real(psi[3,:]), lw=2, label=f'n={3}, E={E[3]:.2f}')
plt.plot(x[1:-1], np.abs(psi[30,:])**2, lw=2, label=f'n={30}, E={E[30]:.2f}')
V_map = np.tile(V, (10, 1))
plt.imshow(
    V_map,
    extent=[x[1], x[-1], -0.25, 0.25],
    origin="lower",
    aspect="auto",
    cmap="hot",
)
plt.colorbar(label="V(x)")
plt.title('First Four Eigenstates')
plt.xlim(-10,10)
plt.ylim(-0.025,0.025)
plt.legend()
plt.show()




