from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt("data.csv", delimiter=",", comments="#")



# Scales for graph
f_max = 100
f_min = 0.1
f_step = 0.1  # Frequency step in Hz

# Number of sample points
N = data.shape[0]
# sample spacing
T = data[1, 0] - data[0, 0]

x = data[:, 0]
y_in = data[:, 1]


yf_in = fft(y_in)

# Only keep the positive frequency components for plotting/exporting
xf = fftfreq(N, T)

# Create interpolated frequency array with specified step
xf = np.arange(f_min, f_max + f_step, f_step)



amplitude_scale = 2.0 / N
amp_in = amplitude_scale * np.abs(yf_in[:len(xf)])


# Match the FFT amplitude scale to the peak amplitude observed in the time domain.
max_input_signal = np.max(np.abs(y_in))
max_fft_amplitude = np.max(amp_in) if amp_in.size else 0.0
if max_fft_amplitude > 0.0:
	amplitude_match_scale = max_input_signal / max_fft_amplitude
	amp_in *= amplitude_match_scale

R = 220 # Resistance in ohms
Z_R = R
C = 220e-6 # Capacitance in farads
Z_C = 1/(1j * 2 * np.pi * xf * C)
H = Z_C / (Z_R + Z_C)  # Transfer function
amp_out = amp_in * np.abs(H)

np.savetxt(
	"fft.csv",
	np.column_stack((xf, amp_in, amp_out)),
	delimiter=",",
	header="# frequency(Hz) , input_amplitude(V) , output_amplitude(V)",
	comments="",
)



plt.plot(xf, amp_in, label="Input")
plt.plot(xf, amp_out, label="Output")
plt.xlim(f_min, f_max)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (V)")
plt.grid()
plt.legend()
plt.show()

# plt.plot(xf, phase_in, label="Input")
# plt.plot(xf, phase_out, label="Output")
# plt.xlim(f_min, f_max)
# plt.xlabel("Frequency (kHz)")
# plt.ylabel("Phase (radians)")
# plt.grid()
# plt.legend()
# plt.show()