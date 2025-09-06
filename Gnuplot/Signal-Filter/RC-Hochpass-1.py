import numpy as np
import csv

"""
RC High-Pass Filter (1st order) Data Generator
"""

# Set the parameters for the filter
tau = 2.0  # Time constant
dt = 0.05   # Time step
t = np.arange(0, 40, dt)  # Time array
f0 = 1/(2*np.pi*np.sqrt(tau))  # Limit frequency

# Generate the input signal (square wave)
f = 1*f0  # Frequency of the square wave
u_in = (np.sin(2 * np.pi *f* t))

# Apply the low-pass filter
def high_pass_filter(u_in, tau, dt):
    u_out = np.zeros_like(u_in)   
    u_C = np.zeros_like(u_in) 
    for i in range(1, len(u_in)):
        u_C[i] = (dt/tau)*u_in[i] + (1 - (dt/tau))*u_C[i - 1]
        u_out[i] = u_in[i] - u_C[i]
    return u_out

u_out = high_pass_filter(u_in, tau, dt)

# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input", "Output"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_in[i], u_out[i]])  