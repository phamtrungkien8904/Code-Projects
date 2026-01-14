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
u_sig = 2.0*np.sin(2 * np.pi * 50*f * t)
u_noise = 1.0*np.sin(2 * np.pi * 500*f * t)
u_ref = 1.0*np.sin(2 * np.pi * 50 * f * t)  # Reference signal with phase shift
u_in = u_DC + u_sig + u_noise
u_mix = u_in * u_ref
# Apply the low-pass filter


def low_pass_filter(u):
    u_C = np.zeros_like(u)
    for i in range(1, len(u)):
        u_C[i] = (dt/tau)*u[i] + (1 - (dt/tau))*u_C[i - 1]
    return u_C
u_out = low_pass_filter(u_mix)


def fft_single_sided_spectrum(u: np.ndarray, sample_time: float):
    """Return single-sided FFT spectrum with amplitude scaled to peak units.

    With this scaling, a sinusoid `A*sin(2*pi*f*t)` appears with amplitude ~A
    at frequency f (assuming coherent sampling / minimal leakage).
    """
    n = len(u)
    spectrum = np.fft.rfft(u)
    freqs_hz = np.fft.rfftfreq(n, sample_time)

    amplitude = (2.0 / n) * np.abs(spectrum)
    # Don't double-count DC (and Nyquist when n is even)
    amplitude[0] = np.abs(spectrum[0]) / n
    if n % 2 == 0:
        amplitude[-1] = np.abs(spectrum[-1]) / n

    phase_rad = np.angle(spectrum)
    return freqs_hz, spectrum, amplitude, phase_rad


freq_in, U_in, amp_in, phase_in = fft_single_sided_spectrum(u_in, dt)
freq_out, U_out, amp_out, phase_out = fft_single_sided_spectrum(u_out, dt)

# Save FFT results to CSV (column 2 is amplitude for your gnuplot script)
with open('fft_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        'Frequency (Hz)',
        'Input Amplitude (V_peak)',
        'Output Amplitude (V_peak)',
        'Input Phase (rad)',
        'Output Phase (rad)',
        'Input Real',
        'Input Imag',
        'Output Real',
        'Output Imag',
    ])
    for f_hz, a_in, a_out, p_in, p_out, u_in_val, u_out_val in zip(
        freq_in, amp_in, amp_out, phase_in, phase_out, U_in, U_out
    ):
        writer.writerow([
            f_hz,
            a_in,
            a_out,
            p_in,
            p_out,
            u_in_val.real,
            u_in_val.imag,
            u_out_val.real,
            u_out_val.imag,
        ])