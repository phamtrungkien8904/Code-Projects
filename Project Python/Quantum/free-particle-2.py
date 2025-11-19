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


def integrate(func, x_start, x_end, Nx):
    dx = (x_end - x_start) /Nx 
    x_vals = np.linspace(x_start, x_end, Nx)
    y_vals = func(x_vals)
    integral = np.sum(y_vals[:]*dx)

    return integral 



# Define wave function (General solution)

## Gaussian initial wave packet (Problem 2.21 in Griffiths)
def wave_gauss_analytic():
    global t, x
    Psi = np.zeros((Nx, Nt), dtype=complex)
    for i in range(0, Nx):
        for j in range(0, Nt):
            Psi[i][j] = (2*a/np.pi)**0.25 * np.exp(-a*x[i]**2/(1 + 2j*hbar*a*t[j]/m))/np.sqrt(1 + 2j*hbar*a*t[j]/m)
    C = np.sqrt(np.sum(np.abs(Psi[:,0])**2)*dx)  # Normalization constant
    return Psi/C  

def wave_gauss_numeric():
    global t, x
    psi0 = np.exp(-a * x**2)
    psi0 /= np.sqrt(np.sum(np.abs(psi0) ** 2) * dx)
    k_max = np.pi / dx
    Nk = Nx
    k_vals = np.linspace(-k_max, k_max, Nk, endpoint=False)
    dk = k_vals[1] - k_vals[0]
    phi = np.zeros(Nk, dtype=complex)
    for idx, k in enumerate(k_vals):
        phi[idx] = np.sum(psi0 * np.exp(-1j * k * x)) * dx
    exp_kx = np.exp(1j * np.outer(x, k_vals))
    prefactor = dk / (2 * np.pi)
    Psi = np.zeros((Nx, Nt), dtype=complex)
    for j in range(Nt):
        coeff = phi * np.exp(-1j * hbar * k_vals**2 * t[j] / (2 * m))
        Psi[:, j] = prefactor * exp_kx @ coeff
    return Psi




## Square initial wave packet (Example 2.6 in Griffiths)

def wave_square_analytic():
    global t, x
    k_min = -50
    k_max = 50
    dk = 0.1
    Nk = int((k_max - k_min) / dk)
    k_vals = np.linspace(k_min, k_max, Nk, endpoint=False)
    Psi = np.zeros((Nx, Nt), dtype=complex)
    for i in range(0, Nx):
        for j in range(0, Nt):
            Psi[i][j] = integrate(func=lambda k: np.exp(1j*(k*x[i] - hbar*k**2*t[j]/(2*m)))/(2*np.pi) * (2*np.sinc(k*1/np.pi)), x_start=k_min, x_end=k_max, Nx=Nk)
    C = np.sqrt(np.sum(np.abs(Psi[:,0])**2)*dx)  # Normalization constant
    return Psi/C  
   

def wave_square_numeric():
    global t, x
    psi0 = np.zeros_like(x, dtype=complex)
    mask = np.logical_and(x >= -1, x <= 1)
    psi0[mask] = 1.0
    psi0 /= np.sqrt(np.sum(np.abs(psi0) ** 2) * dx)
    k_max = np.pi / dx
    Nk = Nx
    k_vals = np.linspace(-k_max, k_max, Nk, endpoint=False)
    dk = k_vals[1] - k_vals[0]
    phi = np.zeros(Nk, dtype=complex)
    for idx, k in enumerate(k_vals):
        phi[idx] = np.sum(psi0 * np.exp(-1j * k * x)) * dx
    exp_kx = np.exp(1j * np.outer(x, k_vals))
    prefactor = dk / (2 * np.pi)
    Psi = np.zeros((Nx, Nt), dtype=complex)
    for j in range(Nt):
        coeff = phi * np.exp(-1j * hbar * k_vals**2 * t[j] / (2 * m))
        Psi[:, j] = prefactor * exp_kx @ coeff
    return Psi


## Random initial wave packet
def wave_random():
    global t, x
    psi0 = np.exp(-a * np.abs(x))
    psi0 /= np.sqrt(np.sum(np.abs(psi0) ** 2) * dx)
    k_max = np.pi / dx
    Nk = Nx
    k_vals = np.linspace(-k_max, k_max, Nk, endpoint=False)
    dk = k_vals[1] - k_vals[0]
    phi = np.zeros(Nk, dtype=complex)
    for idx, k in enumerate(k_vals):
        phi[idx] = np.sum(psi0 * np.exp(-1j * k * x)) * dx
    exp_kx = np.exp(1j * np.outer(x, k_vals))
    prefactor = dk / (2 * np.pi)
    Psi = np.zeros((Nx, Nt), dtype=complex)
    for j in range(Nt):
        coeff = phi * np.exp(-1j * hbar * k_vals**2 * t[j] / (2 * m))
        Psi[:, j] = prefactor * exp_kx @ coeff
    return Psi

## Note that: For numerical method, at large time t, the wave may oscillate wildly due to finite k_max truncation.
## To avoid this, increase k_max (decrease dx) and Nk (increase Nx) accordingly. (increase compile time ofc)
## However, for short time t, the numerical method works well.

Psi = wave_gauss_numeric()  




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


