import numpy as np
import csv

"""
RLC Bandpass Filter (2nd order) Data Generator
"""

# Set the parameters for the filter
# R = 1    # Resistance in ohms
# L = 1.0      # Inductance in henrys
# C = 0.1     # Capacitance in farads
w0 = 5  # Resonant angular frequency
Q = 10    # Quality factor
dt = 0.001   # Time step
t = np.arange(0, 40, dt)  # Time array

# Generate the input signal (square wave)
f0 = w0/(2*np.pi)  # Limit frequency

# Sine wave
u_in = np.sin(2 * np.pi *0.1*f0* t + np.pi/2)

# # Square wave
# u_in = np.sign(np.sin(2 * np.pi *0.1*f0* t))

# Fourier series approximation of square wave
# u_in = np.sum([ (4/(np.pi*(2*n+1))) * np.sin(2 * np.pi * (2*n+1) * f * t) for n in range(3)], axis=0)

# Sawtooth wave
# u_in = (2*(t*f - np.floor(0.5 + t*f)))

# Sawtooth wave Fourier series
# u_in = 1*np.sum([ ((-1)**n)/(n+1) * np.sin(2 * np.pi * (n+1) * f * t) for n in range(20)], axis=0)

# Fourier series (random noising waves)
# amplitudes = [1,0.2,0.2]
# frequencies = [1,10,20]
# u_in = sum(a * np.sin(2 * np.pi * x* f * t) for a, x in zip(amplitudes, frequencies))

# Apply the band-pass filter
def band_pass_filter():
    u_R = np.zeros_like(u_in)
    u_C = np.zeros_like(u_in)
    for i in range(1, len(t)-1):
        u_C[i+1] = 2*u_C[i] - u_C[i-1] + (dt**2)*(w0**2)*(u_in[i] - u_C[i]) - (dt*w0/Q)*(u_C[i] - u_C[i-1])
    for i in range(1, len(t)):
        u_R[i] = 1/(Q*w0)*(u_C[i] - u_C[i-1])/dt
    return u_R*10

u_out = band_pass_filter()


# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input", "Output"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_in[i], u_out[i]])  