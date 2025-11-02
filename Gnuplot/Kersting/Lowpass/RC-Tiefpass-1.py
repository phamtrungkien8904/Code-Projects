import numpy as np
import csv

"""
RC Low-Pass Filter (1st order) Data Generator
"""
# Set the parameters for the filter
R = 220
C = 2.2e-6
tau = R*C  # Time constant
dt = 0.01*tau   # Time step (dt << tau)
t = np.arange(0, 0.2, dt)  # Time array
f0 = 1/(2*np.pi*np.sqrt(tau))  # Limit frequency


# AC sweep
f_start = 10
f_end = 2000
df = 5
u_in = np.sin(2 * np.pi * (f_start + df*t*1000 ) * t) 

# Apply the low-pass filter
def low_pass_filter(u_in, tau, dt):
    u_C = np.zeros_like(u_in)
    for i in range(1, len(u_in)):
        u_C[i] = (dt/tau)*u_in[i] + (1 - (dt/tau))*u_C[i - 1]
    return u_C

u_out = low_pass_filter(u_in, tau, dt)

# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input", "Output"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_in[i], u_out[i]])  