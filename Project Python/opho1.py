import numpy as np
import matplotlib.pyplot as plt

# Parameters
L = 100  # grid size
T_begin = 0.5
T_end = 5.0
T_step = 0.5
T_list = np.linspace(T_begin, T_end, int((T_end - T_begin) / T_step) + 1)  # temperatures to simulate
n_steps = 100000  # number of Monte Carlo steps
B = 0.1  # uniform magnetic field

'''
DO NOT TOUCH THE SUBSEQUENT CODE!
'''

J = 1.0  # interaction strength
k_B = 1.0  # Boltzmann constant

def delta_energy(grid, i, j):
    """Calculate the change in energy if the spin at (i, j) is flipped."""
    spin = grid[i, j]
    neighbors = grid[(i+1) % L, j] + grid[(i-1) % L, j] + grid[i, (j+1) % L] + grid[i, (j-1) % L]
    return 2 * J * spin * neighbors + 2 * B * spin

def monte_carlo_simulation(T):
    """Perform the Monte Carlo simulation at temperature T."""
    grid = np.random.choice([-1, 1], size=(L, L))

    for _ in range(n_steps):
        i, j = np.random.randint(0, L, 2)
        dE = delta_energy(grid, i, j)

        if dE < 0 or np.random.rand() < np.exp(-dE / (k_B * T)):
            grid[i, j] *= -1

    return grid

magnetizations = []

# Calculate number of rows needed (5 figures per row)
n_cols = 15
n_rows = int(np.ceil(len(T_list) / n_cols))

# Create the first figure (grid plots)
fig1, axes = plt.subplots(n_rows, n_cols, figsize=(18, 6 * n_rows))
axes = axes.flatten()  # Flatten the 2D array of axes for easy iteration

for ax, T in zip(axes, T_list):
    final_grid = monte_carlo_simulation(T)
    magnetization = abs(np.sum(final_grid)) / (L * L)  # Calculate average magnetization
    magnetizations.append(magnetization)
    ax.imshow(final_grid, cmap='coolwarm')
    ax.set_title(f"T = {T:.2f}")  # Format T to two decimal places
    ax.axis('off')

# If there are unused axes, remove them
for ax in axes[len(T_list):]:
    ax.remove()

# Don't call plt.show() yet

# Create the second figure (magnetization vs. temperature)
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.plot(T_list, magnetizations, marker='o')
ax2.set_xlabel('Temperature (T)')
ax2.set_ylabel('Magnetization (M)')
ax2.set_title('Magnetization vs Temperature')
ax2.grid(True)

# Now show both figures
plt.show()