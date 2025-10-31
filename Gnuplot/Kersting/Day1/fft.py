from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt("day1.csv", delimiter=",", comments="#")


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
xf = fftfreq(N, T)[: N // 2]
amplitude_scale = 2.0 / N
amp_in = amplitude_scale * np.abs(yf_in[: N // 2])
amp_out = amplitude_scale * np.abs(yf_out[: N // 2])
phase_in = np.unwrap(np.angle(yf_in[: N // 2]))
phase_out = np.unwrap(np.angle(yf_out[: N // 2]))

np.savetxt(
	"fft.csv",
	np.column_stack((xf, amp_in, amp_out, phase_in, phase_out)),
	delimiter=",",
	header="frequency,input_amplitude,output_amplitude,input_phase,output_phase",
	comments="",
)

plt.plot(xf, amp_in, label="Input")
plt.plot(xf, amp_out, label="Output")
plt.xlim(0, 2)
plt.xlabel("Frequency (kHz)")
plt.ylabel("Amplitude (V)")
plt.grid()
plt.legend()
plt.show()

# plt.plot(xf, phase_in, label="Input")
# plt.plot(xf, phase_out, label="Output")
# plt.xlim(0, 2)
# plt.xlabel("Frequency (kHz)")
# plt.ylabel("Phase (radians)")
# plt.grid()
# plt.legend()
# plt.show()