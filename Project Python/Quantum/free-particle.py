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
psi = np.zeros((Nx, Nt), dtype=complex)

def wave():
    global t, x
    psi = np.zeros((Nx, Nt), dtype=complex)
    for i in range(0, Nx):
        for j in range(0, Nt):
            psi[i][j] = np.exp(1j*(k*x[i] - w*t[j]))/np.sqrt(alpha + 1j*beta*t[j]) * np.exp(-(x[i] - vG*t[j])**2/(4*(alpha + 1j*beta*t[j])))
    C = np.sqrt(np.sum(np.abs(psi[:,0])**2)*dx)  # Normalization constant
    return psi/C  # shape (Nx, Nt)

psi = wave()  # shape (Nx, Nt)


fig, ax = plt.subplots()
line1, = ax.plot([], [], lw=2, color='red')
line2, = ax.plot([], [], lw=2, color='blue')
line3, = ax.plot([], [], lw=2, color='green')
ax.set_xlim(x_min, x_max)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('Position')
ax.set_ylabel('Amplitude')

def animate(i):
    line1.set_data(x, np.real(psi[:, i]))
    line2.set_data(x, np.imag(psi[:, i]))
    line3.set_data(x, np.abs(psi[:, i])**2)
    return line1, line2, line3

interval =  1000*dt 
nframes = int(Nt)
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
# ani.save('wave.gif', writer='pillow', fps=30)
plt.show()


