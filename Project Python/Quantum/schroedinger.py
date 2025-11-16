import numpy as np
import matplotlib.pyplot as plt


# Constant
hbar = 1.0545718e-34  # Reduced Planck's constant in J·s
me = 9.10938356e-31   # Electron mass in kg


# Parameters

nx = 100
nt = 100

x_min = -5e-9
x_max = 5e-9
dx = (x_max - x_min) / (nx - 1)

t_min = 0
t_max = 1e-15
dt = (t_max - t_min) / (nt - 1)


def schroedinger(x,t,x0,t0):
    psi = np.zeros((nx, nt),dtype=complex)
    dpsi = np.zeros((nx, nt),dtype=complex)
    ddpsi = np.zeros((nx, nt),dtype=complex)
    psi[x0][t0] = 1
    for i in range(1,nx):
        for k in range(1,nt):
            dpsi[i][k-1] = (psi[i][k-1] - psi[i-1][k-1]) / dx
            ddpsi[i][k-1] = (dpsi[i][k-1] - dpsi[i-1][k-1]) / dx
            psi[i][k] = psi[i][k-1] + dt*hbar/(2*me)*ddpsi[i][k-1] 
    return psi[x][t]
C = schroedinger(3, 2, 0, 0)


print(C)
# Example usage
x0 = 0
t0 = 0
psi = schroedinger(np.arange(nx), np.arange(nt), x0, t0)
# Plotting the probability density at final time
plt.plot(np.linspace(x_min, x_max, nx), np.abs(psi[:, 50])**2)
plt.xlabel('Position x')
plt.ylabel('Probability Density |ψ(x, t_max)|^2')
plt.title('Time Evolution of Quantum Wavefunction')
plt.grid()
plt.show()

