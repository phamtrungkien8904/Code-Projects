import numpy as np
import csv

""" Frequency Domain Analysis using FFT """
# Set the parameters for the signal
R = 220
C = 2.2e-6
tau = R*C  # Time constant
dt = 0.001*tau   # Time step (dt << tau)
t = np.arange(0, 0.003, dt)  # Time array
f0 = 1/(2*np.pi*tau)  # Limit frequency
# Generate the input signal (AM signal)
f = f0 # Frequency of wave
u_DC = 5
u_sig = 2*np.sin(2 * np.pi * 50*f * t)
u_noise = 1.0*np.sin(2 * np.pi * 500*f * t)
u_ref = 1*np.sin(2 * np.pi * 50 * f * t)  # Reference signal with phase shift
u_in = u_DC + u_sig + u_noise
u_mix = u_in * u_ref
# Apply the low-pass filter


def low_pass_filter(u):
    u_C = np.zeros_like(u)
    for i in range(1, len(u)):
        u_C[i] = (dt/tau)*u[i] + (1 - (dt/tau))*u_C[i - 1]
    return u_C
u_out = low_pass_filter(u_mix)
# Perform FFT
def perform_fft(u):
    N = len(u)
    U_f = np.fft.fft(u)
    freq = np.fft.fftfreq(N, dt)
    return freq, U_f
freq_in, U_in = perform_fft(u_in)
freq_out, U_out = perform_fft(u_out)
# Save FFT results to CSV

with open('fft_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Frequency (Hz)', 'Input Real', 'Input Imag', 'Output Real', 'Output Imag'])
    for f, u_in_val, u_out_val in zip(freq_in, U_in, U_out):
        writer.writerow([f, u_in_val.real, u_in_val.imag, u_out_val.real, u_out_val.imag])