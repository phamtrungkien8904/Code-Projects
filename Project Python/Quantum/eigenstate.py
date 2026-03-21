# Solve Schrödinger equation for every 1D system using Finite Difference Method and Eigenvalue Decomposition
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('classic')
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
plt.rc('text', usetex=True) 

# Constant
hbar = 1.0  # Reduced Planck's constant
m = 1.0    # Particle mass

dx = 0.005
x_min = -5
x_max = 5
Nx = int((x_max - x_min) / dx) 
x = np.linspace(x_min, x_max, Nx + 1)


# Potential function
V = np.zeros(Nx-1)

### Basic potentials ###

# # Infinite square well potential
# for i in range(Nx-1):
#     V[i] = 0 if (x[i] >= -1 and x[i] <= 1) else 1000

# # Finite square well potential
# for i in range(Nx-1):
#     V[i] = 0 if (x[i] >= -1 and x[i] <= 1) else 30

# # Double-well potential
# for i in range(Nx-1):
#     V[i] = 0 if (np.abs(x[i]) <= 1 and np.abs(x[i]) >= 0.5) else 30 

# # Harmonic oscillator potential
# for i in range(Nx-1):
#     V[i] = 10*x[i]**2

### Advanced potentials ###

# # Infinite square well potential with step
# for i in range(Nx-1):
#     V[i] = 0 if (x[i] >= -1 and x[i] <= 0) else 1000
#     V[i] = 20 if (x[i] >= 0 and x[i] <= 1) else V[i]

# # Harmonic oscillator potential with perturbation
# for i in range(Nx-1):
#     V[i] = 10*x[i]**2 + 1*x[i]**4

# # V-shape potential
# for i in range(Nx-1):
#     V[i] = 50*np.abs(x[i])

# # Linear potential (Free fall)
# for i in range(Nx-1):
#     V[i] = 50*x[i] if x[i]>0 else 100


# # Semi-harmonic oscillator potential
# for i in range(Nx-1):
#     V[i] = 30 if x[i]<-1 else 0  
#     V[i] = 0 if x[i]>-1 and x[i]<1 else V[i]
#     V[i] = 10*x[i]**2 if x[i]>0 else V[i]

# Semi-harmonic oscillator potential 2
for i in range(Nx-1):
    V[i] = 10*x[i]**2 if x[i]>0 else 1000


# Halmiltonian matrix
lamb = hbar**2/(2*m*dx**2)
H =lamb*(np.diag(2*np.ones(Nx-1) + V/lamb,0) + (-1)*np.diag(np.ones(Nx-2),1) + (-1)*np.diag(np.ones(Nx-2),-1))
E,psi = np.linalg.eigh(H)  # Eigenvalue decomposition
psi = psi.T  

print(f'E1 - E0 = {E[1] - E[0]:.2f}')
print(f'E3 - E2 = {E[3] - E[2]:.2f}')

# Plot Eigenstates
N = 20  # Number of eigenstates to plot
plt.plot(x[1:-1], V, lw=2, label='V(x)', color='k')
plt.fill_between(x[1:-1], -10, V, color='#dbe9ff')
for i in range(N):
    plt.plot(x[1:-1], E[i] + 50*np.real(psi[i,:]), lw=2, label=f'n={i+1}, E={E[i]:.2f}')
    plt.plot(x[1:-1], np.full_like(x[1:-1], E[i]), lw=1, ls='--', color='k')
plt.xlim(-2,2)
plt.ylim(-10,50)
plt.xlabel('Position', fontsize=12)
plt.ylabel('Energy', fontsize=12)
plt.title('Eigenstates of 1D Quantum System', fontsize=12)
# plt.legend()
# plt.savefig('eigenstate.eps', format='eps', bbox_inches='tight')
plt.show()

# Plot Probability Density of Eigenstates
plt.plot(x[1:-1], V, lw=2, label='V(x)', color='k')
plt.fill_between(x[1:-1], -10, V, color='#dbe9ff')
for i in range(N):
    plt.plot(x[1:-1], E[i] + 1000*np.abs(psi[i,:])**2, lw=2, label=f'n={i+1}, E={E[i]:.2f}')
    plt.plot(x[1:-1], np.full_like(x[1:-1], E[i]), lw=1, ls='--', color='k')
plt.xlim(-2,2)
plt.ylim(-10,50)
plt.xlabel('Position', fontsize=12)
plt.ylabel('Energy', fontsize=12)
plt.title('Eigenstates of 1D Quantum System', fontsize=12)
# plt.legend()
# plt.savefig('eigenstate.eps', format='eps', bbox_inches='tight')
plt.show()

# Plot Eigenvalues
n = np.arange(N)
# f = lambda n: 0.5*(50*1.5*(n+0.5)*3.141596)**(2/3)
# plt.plot(n, f(n), color='b', label='Theoretical')

plt.plot(n, E[n], marker='o', color='r', label='Eigenvalues')
plt.xlabel('Eigenstate Index', fontsize=12)
plt.ylabel('Energy', fontsize=12)
plt.xlim(-1, N)
plt.title('Eigenvalues of 1D Quantum System (discrete)', fontsize=12)
# plt.legend()
# plt.savefig('eigenvalues.eps', format='eps', bbox_inches='tight')
plt.show()

