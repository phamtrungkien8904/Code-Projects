import numpy as np
import matplotlib.pyplot as plt
import csv

##### Air bubble in water #####
# Parameters
N = 5000  # Number of samples
dt = 0.00001  # Time step
t = np.zeros(N)
v = np.zeros(N)
z = np.zeros(N)
r = np.zeros(N)
rho0 = 1000  # Density of glycerol (kg/m^3)
rho = 1.2  # Density of air (kg/m^3)
g = 9.81  # Gravitational acceleration (m/s^2)
eta = 0.001  # Dynamic viscosity of glycerol (Pa.s)
R = 0.002  # Initial radius of the bubble (m)
p0 = 101325  # Atmospheric pressure (Pa)
L = 0.30 # Height of the glycerol column (m)

# Initial conditions
v[0] = 0.0  # Initial velocity (m/s)
z[0] = 0.0  # Initial height (m)
r[0] = R  # Initial radius (m)

for i in range(1, N):
    t[i] = i * dt
    v[i] = v[i-1] + dt*((rho0/rho - 1.0)*g - 9.0*eta*v[i-1]/(2.0*rho*r[i-1]**2))  # Update velocity using the equation of motion
    z[i] = z[i-1] + dt*v[i]
    # r[i] = R # Simple model
    r[i] = r[0]*(1 - rho0*g*z[i]/(p0 + rho0*g*L))**(-1/3)  # Update radius using the ideal gas law

# Time when height first reaches L (linear interpolation between samples)
crossings = np.where(z >= L)[0]
if len(crossings) > 0:
    i_cross = crossings[0]
    if i_cross == 0 or z[i_cross] == z[i_cross - 1]:
        T = t[i_cross]
    else:
        T = t[i_cross - 1] + (L - z[i_cross - 1]) * (t[i_cross] - t[i_cross - 1]) / (z[i_cross] - z[i_cross - 1])
    print(f"T_sim = {T:.6f} s")
else:
    print("The bubble did not reach the height L within the simulation time.")

T_theo = 9.0*eta*L/(2.0*g*(rho0 - rho)*R**2)
print(f"T_theo = {T_theo:.6f} s")

# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time","Velocity", "Height", "Radius"])  
    for i in range(len(t)):
        csvwriter.writerow([t[i], v[i], z[i], r[i]])  

plt.plot(t, v, label='Velocity', color='red', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity')
plt.show()

plt.plot(t, z, label='Height', color='blue', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Height (m)')
plt.title('Height')
plt.show()

plt.plot(t, r, label='Radius', color='green', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Radius (m)')
# plt.xlim(0, T*1.5) 
plt.ylim(0, R*1.5) 
plt.title('Radius')
plt.show()

