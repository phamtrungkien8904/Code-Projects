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
k = 20  # wave number -> classic with larger k
wavelength = 2 * np.pi / k
# w = hbar * k**2 / (2 * m)  # angular frequency
alpha = 0.5  # packet width
p = hbar * k  # momentum
KE = p**2/(2*m)  # Kinetic energy
x0 = -10  # Initial position

t = np.linspace(t_min, t_max, Nt + 1)
x = np.linspace(x_min, x_max, Nx + 1)


# Potential function
V = np.zeros(Nx-1)
ratio = 1
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
    H =lamb*(np.diag(2*np.ones(Nx-1) + V/lamb,0) + (-1)*np.diag(np.ones(Nx-2),1) + (-1)*np.diag(np.ones(Nx-2),-1))
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
print(f'Transmission Coefficient: {transmittion:.4f}')
print(f'Reflection Coefficient: {reflection:.4f}')





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




fig, (ax_wave, ax_heat) = plt.subplots(
    2,
    1,
    figsize=(10, 8),
    sharex=True,
    gridspec_kw={"height_ratios": [1, 1]},
)
line1, = ax_wave.plot([], [], lw=2, color='red')
line2, = ax_wave.plot([], [], lw=2, color='blue')
line3, = ax_wave.plot([], [], lw=2, color='green')
line4, = ax_wave.plot([], [], lw=1, color='black', linestyle='--')
ax_wave.fill_between(x[1:-1], 0, 1, where=V > 0, color='gray', alpha=0.5, transform=ax_wave.get_xaxis_transform(), label='Potential')
ax_wave.set_title('Quantum Tunneling')



ax_wave.legend(["Real", "Imaginary", "Magnitude"])
ax_wave.set_xlim(x_min, x_max)
ax_wave.set_ylim(-1.5, 1.5)
ax_wave.set_ylabel("Amplitude")
ax_heat.set_xlabel("Position")
time_text = ax_wave.text(0.02, 0.95,  "", transform=ax_wave.transAxes)

# Probability heat map
Prob = ax_heat.imshow([np.abs(Psi[:,0])**2], extent=[x[1], x[-1], -1.5, 1.5], aspect='auto', cmap='hot', alpha=1, vmin=0)
cbar = fig.colorbar(Prob, ax=[ax_wave, ax_heat], label='Probability Density', pad=0.02, fraction=0.05, shrink=0.45, anchor=(0.0, 0.0))
ax_heat.fill_between(x[1:-1], 0, 1, where=V > 0, color='gray', alpha=0.5, transform=ax_heat.get_xaxis_transform(), label='Potential')

def animate(i):
    line1.set_data(x[1:-1], np.real(Psi[:, i]))
    line2.set_data(x[1:-1], np.imag(Psi[:, i]))
    line3.set_data(x[1:-1], np.abs(Psi[:, i]))
    Prob.set_data([np.abs(Psi[:, i])**2])


    idx = np.argmax(np.abs(Psi[:, i]))
    peak_x = x[1:-1][idx]
    line4.set_data([peak_x, peak_x], [-1.5, 1.5])
    time_text.set_text(f't={t[i]:.1f}s')
    return line1, line2, line3, line4, time_text, Prob

###########
###########

nframes = int(Nt)
interval =  100*dt
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
plt.show()


ani.save('gifs/tunnel.gif', writer='pillow', fps=30, dpi = 200) # Size  
