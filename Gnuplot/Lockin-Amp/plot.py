import numpy as np
import csv

"""
RC Low-Pass Filter (1st order) Data Generator
"""

# Set the parameters for the filter
R = 220
C = 2.2e-6
tau = R*C  # Time constant
dt = 0.001*tau   # Time step (dt << tau)
t = np.arange(0, 0.003, dt)  # Time array
f0 = 1/(2*np.pi*tau)  # Limit frequency

# Generate the input signal (square wave)
f = f0 # Frequency of wave  

# Sine wave
# u_in = np.sin(2 * np.pi *f* t)

# # Square wave
# u_in =np.sign(np.sin(2 * np.pi *3.6*f* t))

# Fourier series approximation of square wave
# u_in = np.sum([ (4/(np.pi*(2*n+1))) * np.sin(2 * np.pi * (2*n+1) * f * t) for n in range(3)], axis=0)

# # Sawtooth wave
# u_in = (2*(t*f - np.floor(0.5 + t*f)))

# Sawtooth wave Fourier series
# u_in = 1/3*np.sum([ ((-1)**n)/(n+1) * np.sin(2 * np.pi * (n+1) * f * t) for n in range(20)], axis=0)


# Fourier series (random noising waves)
# u_in = 1*np.sin(2 * np.pi * f * t) + (1/5)*np.sin(2 * np.pi * 10 * f * t) + (1/5)*np.sin(2 * np.pi * 20 * f * t) + (1/5)*np.sin(2 * np.pi * 15 * f * t)

# AM
u_DC = 5
u_sig = 2*np.sin(2 * np.pi * 50*f * t)
u_noise = 0.5*np.sin(2 * np.pi * 100*f * t) + 0.2*np.sin(2 * np.pi * 150*f * t) + 0.1*np.sin(2 * np.pi * 200*f * t)
u_ref = 1*np.sin(2 * np.pi * 50 * f * t)  # Reference signal with phase shift
u_in = u_DC + u_sig + u_noise
u_mix = u_in * u_ref

# # AC sweep
# f_start = 10
# f_end = 1000
# df = (f_end - f_start)/len(t)
# u_in = np.sin(2 * np.pi * (f_start + df*t*100000) * t) 

# Apply the low-pass filter
def low_pass_filter(u):
    u_C = np.zeros_like(u)
    for i in range(1, len(u)):
        u_C[i] = (dt/tau)*u[i] + (1 - (dt/tau))*u_C[i - 1]
    return u_C

u_out = low_pass_filter(u_mix)


# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input", "Reference", "Mix", "Output"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_in[i], u_ref[i], u_mix[i], u_out[i]])  