import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Free quantum wave packet

# Constant
hbar = 1.0  # Reduced Planck's constant
m = 1.0    # Particle mass



# Time steps
dt = 0.1
t_min = 0
t_max = 50
Nt = int((t_max - t_min) / dt)
dx = 0.1
x_min = 0
x_max = 50
Nx = int((x_max - x_min) / dx)

# Parameters

k = 5  # wave number
w = hbar * k**2 / (2 * m)  # angular frequency
vG = hbar * k / m  # group velocity
alpha = 1  # packet width
beta = hbar/(2*m) # dispersion coefficient

t = np.linspace(t_min, t_max, Nt)
x = np.linspace(x_min, x_max, Nx)


# Define wave function (General solution)
def wave_1():
    global t, x
    Psi = np.zeros((Nx, Nt), dtype=complex)
    for i in range(0, Nx):
        for j in range(0, Nt):
            Psi[i][j] = np.exp(1j*(k*x[i] - w*t[j]))/np.sqrt(alpha + 1j*beta*t[j]) * np.exp(-(x[i] - vG*t[j])**2/(4*(alpha + 1j*beta*t[j])))
    C = np.sqrt(np.sum(np.abs(Psi[:,0])**2)*dx)  # Normalization constant
    return Psi/C  # shape (Nx, Nt)


def wave_2():
    global t,x
    N = 10  # number of energy levels to sum over
    Psi = np.zeros((Nx, Nt), dtype=complex)
    psi = np.zeros((Nx, N), dtype=complex)
    for i in range(0, Nx):
        Psi[i][0] = np.exp(1j*k*x[i]) * np.exp(-(x[i]-x_max/2)**2/(2*alpha**2))  # Initial wave packet at t=0
    # Normalize initial wave function
    C = np.sqrt(np.sum(np.abs(Psi[:,0])**2)*dx)
    Psi[:,0] /= C
    # Expand initial wave function in terms of energy eigenstates
    for n in range(1, N+1):
        E_n = (n**2 * np.pi**2 * hbar**2) / (2 * m * x_max**2)
        for i in range(0, Nx):
            psi[i][n-1] = np.sqrt(2/x_max) * np.sin(n * np.pi * x[i] / x_max)
        c_n = np.sum(np.conj(psi[:,n-1]) * Psi[:,0]) * dx  # Expansion coefficient
        for j in range(0, Nt):
            for i in range(0, Nx):
                Psi[i][j] += c_n * psi[i][n-1] * np.exp(-1j * E_n * t[j] / hbar)
    return Psi  # shape (Nx, Nt)
Psi = wave_1()  # shape (Nx, Nt)


# PLot test
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
ax.set_xlim(x_min, x_max)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('Position')
ax.set_ylabel('Amplitude')

def animate(i):
    line1.set_data(x, np.real(Psi[:, i]))
    line2.set_data(x, np.imag(Psi[:, i]))
    line3.set_data(x, np.abs(Psi[:, i])**2)
    return line1, line2, line3

interval =  1000*dt 
nframes = int(Nt)
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
# ani.save('wave.gif', writer='pillow', fps=30)
plt.show()


