import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# General wave function: psi(x,t) = A exp[i(kx - wt)]


# Time steps
dt = 0.001
t_max = 1
Nt = int(t_max / dt)
dx = 0.001
x_max = 1
Nx = int(x_max / dx)

c = 1  # wave speed
k = 1
w = k*c
A = 1

t = np.linspace(0, t_max, Nt)
x = np.linspace(0, x_max, Nx)
psi = np.zeros((Nx, Nt), dtype=complex)

def wave():
    global t, x
    psi = np.zeros((Nx, Nt), dtype=complex)
    for i in range(0, Nx):
        for k in range(0, Nt):
            psi[i][k] = A * np.exp(1j * (k * x[i] - w * t[k]))
    return psi  # shape (Nx, Nt)

psi = wave()  # shape (Nx, Nt)


print(x[500])
print(psi[500][0])
print(A*np.exp(1j*(k*x[500]-w*t[0])))

# fig, ax = plt.subplots()
# line1, = ax.plot([], [], lw=2, color='red')
# line2, = ax.plot([], [], lw=2, color='blue')
# line3, = ax.plot([], [], lw=2, color='green')
# ax.set_xlim(0, x_max)
# ax.set_ylim(-1.5, 1.5)
# ax.set_xlabel('Position')
# ax.set_ylabel('Amplitude')

# def animate(i):
#     line3.set_data(t[i], np.abs(psi[100][i]))
#     return line3,

# interval = 10* dt 
# nframes = int(Nt)
# ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
# # ani.save('damped_oscillation.gif', writer='pillow', fps=30)
# plt.show()


