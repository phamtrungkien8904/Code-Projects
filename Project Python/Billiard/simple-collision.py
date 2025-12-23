import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# 2D collision simulation (billiard, no spin)


# Time steps
dt = 0.01
t_min = 0
t_max = 10
Nt = int((t_max - t_min) / dt) 


t = np.linspace(t_min, t_max, Nt + 1)

# Parameters
x_min = 0
x_max = 5
y_min = 0
y_max = 5
R = 0.1  # radius of sphere


# Collision of N spheres
def engine(positions, velocities, num_balls):
    """
    positions: array of shape (num_balls, 2) with [x, y] for each ball
    velocities: array of shape (num_balls, 2) with [vx, vy] for each ball
    num_balls: number of balls in simulation
    """
    # Initialize arrays for positions over time
    x_all = np.zeros((num_balls, len(t)))
    y_all = np.zeros((num_balls, len(t)))
    
    # Set initial positions
    x_all[:, 0] = positions[:, 0]
    y_all[:, 0] = positions[:, 1]
    
    # Current velocities (mutable)
    v = velocities.copy()
    
    # Simulate step by step
    for i in range(1, len(t)):
        # Update positions for all balls
        x_all[:, i] = x_all[:, i-1] + v[:, 0] * dt
        y_all[:, i] = y_all[:, i-1] + v[:, 1] * dt
        
        # Check for collisions between all pairs
        for j in range(num_balls):
            for k in range(j+1, num_balls):
                dx = x_all[k, i] - x_all[j, i]
                dy = y_all[k, i] - y_all[j, i]
                distance = np.sqrt(dx**2 + dy**2)
                
                if distance <= 2*R:
                    # Collision detected - apply elastic collision physics
                    # Normal vector
                    nx = dx / distance
                    ny = dy / distance
                    
                    # Relative velocity
                    dvx = v[j, 0] - v[k, 0]
                    dvy = v[j, 1] - v[k, 1]
                    
                    # Relative velocity in collision normal direction
                    dvn = dvx * nx + dvy * ny
                    
                    # Do not resolve if velocities are separating
                    if dvn > 0:
                        # Update velocities (equal mass elastic collision)
                        v[j, 0] -= dvn * nx
                        v[j, 1] -= dvn * ny
                        v[k, 0] += dvn * nx
                        v[k, 1] += dvn * ny
                        
                        # Separate spheres to avoid overlap
                        overlap = 2*R - distance
                        x_all[j, i] -= overlap * nx / 2
                        y_all[j, i] -= overlap * ny / 2
                        x_all[k, i] += overlap * nx / 2
                        y_all[k, i] += overlap * ny / 2
        
        # Handle wall collisions (bounce)
        for j in range(num_balls):
            # Left/right walls
            if x_all[j, i] - R <= x_min:
                x_all[j, i] = x_min + R
                v[j, 0] = -v[j, 0]  # Reverse x velocity
            elif x_all[j, i] + R >= x_max:
                x_all[j, i] = x_max - R
                v[j, 0] = -v[j, 0]  # Reverse x velocity
            
            # Bottom/top walls
            if y_all[j, i] - R <= y_min:
                y_all[j, i] = y_min + R
                v[j, 1] = -v[j, 1]  # Reverse y velocity
            elif y_all[j, i] + R >= y_max:
                y_all[j, i] = y_max - R
                v[j, 1] = -v[j, 1]  # Reverse y velocity
    
    return x_all, y_all

# Define initial conditions for N balls
num_balls = 5
positions = np.array([
    [1.0, 2.5],   # Ball 1
    [3.0, 2.5],   # Ball 2
    [2.0, 1.0],   # Ball 3
    [2.0, 4.0],   # Ball 4
    [4.0, 1.5],   # Ball 5
])
velocities = np.array([
    [1.0, 0.0],    # Ball 1
    [-1.0, 0.5],   # Ball 2
    [0.5, 2.0],    # Ball 3
    [0.0, -1.5],   # Ball 4
    [-1.0, 1.0],   # Ball 5
])

x_all, y_all = engine(positions, velocities, num_balls)

# Define colors for each ball
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'gray', 'cyan']


fig, ax = plt.subplots()

# Create lines and spheres for each ball
lines = []
spheres = []
for i in range(num_balls):
    line, = ax.plot([], [], lw=2, color=colors[i % len(colors)], alpha=0.5, label=f'Ball {i+1}')
    sphere, = ax.plot([], [], 'o', markersize=R*144, color=colors[i % len(colors)])
    lines.append(line)
    spheres.append(sphere)

ax.set_title(f'Collision Simulation - {num_balls} Balls')



ax.legend()
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_ylabel("Position y")
ax.set_xlabel("Position x")
ax.set_aspect('equal')
time_text = ax.text(0.02, 0.95,  "", transform=ax.transAxes)

# Track length
N = 50  # Number of points to show in the track

def animate(i):
    # Show only the last N points of the trajectories
    start_idx = max(0, i - N)
    
    for j in range(num_balls):
        lines[j].set_data(x_all[j, start_idx:i], y_all[j, start_idx:i])
        spheres[j].set_data([x_all[j, i]], [y_all[j, i]])
        
    time_text.set_text(f't={t[i]:.2f}s')
    return (*lines, *spheres, time_text)

###########
###########

nframes = int(Nt)
interval =  100*dt
ani = animation.FuncAnimation(fig, animate, frames=nframes, repeat=False, interval=interval, blit=True)
plt.show()


# ani.save('gifs/tunnel.gif', writer='pillow', fps=30, dpi = 200) # Size  
