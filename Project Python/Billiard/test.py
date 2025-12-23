import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Projectile


# Time steps
dt = 0.01
t_min = 0
t_max = 30
Nt = int((t_max - t_min) / dt) 


t = np.linspace(t_min, t_max, Nt + 1)

# Parameters
x_min = 0
x_max = 100
y_min = 0
y_max = 10
g = 9.81  # m/s^2

def engine(x0, y0, v0, alpha):
    alpha_rad = np.radians(alpha)
    v0x = v0 * np.cos(alpha_rad)
    v0y = v0 * np.sin(alpha_rad)

    x = x0 + v0x * t
    y = y0 + v0y * t - 0.5 * g * t**2

    return x, y

    


x, y = engine(x0=5, y0=5, v0=20, alpha=10)









fig, ax = plt.subplots()
line1, = ax.plot([], [], lw=2, color='blue', label='Trajectory')  # Trajectory track
sphere, = ax.plot([], [], 'o', markersize=15, color='red', label='Projectile')  # Projectile sphere
ax.set_title('Projectile Motion')



ax.legend()
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_ylabel("Height y")
ax.set_xlabel("Position x")
time_text = ax.text(0.02, 0.95,  "", transform=ax.transAxes)

# Track length
N = 50  # Number of points to show in the track

def animate(i):
    # Show only the last N points of the trajectory
    start_idx = max(0, i - N)
    line1.set_data(x[start_idx:i], y[start_idx:i])  # Draw trajectory track up to current position
    
    # Update sphere position to current point
    if i < len(x) and y[i] >= 0:  # Only show sphere while above ground
        sphere.set_data([x[i]], [y[i]])
    else:
        sphere.set_data([], [])  # Hide sphere when below ground
        
    time_text.set_text(f't={t[i]:.1f}s')
    return line1, sphere, time_text

###########
###########

nframes = int(Nt)
interval =  100*dt
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
plt.show()


# ani.save('gifs/tunnel.gif', writer='pillow', fps=30, dpi = 200) # Size  
