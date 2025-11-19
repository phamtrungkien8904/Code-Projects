import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Free quantum wave gaussian packet: psi(x,0) = exp(-a(x-x0)^2)

# Constant
hbar = 1.0  # Reduced Planck's constant
m = 1.0    # Particle mass



# Time steps
dt = 0.01
t_min = 0
t_max = 10
Nt = int((t_max - t_min) / dt)
dx = 0.01
x_min = -10
x_max = 10
Nx = int((x_max - x_min) / dx)

# Parameters


a = 1

t = np.linspace(t_min, t_max, Nt, endpoint=False)
x = np.linspace(x_min, x_max, Nx, endpoint=False)


# Define wave function (General solution)
def wave_1():
    global t, x
    Psi = np.zeros((Nx, Nt), dtype=complex)
    for i in range(0, Nx):
        for j in range(0, Nt):
            Psi[i][j] = (2*a/np.pi)**0.25 * np.exp(-a*x[i]**2/(1 + 2j*hbar*a*t[j]/m))/np.sqrt(1 + 2j*hbar*a*t[j]/m)
    C = np.sqrt(np.sum(np.abs(Psi[:,0])**2)*dx)  # Normalization constant
    return Psi/C  # shape (Nx, Nt)


def wave_2():
    """Propagate the initial Gaussian by evolving in Fourier space."""
    Psi = np.zeros((Nx, Nt), dtype=complex)
    psi0 = np.exp(-a * x**2)
    psi0 /= np.sqrt(np.sum(np.abs(psi0) ** 2) * dx)  # normalize initial state
    Psi[:, 0] = psi0

    k_vals = 2 * np.pi * np.fft.fftfreq(Nx, d=dx)
    psi_k = np.fft.fft(psi0)

    for j in range(1, Nt):
        phase = np.exp(-1j * hbar * k_vals**2 * t[j] / (2 * m))
        Psi[:, j] = np.fft.ifft(psi_k * phase)

    return Psi  # shape (Nx, Nt)

Psi = wave_2()  # shape (Nx, Nt)



# PLot test
plt.plot(x, np.abs(Psi[:,0])**2)
plt.xlabel('Position')  
plt.ylabel('Probability Density')
plt.xlim(x_min, x_max)
plt.ylim(-1.5, 1.5)
plt.title('Initial Probability Density of Free Particle Wave Packet')
plt.show()



fig, ax = plt.subplots()
line1, = ax.plot([], [], lw=2, color='red')
line2, = ax.plot([], [], lw=2, color='blue')
line3, = ax.plot([], [], lw=2, color='green')
ax.set_xlim(x_min, x_max)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('Position')
ax.set_ylabel('Probability Density')

def animate(i):
    line3.set_data(x, np.abs(Psi[:, i])**2)
    return line3,

interval =  1000*dt 
nframes = int(Nt)
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
# ani.save('wave.gif', writer='pillow', fps=30)
plt.show()


