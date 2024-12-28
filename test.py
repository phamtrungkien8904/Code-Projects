# Physics Playground: Interactive Physics Simulation Project

## Overview
# This script represents a basic starting point for the Physics Playground project. It includes an interactive simulation of projectile motion,
# which is one of the fundamental topics in physics. Users can modify initial velocity and angle parameters to see how they affect the trajectory.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)

def projectile_motion(v0, angle):
    """
    Calculate projectile motion trajectory.

    Parameters:
        v0 (float): Initial velocity in m/s.
        angle (float): Launch angle in degrees.

    Returns:
        tuple: Time, x, and y coordinates of the projectile.
    """
    angle_rad = np.radians(angle)
    t_flight = 2 * v0 * np.sin(angle_rad) / g  # Total flight time
    t = np.linspace(0, t_flight, num=500)  # Time intervals
    
    x = v0 * np.cos(angle_rad) * t
    y = v0 * np.sin(angle_rad) * t - 0.5 * g * t**2

    return t, x, y

# Initial parameters
v0_init = 20  # Initial velocity (m/s)
angle_init = 45  # Initial angle (degrees)

# Create the figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)
t, x, y = projectile_motion(v0_init, angle_init)
line, = plt.plot(x, y, lw=2)
ax.set_xlim(0, max(x))
ax.set_ylim(0, max(y) + 1)
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Height (m)')
ax.set_title('Projectile Motion')
ax.grid(True)

# Create the angle slider
ax_angle = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
angle_slider = Slider(ax_angle, 'Angle', 0, 90, valinit=angle_init)

# Update function for the slider
def update(val):
    angle = angle_slider.val
    t, x, y = projectile_motion(v0_init, angle)
    line.set_xdata(x)
    line.set_ydata(y)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 20)
    fig.canvas.draw_idle()

# Call update function when slider value changes
angle_slider.on_changed(update)
plt.show()
