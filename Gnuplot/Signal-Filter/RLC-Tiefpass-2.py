import numpy as np
import csv

"""
RLC Low-Pass Filter (2nd order) Data Generator
tau_L*tau_C* d^2u_out/dt^2 + (tau_C)*du_out/dt + u_out = u_in
"""

# Set the parameters for the filter
tau_C = 2.0  # Capacitor time constant
tau_L = 0.5  # Inductance time constant
dt = 0.05   # Time step
t = np.arange(0, 40, dt)  # Time array

# Generate the input signal (square wave)
f = 1/20  # Frequency of the square wave
u_in = (np.sin(2 * np.pi *f* t))

# Apply the low-pass filter
def low_pass_filter(u_in, tau_C, tau_L, dt):
    u_out = np.zeros_like(u_in)
    for i in range(1, len(u_in)):
        if i == 1:
            u_out[i] = (dt**2/(tau_L*tau_C))*u_in[i] + (2 - (dt/tau_C))*u_out[i - 1]
        else:
            u_out[i] = (dt**2/(tau_L*tau_C))*u_in[i] + (2 - (dt/tau_C))*u_out[i - 1] - (1 - (dt/tau_C) + (dt**2/(tau_L*tau_C)))*u_out[i - 2]
    return u_out

u_out = low_pass_filter(u_in, tau_C, tau_L, dt)

# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input", "Output"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_in[i], u_out[i]])  