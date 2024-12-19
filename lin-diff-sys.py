import numpy as np
import matplotlib.pyplot as plt

# Define matrix A
A = 0.5 * np.array([[3, -1],
                    [-1, 3]])

# Compute eigenvalues and eigenvectors of A
eigenvalues, eigenvectors = np.linalg.eig(A)

# Define the initial condition r(0)
r0 = np.array([1,3])  # Example initial condition

# Time array for plotting
t = np.linspace(0, 1, 500)

# Compute the solution r(t)
# r(t) = P * exp(Λ * t) * P^(-1) * r(0)
P = eigenvectors
P_inv = np.linalg.inv(P)
r_t = np.array([P @ np.diag(np.exp(eigenvalues * t_i)) @ P_inv @ r0 for t_i in t])

# Extract x and y components
x_t = r_t[:, 0]
y_t = r_t[:, 1]

# Plot the trajectory in phase space
plt.figure(figsize=(8, 6))
plt.plot(x_t, y_t, label="Trajectory r(t)")
plt.scatter([r0[0]], [r0[1]], color='red', label='Initial Condition r(0)')
plt.title("Solution of dr/dt = Ar")
plt.xlabel("x(t)")
plt.ylabel("y(t)")
plt.axhline(0, color='gray', linewidth=0.8, linestyle='--')
plt.axvline(0, color='gray', linewidth=0.8, linestyle='--')
plt.legend()
plt.grid()
plt.show()
