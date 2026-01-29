import numpy as np
import csv

"""
RC Low-Pass Filter (1st order) Data Generator
"""

# Set the parameters for the filter
R = 3000
C = 10e-9
tau = R*C  # Time constant
dt = 0.001*tau   # Time step (dt << tau)
t = np.arange(0, 0.01, dt)  # Time array

fe = 1000
u_e =0.8 + 0.3*np.sin(2 * np.pi *fe* t)
f0 = 10000
u_0 = 5*np.sign(np.sin(2 * np.pi *f0* t))
u_s = u_e * np.sign(u_0)






# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input", "Output"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_e[i], u_s[i]])  