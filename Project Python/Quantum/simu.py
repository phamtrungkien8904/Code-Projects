import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Newton: x'' + 2*alpha*x' + (2*pi*f)^2*x = 0


# Time steps
dt = 0.001
t_max = 5
N = int(t_max / dt)

f = 2.5
alpha = 1

t = np.linspace(0, t_max, N)
x = np.zeros(N)

def newton():
    global N, dt, f, alpha
    x = np.zeros(N)
    x[0] = 1.0  # Initial position
    v = np.zeros(N)
    v[0] = 0.0  # Initial velocity
    a = np.zeros(N)
    for i in range(1,N):
        a[i-1] = -2 * alpha * v[i-1] - (2 * np.pi * f)**2 * x[i-1]
        v[i] = v[i-1] + a[i-1] * dt
        x[i] = x[i-1] + v[i-1] * dt
    return x

x = newton()


fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2, color='red')
ax.set_xlim(0, t_max)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')

def animate(i):
    line.set_data(t[:i], x[:i])
    return line,

interval = 10* dt 
nframes = int(N)
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
# ani.save('damped_oscillation.gif', writer='pillow', fps=30)
plt.show()


