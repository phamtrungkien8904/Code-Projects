# Solve Schrödinger equation for every 1D system using Finite Difference Method and Eigenvalue Decomposition
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Free quantum wave packet with potential barrier (Tunneling effect)

# Constant
hbar = 1.0  # Reduced Planck's constant
m = 10.0    # Particle mass



# Time steps
dt = 0.1
t_min = 0
t_max = 30
Nt = int((t_max - t_min) / dt) 
dx = 0.05
x_min = -25
x_max = 25
Nx = int((x_max - x_min) / dx) 

# Parameters

k = 20  # wave number
# w = hbar * k**2 / (2 * m)  # angular frequency
alpha = 0.5  # packet width
p = hbar * k  # momentum
KE = p**2/(2*m)  # Kinetic energy
x0 = -10  # Initial position

t = np.linspace(t_min, t_max, Nt + 1)
x = np.linspace(x_min, x_max, Nx + 1)


# Potential function
V = np.zeros(Nx-1)
ratio = 18
for i in range(Nx-1):
    if x[i]>-1 and x[i]<1:
        V[i] = ratio*KE

# Configuration print 
print(f'Wave number (at center): {k}')
print(f'Packet width: {alpha}')
print(f'Barrier Potential/KE: {ratio}')


# Solve engine
def solve():
    # Initial wave function
    global t, x, dt, dx
    Psi0 = np.exp(1j*k*(x[1:-1]-x0)) * np.exp(-(x[1:-1]-x0)**2/(2*alpha**2))
    C0 = np.sqrt(np.sum(np.abs(Psi0[:])**2*dx))  # Normalization constant
    Psi0 = Psi0/C0

    # Halmiltonian matrix
    lamb = hbar**2/(2*m*dx**2)
    H =lamb*(2*np.diag(np.ones(Nx-1),0) + (-1)*np.diag(np.ones(Nx-2),1) + (-1)*np.diag(np.ones(Nx-2),-1))
    for i in range(Nx-2):
        H[i][i] += V[i]/lamb
    E,psi = np.linalg.eigh(H)  # Eigenvalue decomposition
    psi = psi.T  

    c = np.zeros(Nx-1, dtype=complex)
    for n in range(Nx-1):
        c[n] = np.sum(np.conj(psi[n,:]) * Psi0[:]*dx)  # Expansion coefficients

    Psi = np.zeros((Nx-1, Nt), dtype=complex)
    for j in range(Nt):
        for n in range(Nx-1):
            Psi[:, j] += c[n] * psi[n, :] * np.exp(-1j * E[n] * t[j] / hbar)  # Time evolution
        C = np.sqrt(np.sum(np.abs(Psi[:, j])**2*dx))  # Normalization constant
        Psi[:, j] = Psi[:, j]/C
    return Psi  


Psi = solve() 

# Transmission and Reflection Coefficients
transmittion = np.sum(np.abs(Psi[int(Nx/2):, -1])**2*dx)
reflection = np.sum(np.abs(Psi[:int(Nx/2), -1])**2*dx)
print(f'Transmission: {transmittion:.4f}')
print(f'Reflection: {reflection:.4f}')





# Plot test

plt.plot(x[1:-1], np.real(Psi[:,0]), lw=2, color='red')
plt.plot(x[1:-1], np.imag(Psi[:,0]), lw=2, color='blue')
plt.plot(x[1:-1], np.abs(Psi[:,0]), lw=2, color='green')
plt.legend(['Real', 'Imaginary', 'Magnitude'])
plt.xlabel('Position')  
plt.ylabel('Amplitude')
plt.xlim(x_min, x_max)
plt.ylim(-1.5, 1.5)
plt.fill_between(x[1:-1], 0, 1, where=V > 0, color='gray', alpha=0.5, transform=plt.gca().get_xaxis_transform(), label='Potential')
plt.title('Initial Wave Function')
plt.show()





# Probability heat map
fig, ax = plt.subplots()

ax.set_xlim(x_min, x_max)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('Position')
ax.set_ylabel('Amplitude')
time_text = ax.text(0.02, 0.95, '', color='white', transform=ax.transAxes)



# Probability heat map
Prob = ax.imshow([np.abs(Psi[:,0])**2], extent=[x[1], x[-1], -1.5, 1.5], aspect='auto', cmap='hot', alpha=1, vmin=0)
fig.colorbar(Prob, ax=ax, label='Probability Density')
plt.fill_between(x[1:-1], 0, 1, where=V > 0, color='gray', alpha=0.5, transform=plt.gca().get_xaxis_transform(), label='Potential')


def animate_heatmap(i):
    Prob.set_data([np.abs(Psi[:, i])**2])
    time_text.set_text(f't={t[i]:.1f}s')
    return Prob, time_text

nframes = int(Nt)
interval =  100*dt
ani_heatmap = animation.FuncAnimation(fig, animate_heatmap, frames=nframes, repeat=False, interval=interval, blit=True)

plt.title('Quantum Tunneling')
plt.show()


ani_heatmap.save('tunnel_heatmap.gif', writer='pillow', fps=30, dpi = 200) # Size  