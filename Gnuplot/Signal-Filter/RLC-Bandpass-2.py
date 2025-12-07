import numpy as np
import csv

"""
RLC Bandpass Filter (2nd order) Data Generator
"""


# Set the parameters for the filter
R = 20
C = 2.2e-6
L = 10e-3
tau_C = R*C  # Capacitor time constant
tau_L = L/R  # Inductance time constant
dt = 0.00001   # Time step (dt << tau)
t = np.arange(0, 0.04, dt)  # Time array
f0 = 1/(2*np.pi*np.sqrt(tau_L*tau_C))  # Limit frequency

# Generate the input signal (square wave)
f = f0 # Frequency of wave  

# Sine wave
# u_in = np.sin(2 * np.pi *f* t)

# Square wave
# u_in = np.sign(np.sin(2 * np.pi *2*f* t))

# Fourier series approximation of square wave
# u_in = np.sum([ (4/(np.pi*(2*n+1))) * np.sin(2 * np.pi * (2*n+1) * f * t) for n in range(3)], axis=0)

# # Sawtooth wave
# u_in = (2*(t*f - np.floor(0.5 + t*f)))

# Sawtooth wave Fourier series
# u_in = 1/3*np.sum([ ((-1)**n)/(n+1) * np.sin(2 * np.pi * (n+1) * f * t) for n in range(20)], axis=0)


# Fourier series (random noising waves)
# u_in = 1*np.sin(2 * np.pi * f * t) + (1/5)*np.sin(2 * np.pi * 10 * f * t) + (1/5)*np.sin(2 * np.pi * 20 * f * t) + (1/5)*np.sin(2 * np.pi * 15 * f * t)

# AC sweep
f_start = 10
f_end = 1000
df = (f_end - f_start)/len(t)
u_in = np.sin(2 * np.pi * (f_start + df*t*100000) * t) 

# Apply the band-pass filter
def band_pass_filter(u_in, tau_C, tau_L, dt):
    u_C = np.zeros_like(u_in)
    Du_C = np.zeros_like(u_in)  # First derivative of u_C
    u_LC = np.zeros_like(u_in)  # Output across LC (bandpass output)
    for i in range(1, len(u_in)):
        Du_C[i] = Du_C[i-1]*(1 - dt/tau_L) + (u_in[i-1] - u_C[i-1])*(dt/(tau_L*tau_C))
        u_C[i] = u_C[i-1] + Du_C[i]*dt
    return Du_C*tau_C

u_out = band_pass_filter(u_in, tau_C, tau_L, dt)

# # Transfer function (Amplitude)
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