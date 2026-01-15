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
u_noise = 1.0*np.sin(2 * np.pi * 500*f * t) + 0.5*np.sin(2 * np.pi * 200*f * t)
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


def fft_two_sided_spectrum(u: np.ndarray, sample_time: float):
    """Return two-sided FFT spectrum (includes negative frequencies).

    Frequencies are ordered from negative to positive using `fftshift`.

    Amplitude scaling here is two-sided: for a real sinusoid
    `A*sin(2*pi*f*t)`, peaks appear at ±f with amplitude about A/2 each.
    """
    n = len(u)
    spectrum = np.fft.fft(u)
    freqs_hz = np.fft.fftfreq(n, sample_time)

    spectrum = np.fft.fftshift(spectrum)
    freqs_hz = np.fft.fftshift(freqs_hz)

    amplitude = np.abs(spectrum) / n
    phase_rad = np.angle(spectrum)
    return freqs_hz, spectrum, amplitude, phase_rad


freq_in_full, _, amp_in_full, _ = fft_two_sided_spectrum(u_in, dt)
freq_ref_full, _, amp_ref_full, _ = fft_two_sided_spectrum(u_ref, dt)
freq_mix_full, _, amp_mix_full, _ = fft_two_sided_spectrum(u_mix, dt)
freq_out_full, _, amp_out_full, _ = fft_two_sided_spectrum(u_out, dt)

# Sanity: all FFT frequency grids must match (same n and dt)
if not (
    np.array_equal(freq_in_full, freq_ref_full)
    and np.array_equal(freq_in_full, freq_mix_full)
    and np.array_equal(freq_in_full, freq_out_full)
):
    raise ValueError('FFT frequency grids do not match; ensure same length and sample time.')


# Save FFT results to CSV (two-sided: includes negative frequencies)
with open('fft_data_full.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        'Frequency (Hz)',
        'Input Amplitude (two-sided)',
        'Reference Amplitude (two-sided)',
        'Mix Amplitude (two-sided)',
        'Output Amplitude (two-sided)',
    ])
    for f_hz, a_in, a_ref, a_mix, a_out in zip(
        freq_in_full,
        amp_in_full,
        amp_ref_full,
        amp_mix_full,
        amp_out_full,
    ):
        writer.writerow([f_hz, a_in, a_ref, a_mix, a_out])