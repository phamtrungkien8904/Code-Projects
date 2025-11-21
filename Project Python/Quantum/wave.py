import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# General wave function: psi(x,t) = A(x,t) exp[i(kx - wt)]


# Time steps
dt = 0.01
t_max = 10
Nt = int(t_max / dt) + 1
dx = 0.01
x_max = 10
Nx = int(x_max / dx) + 1

c = 1  # wave speed (group velocity)
w = 1 # angular frequency
k = 10  # wave number
#k = w/c # dispersion relation, group velocity = phase velocity = c


t = np.linspace(0, t_max, Nt)
x = np.linspace(0, x_max, Nx)
psi = np.zeros((Nx, Nt), dtype=complex)

def wave():
    global t, x
    psi = np.zeros((Nx, Nt), dtype=complex)
    for i in range(0, Nx):
        for j in range(0, Nt):
            A = 1*np.exp(-(x[i] - c*t[j])**2) # Gaussian envelope
            psi[i][j] = A * np.exp(1j * (k * x[i] - w * t[j]))
    return psi  # shape (Nx, Nt)

psi = wave()  # shape (Nx, Nt)


fig, ax = plt.subplots()
line1, = ax.plot([], [], lw=2, color='red')
line2, = ax.plot([], [], lw=2, color='blue')
line3, = ax.plot([], [], lw=2, color='green')
ax.set_xlim(0, x_max)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('Position')
ax.set_ylabel('Amplitude')

def animate(i):
    line1.set_data(x, np.real(psi[:, i]))
    line2.set_data(x, np.imag(psi[:, i]))
    line3.set_data(x, np.abs(psi[:, i]))
    return line1, line2, line3

interval = 10* dt 
nframes = int(Nt)
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
# ani.save('wave.gif', writer='pillow', fps=30)
plt.show()


