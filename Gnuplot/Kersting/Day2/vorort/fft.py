from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt("data.csv", delimiter=",", comments="#")

# Scales for graph
f_max = 100000
f_min = 10000

# Number of sample points
N = data.shape[0]
# sample spacing
T = data[1, 0] - data[0, 0]

x = data[:, 0]
y_in = data[:, 1]
y_out = data[:, 2]


yf_in = fft(y_in)
yf_out = fft(y_out)

# Only keep the positive frequency components for plotting/exporting
half = N // 2
xf = fftfreq(N, T)[:half]
yf_in_half = yf_in[:half]
yf_out_half = yf_out[:half]

# Truncate output to the frequency window of interest
mask = (xf >= f_min) & (xf <= f_max)
xf = xf[mask]
yf_in_half = yf_in_half[mask]
yf_out_half = yf_out_half[mask]

amplitude_scale = 2.0 / N
amp_in = amplitude_scale * np.abs(yf_in_half)
amp_out = amplitude_scale * np.abs(yf_out_half)

# Match the FFT amplitude scale to the peak amplitude observed in the time domain.
max_input_signal = np.max(np.abs(y_in))
max_fft_amplitude = np.max(amp_in) if amp_in.size else 0.0
if max_fft_amplitude > 0.0:
	amplitude_match_scale = max_input_signal / max_fft_amplitude
	amp_in *= amplitude_match_scale
	amp_out *= amplitude_match_scale

eps = np.finfo(float).eps
valid = (amp_in > eps) & (amp_out > eps)

phase_in = np.full_like(xf, np.nan)
phase_out = np.full_like(xf, np.nan)
phase_diff_rad = np.full_like(xf, np.nan)
phase_diff_deg = np.full_like(xf, np.nan)

if np.any(valid):
	ratio = np.empty_like(yf_in_half, dtype=np.complex128)
	ratio[:] = np.nan + 1j * np.nan
	ratio[valid] = yf_out_half[valid] / yf_in_half[valid]

	valid_idx = np.flatnonzero(valid)
	phase_in_vals = np.angle(yf_in_half[valid_idx])
	phase_out_vals = np.angle(yf_out_half[valid_idx])
	phase_ratio_vals = np.angle(ratio[valid_idx])

	phase_in_unwrapped = np.unwrap(phase_in_vals)
	phase_out_unwrapped = np.unwrap(phase_out_vals)
	phase_ratio_unwrapped = np.unwrap(phase_ratio_vals)

	phase_diff_deg_valid = np.degrees(phase_ratio_unwrapped)
	phase_diff_deg_valid = (phase_diff_deg_valid + 180.0) % 360.0 - 180.0
	phase_diff_rad_valid = np.radians(phase_diff_deg_valid)

	phase_in[valid_idx] = phase_in_unwrapped
	phase_out[valid_idx] = phase_out_unwrapped
	phase_diff_deg[valid_idx] = phase_diff_deg_valid
	phase_diff_rad[valid_idx] = phase_diff_rad_valid

np.savetxt(
	"fft.csv",
	np.column_stack((xf, amp_in, amp_out, phase_in, phase_out, phase_diff_rad, phase_diff_deg)),
	delimiter=",",
	header="# frequency,input_amplitude,output_amplitude,input_phase,output_phase,phase_diff_rad,phase_diff_deg",
	comments="",
)

# plt.plot(xf, amp_in, label="Input")
# plt.plot(xf, amp_out, label="Output")
# plt.xlim(f_min, f_max)
# plt.xlabel("Frequency (kHz)")
# plt.ylabel("Amplitude (V)")
# plt.grid()
# plt.legend()
# plt.show()

# plt.plot(xf, phase_in, label="Input")
# plt.plot(xf, phase_out, label="Output")
# plt.xlim(f_min, f_max)
# plt.xlabel("Frequency (kHz)")
# plt.ylabel("Phase (radians)")
# plt.grid()
# plt.legend()
# plt.show()