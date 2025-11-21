# Solve Schrödinger equation for every 1D system using Finite Difference Method and Eigenvalue Decomposition
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Free quantum wave packet

# Constant
hbar = 1.0  # Reduced Planck's constant
m = 10.0    # Particle mass



# Time steps
dt = 0.1
t_min = 0
t_max = 35
Nt = int((t_max - t_min) / dt) 
dx = 0.1
x_min = -25
x_max = 25
Nx = int((x_max - x_min) / dx) 

# Parameters

k = 10  # wave number
# w = hbar * k**2 / (2 * m)  # angular frequency
alpha = 0.5  # packet width
p = hbar * k  # momentum
V0 = p**2/(2*m)  # Kinetic energy
x0 = -10  # Initial position

t = np.linspace(t_min, t_max, Nt + 1)
x = np.linspace(x_min, x_max, Nx + 1)


# Potential function
V = np.zeros(Nx-1)
for i in range(Nx-1):
    if x[i]>-2 and x[i]<2:
        V[i] = 6*V0




# plt.plot(x,V)
# plt.xlabel('Position')
# plt.ylabel('Potential Energy')
# plt.xlim(x_min, x_max)
# plt.ylim(0, 2.5*V0)
# plt.title('Potential Energy Function')
# plt.show()

# Initial wave function

Psi0 = np.exp(1j*k*(x[1:-1]-x0)) * np.exp(-(x[1:-1]-x0)**2/(2*alpha**2))
C0 = np.sqrt(np.sum(np.abs(Psi0[:])**2*dx))  # Normalization constant
Psi0 = Psi0/C0
# plt.plot(x, np.abs(Psi0)**2)
# plt.xlabel('Position')
# plt.ylabel('Probability Density')
# plt.xlim(x_min, x_max)
# plt.ylim(0, 1)
# plt.title('Initial Probability Density of Free Particle Wave Packet')
# plt.show()

# Halmiltonian matrix
lamb = hbar**2/(2*m*dx**2)
H =lamb*(2*np.diag(np.ones(Nx-1),0) + (-1)*np.diag(np.ones(Nx-2),1) + (-1)*np.diag(np.ones(Nx-2),-1))
for i in range(Nx-2):
    H[i][i] += V[i]/lamb
E,psi = np.linalg.eigh(H)  # Eigenvalue decomposition
psi = psi.T  

c = np.zeros(Nx-1, dtype=complex)
for n in range(Nx-1):
    c[n] = np.sum(np.conj(psi[n,:]) * Psi0[:])  # Expansion coefficients

Psi = np.zeros((Nx-1, Nt), dtype=complex)
for j in range(Nt):
    for n in range(Nx-1):
        Psi[:, j] += c[n] * psi[n, :] * np.exp(-1j * E[n] * t[j] / hbar)  # Time evolution


# plt.plot(x[1:-1], np.abs(Psi[:,int(Nt/100)])**2)
# plt.plot(x[1:-1], np.abs(Psi[:,int(2*Nt/100)])**2)
# plt.plot(x[1:-1], np.abs(Psi[:,int(3*Nt/100)])**2)
# plt.plot(x[1:-1], np.abs(Psi[:,int(4*Nt/100)])**2)
# plt.plot(x[1:-1], np.abs(Psi[:,int(5*Nt/100)])**2)
# plt.plot(x[1:-1], np.abs(Psi[:,int(6*Nt/100)])**2)
# # plt.plot(x[1:-1], V)
# plt.fill_between(x[1:-1], 0, 1, where=V > 0, color='gray', alpha=0.3, transform=plt.gca().get_xaxis_transform(), label='Potential')
# plt.xlabel('Position')
# plt.ylabel('Probability Density')
# plt.xlim(x_min, x_max)
# plt.ylim(0, 1)
# plt.show()



# Define wave function (General solution)
# def solve():
#     global t, x
#     Psi = np.zeros((Nx, Nt), dtype=complex)
#     Psi0 = np.zeros(Nx, dtype=complex)
#     Psi0 = np.exp(1j*k*(x-x0))/np.sqrt(np.sqrt(np.pi)*alpha) * np.exp(-(x-x0)**2/(2*alpha**2))
#     C0 = np.sqrt(np.sum(np.abs(Psi0[:])**2*dx))  # Normalization constant
#     Psi0 = Psi0/C0
#     for i in range(0, Nx):
#         for j in range(0, Nt):
#             Psi[i][j] = 
#     C = np.sqrt(np.sum(np.abs(Psi[:,0])**2)*dx)  # Normalization constant
#     return Psi/C  


# Psi = solve() 

# # PLot test
# plt.plot(x, np.abs(Psi[:,0])**2)
# plt.xlabel('Position')  
# plt.ylabel('Probability Density')
# plt.xlim(x_min, x_max)
# plt.ylim(-1.5, 1.5)
# plt.title('Initial Probability Density of Free Particle Wave Packet')
# plt.show()



fig, ax = plt.subplots()
line1, = ax.plot([], [], lw=2, color='red')
line2, = ax.plot([], [], lw=2, color='blue')
line3, = ax.plot([], [], lw=2, color='green')
ax.legend(['Real', 'Imaginary', 'Magnitude'])
ax.set_xlim(x_min, x_max)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('Position')
ax.set_ylabel('Amplitude')

def animate(i):
    line1.set_data(x[1:-1], np.real(Psi[:, i]))
    line2.set_data(x[1:-1], np.imag(Psi[:, i]))
    line3.set_data(x[1:-1], np.abs(Psi[:, i]))
    return line1, line2, line3


nframes = int(Nt)
interval =  150*dt
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
plt.fill_between(x[1:-1], 0, 1, where=V > 0, color='gray', alpha=0.3, transform=plt.gca().get_xaxis_transform(), label='Potential')
plt.show()


ani.save('tunnel.gif', writer='pillow', fps=30, dpi=600) # Size  
