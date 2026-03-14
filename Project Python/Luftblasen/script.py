import numpy as np
import matplotlib.pyplot as plt
import csv

##### Air bubble in water #####
# Parameters
N = 100  # Number of samples
dt = 0.0001  # Time step
t = np.zeros(N)
v = np.zeros(N)
z = np.zeros(N)
r = np.zeros(N)
rho0 = 1000  # Density of water (kg/m^3)
rho = 1.2  # Density of air (kg/m^3)
g = 9.81  # Gravitational acceleration (m/s^2)
eta = 0.001  # Dynamic viscosity of water (Pa.s)
R = 0.002  # Initial radius of the bubble (m)

for i in range(N):
    t[i] = i * dt
    v[i] = v[i-1] + dt*((rho0/rho - 1.0)*g - 9.0*eta*v[i-1]/(2.0*rho*R**2))  # Update velocity using the equation of motion
    z[i] = z[i-1] + dt*v[i]

# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time","Velocity", "Height", "Radius"])  
    for i in range(len(t)):
        csvwriter.writerow([t[i], v[i], z[i], r[i]])  

plt.plot(t, v, label='Velocity')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.legend()
plt.show()

plt.plot(t, z, label='Height')
plt.xlabel('Time (s)')
plt.ylabel('Height (m)')
plt.legend()
plt.show()