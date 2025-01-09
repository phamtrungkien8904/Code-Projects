import numpy as np
import matplotlib.pyplot as plt

# Define the function f

def f(x1, x2, x3):
    f1 = np.log((x1 * (1 + x3**2)) / x2)
    f2 = x2**(x1 * x2)
    return np.array([f1, f2])

# Simulate the limit for x -> 0+ with x1 = x2 = x and x3 = 0
x_values = np.logspace(-5, 0, 500)  # x values from 10^-5 to 1
results = np.array([f(x, x, 0) for x in x_values])

# Extract f1 and f2 values
f1_values = results[:, 0]
f2_values = results[:, 1]

# Plot the results
plt.figure(figsize=(10, 5))

# Plot f1
plt.subplot(1, 2, 1)
plt.plot(x_values, f1_values, label="$f_1(x, x, 0)$")
plt.xscale("log")
plt.title("Behavior of $f_1$ as $x \to 0^+$")
plt.xlabel("x")
plt.ylabel("$f_1(x, x, 0)$")
plt.axhline(0, color='red', linestyle='--', label="Limit")
plt.legend()

# Plot f2
plt.subplot(1, 2, 2)
plt.plot(x_values, f2_values, label="$f_2(x, x, 0)$")
plt.xscale("log")
plt.title("Behavior of $f_2$ as $x \to 0^+$")
plt.xlabel("x")
plt.ylabel("$f_2(x, x, 0)$")
plt.axhline(1, color='red', linestyle='--', label="Limit")
plt.legend()

plt.tight_layout()
plt.show()
