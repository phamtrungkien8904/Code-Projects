import numpy as np
import matplotlib.pyplot as plt


# Read outputs written by eigenstate_solver.cpp
x = np.loadtxt('x_inner.csv', delimiter=',')
V = np.loadtxt('potential.csv', delimiter=',')
E = np.loadtxt('eigenvalues.csv', delimiter=',')
psi = np.loadtxt('psi.csv', delimiter=',')

# Ensure psi is always treated as a 2D array
if psi.ndim == 1:
    psi = psi[np.newaxis, :]

N = min(10, len(E), psi.shape[0])

# Plot eigenstates
plt.figure(figsize=(10, 6))
plt.plot(x, V, lw=2, color='k', label='V(x)')
plt.fill_between(x, -10, V, color='#dbe9ff')
for i in range(N):
    plt.plot(x, E[i] + 50 * np.real(psi[i, :]), lw=2, label=f'n={i + 1}, E={E[i]:.2f}')
    plt.plot(x, np.full_like(x, E[i]), lw=1, ls='--', color='k')
plt.xlim(-5, 5)
plt.ylim(-10, 30)
plt.xlabel('Position', fontsize=12)
plt.ylabel('Energy', fontsize=12)
plt.title('Eigenstates of 1D Quantum System (C++ Output)', fontsize=12)
# plt.legend()
plt.tight_layout()
plt.show()

# Plot probability density of eigenstates
plt.figure(figsize=(10, 6))
plt.plot(x, V, lw=2, color='k', label='V(x)')
plt.fill_between(x, -10, V, color='#dbe9ff')
for i in range(N):
    plt.plot(x, E[i] + 1000 * np.abs(psi[i, :]) ** 2, lw=2, label=f'n={i + 1}, E={E[i]:.2f}')
    plt.plot(x, np.full_like(x, E[i]), lw=1, ls='--', color='k')
plt.xlim(-5, 5)
plt.ylim(-10, 30)
plt.xlabel('Position', fontsize=12)
plt.ylabel('Energy', fontsize=12)
plt.title('Probability Density of 1D Quantum System (C++ Output)', fontsize=12)
plt.tight_layout()
plt.show()
