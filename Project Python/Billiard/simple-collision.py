import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def check_collision(circle1, circle2):
    """Check if two circles collide.

    Args:
        circle1 (tuple): A tuple (x, y, r) representing the first circle's center and radius.
        circle2 (tuple): A tuple (x, y, r) representing the second circle's center and radius.

    Returns:
        bool: True if the circles collide, False otherwise.
    """
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance <= (r1 + r2)
def plot_circles(circle1, circle2):

    """Plot two circles and indicate if they collide.

    Args:
        circle1 (tuple): A tuple (x, y, r) representing the first circle's center and radius.
        circle2 (tuple): A tuple (x, y, r) representing the second circle's center and radius.
    """
    fig, ax = plt.subplots()
    c1 = Circle((circle1[0], circle1[1]), circle1[2], color='blue', alpha=0.5)
    c2 = Circle((circle2[0], circle2[1]), circle2[2], color='red', alpha=0.5)
    
    ax.add_patch(c1)
    ax.add_patch(c2)
    
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', 'box')
    
    if check_collision(circle1, circle2):
        plt.title("Circles Collide")
    else:
        plt.title("No Collision")
    
    plt.grid()
    plt.show()
# Example usage
circle_a = (0, 0, 3)  # Circle center (0,0) with radius 3
circle_b = (4, 0, 3)  # Circle center (4,0) with radius 3
plot_circles(circle_a, circle_b)
    