import numpy as np
import matplotlib.pyplot as plt

# Parameters
L = 50  # grid size
T_list = [1.0, 5.0, 10.0]  # list of temperatures for simulation
n_steps = 100000  # number of Monte Carlo steps
B_list = [0, 0.01, 0.1] # list of uniform magnetic fields for simulation

'''

DO NOT TOUCH THE SUBSEQUENT CODE!


'''

J = 1.0  # interaction strength
k_B = 1.0  # Boltzmann constant

def delta_energy(grid, i, j, B):
    """Calculate the change in energy if the spin at (i, j) is flipped."""
    spin = grid[i, j]
    neighbors = grid[(i+1) % L, j] + grid[(i-1) % L, j] + grid[i, (j+1) % L] + grid[i, (j-1) % L]
    return 2 * J * spin * neighbors + 2 * B * spin

def monte_carlo_simulation(B, T):
    """Perform the Monte Carlo simulation at temperature T."""
    grid = np.random.choice([-1, 1], size=(L, L))

    for _ in range(n_steps):
        i, j = np.random.randint(0, L, 2)
        dE = delta_energy(grid, i, j, B)

        if dE < 0 or np.random.rand() < np.exp(-dE / (k_B * T)):
            grid[i, j] *= -1

    return grid

# Plotting and simulation for different magnetic fields and visualize the results
fig, axes = plt.subplots(len(B_list), len(T_list), figsize=(4*len(B_list), 4*len(T_list)))

for i, b in enumerate(B_list):
    for j, t in enumerate(T_list):
        ax = axes[i, j]
        final_grid = monte_carlo_simulation(b, t)
        ax.imshow(final_grid, cmap='coolwarm')
        ax.set_title(f"B = {b}, T = {t}")
        ax.axis('off')

plt.show()