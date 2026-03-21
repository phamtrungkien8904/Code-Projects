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

def potential_0():
    for i in range(Nx-1):
      V[i] = 0.5*x[i]**2
    return V

alpha = 0.005
def potential_per():
    for i in range(Nx-1):
      V[i] = 0.5*x[i]**2 + alpha*x[i]**4
    return V

### Basic potentials

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

### Advanced potentials

# # Infinite square well potential with step
# for i in range(Nx-1):
#     V[i] = 0 if (x[i] >= -1 and x[i] <= 0) else 1000
#     V[i] = 20 if (x[i] >= 0 and x[i] <= 1) else V[i]

# # Harmonic oscillator potential with perturbation
# for i in range(Nx-1):
#     V[i] = 10*x[i]**2 + 1*x[i]**4



# Halmiltonian matrix
def solve(V):
    lamb = hbar**2/(2*m*dx**2)
    H =lamb*(np.diag(2*np.ones(Nx-1) + V/lamb,0) + (-1)*np.diag(np.ones(Nx-2),1) + (-1)*np.diag(np.ones(Nx-2),-1))
    E,psi = np.linalg.eigh(H)  # Eigenvalue decomposition
    psi = psi.T 
    return E, psi 

E_0, psi_0 = solve(potential_0())
E_per, psi_per = solve(potential_per())

k = 5
theory = 0.75*alpha*(2*k**2 + 2*k + 1)
print(f'E_per[5] - E_0[5] = {E_per[5] - E_0[5]:.4f}')
print(f'First-order energy correction (Theory): {theory:.4f}')


# Plot Eigenstates
N = 4  # Number of eigenstates to plot
plt.plot(x[1:-1], potential_0(), lw=2, label='V(x)', color='k')
plt.plot(x[1:-1], potential_per(), lw=2, label='V\'(x)', color='k', ls='--')
# plt.fill_between(x[1:-1], -10, V, color='#dbe9ff')
for i in range(N):
    plt.plot(x[1:-1], E_0[i] + 3*np.real(psi_0[i,:]), lw=2, label=f'n={i+1}, E={E_0[i]:.2f}')
    plt.plot(x[1:-1], np.full_like(x[1:-1], E_0[i]), lw=1, ls='--', color='k')
    plt.plot(x[1:-1], E_per[i] + 3*np.real(psi_per[i,:]), lw=2, label=f'n={i+1}, E\'={E_per[i]:.2f}', ls='--')
    plt.plot(x[1:-1], np.full_like(x[1:-1], E_per[i]), lw=1, ls='--', color='k')
plt.xlim(-2,2)
plt.ylim(0,2)
plt.xlabel('Position', fontsize=12)
plt.ylabel('Energy', fontsize=12)
plt.title('Eigenstates of 1D Quantum System', fontsize=12)
# plt.legend()
# plt.savefig('eigenstate.eps', format='eps', bbox_inches='tight')
plt.show()

# # Plot Probability Density of Eigenstates
# plt.plot(x[1:-1], V, lw=2, label='V(x)', color='k')
# plt.fill_between(x[1:-1], -10, V, color='#dbe9ff')
# for i in range(N):
#     plt.plot(x[1:-1], E[i] + 1000*np.abs(psi[i,:])**2, lw=2, label=f'n={i+1}, E={E[i]:.2f}')
#     plt.plot(x[1:-1], np.full_like(x[1:-1], E[i]), lw=1, ls='--', color='k')
# plt.xlim(-2,2)
# plt.ylim(-10,50)
# plt.xlabel('Position', fontsize=12)
# plt.ylabel('Energy', fontsize=12)
# plt.title('Eigenstates of 1D Quantum System', fontsize=12)
# # plt.legend()
# # plt.savefig('eigenstate.eps', format='eps', bbox_inches='tight')
# plt.show()

# # Plot Eigenvalues
# n = np.arange(N)
# plt.plot(n, E[n], marker='o', color='r', label='Eigenvalues')
# plt.xlabel('Eigenstate Index', fontsize=12)
# plt.ylabel('Energy', fontsize=12)
# plt.xlim(-1, N)
# plt.title('Eigenvalues of 1D Quantum System (discrete)', fontsize=12)
# # plt.legend()
# # plt.savefig('eigenvalues.eps', format='eps', bbox_inches='tight')
# plt.show()

