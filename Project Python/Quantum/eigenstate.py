# Solve Schrödinger equation for every 1D system using Finite Difference Method and Eigenvalue Decomposition
import numpy as np
import matplotlib.pyplot as plt

# Constant
hbar = 1.0  # Reduced Planck's constant
m = 1.0    # Particle mass

# Time steps
dt = 0.1
t_min = 0
t_max = 40
Nt = int((t_max - t_min) / dt) 
dx = 0.005
x_min = -5
x_max = 5
Nx = int((x_max - x_min) / dx) 
t = np.linspace(t_min, t_max, Nt + 1)
x = np.linspace(x_min, x_max, Nx + 1)


# Potential function
V = np.zeros(Nx-1)
for i in range(Nx-1):
    # V[i] = 0.5 * K * (x[i]**2)  # Harmonic oscillator potential
    V[i] = 20 if np.abs(x[i])>1 else 0  # infinite well potential
    # V[i]=-0.5 if (np.abs(x[i])<5 and np.abs(x[i])>0.1) else 0 # Double-well potential
    # V[i] = -100 if np.abs(x[i])<0.1 else 0  # Delta-Function potential



# Halmiltonian matrix
lamb = hbar**2/(2*m*dx**2)
H =lamb*(np.diag(2*np.ones(Nx-1) + V/lamb,0) + (-1)*np.diag(np.ones(Nx-2),1) + (-1)*np.diag(np.ones(Nx-2),-1))
E,psi = np.linalg.eigh(H)  # Eigenvalue decomposition
psi = psi.T  

# Plot Eigenstates
plt.plot(x[1:-1], V, lw=2, label='V(x)')
for i in range(20):
    plt.plot(x[1:-1], E[i] + 50*np.real(psi[i,:]), lw=2, label=f'n={i+1}, E={E[i]:.2f}')
plt.xlim(-2,2)
plt.ylim(0,30)
# plt.legend()
plt.show()




