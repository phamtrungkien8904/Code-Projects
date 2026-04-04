import numpy as np
import matplotlib.pyplot as plt

# Maxwell-Boltzmann distribution in 2D
def maxwell_boltzmann(temperature, mass, v):
    kB = 1
    f = 4/np.sqrt(np.pi) * (mass / (2 * kB * temperature))**1.5 * np.exp(-mass * v**2 / (2 * kB * temperature)) * v
    return f

plt.figure(figsize=(8, 6))
temperature = 10000.0
mass = 1
v = np.linspace(0, 300, 5000)
f_v = maxwell_boltzmann(temperature, mass, v)
plt.plot(v, f_v)
plt.title("Maxwell-Boltzmann Speed Distribution (2D)")
plt.xlabel("Speed (m/s)")
plt.ylabel("Probability Density")
plt.show()
