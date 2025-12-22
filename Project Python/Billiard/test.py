# Solve Schrödinger equation for every 1D system using Finite Difference Method and Eigenvalue Decomposition
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation




# Time steps
dt = 0.1
t_min = 0
t_max = 30
Nt = int((t_max - t_min) / dt) 
dx = 0.05
x_min = -25
x_max = 25
Nx = int((x_max - x_min) / dx)

t = np.linspace(t_min, t_max, Nt + 1)
x = np.linspace(x_min, x_max, Nx + 1)





# Solve engine
def solve():












fig, ax = plt.subplots()
line1, = ax.plot([], [], lw=2, color='red')
line2, = ax.plot([], [], lw=2, color='blue')
ax.set_title('Quantum Tunneling')



ax.legend(["Real", "Imaginary", "Magnitude"])
ax.set_xlim(x_min, x_max)
ax.set_ylim(-1.5, 1.5)
ax.set_ylabel("Amplitude")
ax.set_xlabel("Position x")
time_text = ax.text(0.02, 0.95,  "", transform=ax.transAxes)


def animate(i):
    line1.set_data(x, )
    line2.set_data(x[1:-1], np.imag(Psi[:, i]))

    time_text.set_text(f't={t[i]:.1f}s')
    return line1, line2,

###########
###########

nframes = int(Nt)
interval =  100*dt
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
plt.show()


# ani.save('gifs/tunnel.gif', writer='pillow', fps=30, dpi = 200) # Size  
