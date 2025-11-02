import numpy as np
import csv

"""
RLC Bandpass Filter (2nd order) Data Generator
"""

# Set the parameters for the filter
R=100
C=100e-9
L=0.03
tau_C = R*C  # Capacitor time constant
tau_L = L/R  # Inductance time constant
tau = np.sqrt(tau_L*tau_C) 
dt = 0.000001   # Time step
t = np.arange(0, 0.05, dt)  # Time array

# Generate the input signal (square wave)
f0 = 1/(2*np.pi*tau)  # Limit frequency
f = f0  # Frequency of the square wave

# Sine wave
# u_in = np.sin(2 * np.pi *f* t)

# Square wave
# u_in = np.sign(np.sin(2 * np.pi *f* t))

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

# AC sweep
f_start = 100
f_end = 10000
df = 100/0.002
u_in = np.sin(2 * np.pi * (f_start + df*t) * t) 

# Apply the band-pass filter
def band_pass_filter(u_in, tau_C, tau_L, dt):
    u_C = np.zeros_like(u_in)
    Du_C = np.zeros_like(u_in)  # First derivative of u_C
    u_R = np.zeros_like(u_in)  # Output across R (low-pass output)
    for i in range(1, len(u_in)):
        Du_C[i] = Du_C[i-1]*(1 - dt/tau_L) + (u_in[i-1] - u_C[i-1])*(dt/(tau_L*tau_C))
        u_C[i] = u_C[i-1] + Du_C[i]*dt
        u_R[i] = Du_C[i]*tau_C
    return u_R

u_out = band_pass_filter(u_in, tau_C, tau_L, dt)

# Transfer function (Amplitude)
# def transfer_function(f, tau_C, tau_L):
#     s = 1j * 2 * np.pi * f
#     H = (s * tau_C)/(1 + s * tau_C + s**2 * tau_L * tau_C)
#     return abs(H)

# H_amp = transfer_function(f, tau_C, tau_L)

# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input", "Output"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_in[i], u_out[i]])  