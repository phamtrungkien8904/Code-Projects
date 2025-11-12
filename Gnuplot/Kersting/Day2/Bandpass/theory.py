import numpy as np

# test.py
# Plot Bode diagram for series R with parallel L||C (R - (L||C))
import matplotlib.pyplot as plt

# Component values
R = 51
dR = 0.01*R
C = 1e-6
dC = 0.2*C
L = 8.7e-6
dL = 0.2*L

# Frequency axis (Hz)
f = np.logspace(2, 6, 100000)   # 1 kHz .. 100 kHz
w = 2 * np.pi * f

# Impedances
R_S = 50.0  # Source resistance (50 ohm)
R_L = 0.2   # Loss in inductor 
Z_L = 1j * w * L 
Z_C = 1 / (1j * w * C)
Z_p = 1 / (1 / Z_L + 1 / Z_C)      # parallel of L and C
Z_p2 = 1 / (1 / (Z_L + R_L) + 1 / Z_C)  # parallel of (L+R_L) and C

# Transfer functions (complex)
H_ideal = Z_p / (R + Z_p)
H_theo = Z_p2 / (R + Z_p2)

# Input/output divider magnitudes with source resistance included
H_in = np.abs((R + Z_p2) / (R_S + R + Z_p2))
H_out = np.abs(Z_p2 / (R_S + R + Z_p2))
# Magnitude and phase
G_ideal = 20 * np.log10(np.abs(H_ideal))
phi_ideal = np.unwrap(np.angle(H_ideal)) * 180 / np.pi
H_theo_mag = np.abs(H_theo)
G_theo = 20 * np.log10(H_theo_mag)
phi_theo = np.unwrap(np.angle(H_theo)) * 180 / np.pi

# Resonance and -3 dB bandwidth (numerical)
peak_idx = np.argmax(H_theo_mag)
f_res = f[peak_idx]
G_res = 20 * np.log10(H_theo_mag[peak_idx])
db3_level = G_res - 3.0

below_mask = G_theo[:peak_idx] <= db3_level
above_mask = G_theo[peak_idx:] <= db3_level

f_lower = np.nan
f_upper = np.nan
# Linear interpolation helper to avoid np.interp ordering assumptions
def lerp_frequency(target_db, g0, g1, f0, f1):
	if g0 == g1:
		return 0.5 * (f0 + f1)
	return f0 + (target_db - g0) * (f1 - f0) / (g1 - g0)
if below_mask.any():
	idx = np.where(below_mask)[0][-1]
	if idx + 1 < len(G_theo):
		f_lower = lerp_frequency(db3_level, G_theo[idx], G_theo[idx + 1], f[idx], f[idx + 1])
if above_mask.any():
	idx = np.where(above_mask)[0][0] + peak_idx
	if idx - 1 >= 0:
		f_upper = lerp_frequency(db3_level, G_theo[idx - 1], G_theo[idx], f[idx - 1], f[idx])

bandwidth = f_upper - f_lower if np.isfinite(f_lower) and np.isfinite(f_upper) else np.nan

print(f"Resonant frequency (Hz): {f_res:.2f}")
print(f"Gain at resonance (dB): {G_res:.2f}")
if np.isfinite(bandwidth):
	print(f"Lower -3 dB frequency (Hz): {f_lower:.2f}")
	print(f"Upper -3 dB frequency (Hz): {f_upper:.2f}")
	print(f"Bandwidth (Hz): {bandwidth:.2f}")
else:
	print("-3 dB bandwidth could not be determined within the sampled range.")

# Export frequency response to CSV for plotting elsewhere
theory_data = np.column_stack(
	(
		f,
		H_in,
		H_out,
		G_ideal,
		G_theo,
		phi_ideal,
		phi_theo,
	)
)

np.savetxt(
	"theory.csv",
	theory_data,
	delimiter=",",
	header="# f,H_in,H_out,G_ideal,G_theo,phi_ideal,phi_theo",
	comments="",
)

bandwidth_data = np.array([[f_res, f_lower, f_upper, bandwidth, G_res]])
np.savetxt(
	"theory_output.csv",
	bandwidth_data,
	delimiter=",",
	header="# f_res,f_lower,f_upper,bandwidth, G_res",
	comments="",
)

# Plot
# plt.plot(f, G_ideal, label="Ideal (no R_L)")
# plt.plot(f, G_theo, label="Including R_L")
# plt.xlim(1e3, 1e5)
# plt.xscale("log")
# plt.ylim(-40, 0)
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("Amplitude (V)")
# plt.grid()
# plt.legend()
# plt.show()


# plt.plot(f, H_in, label="Input")
# plt.plot(f, H_out, label="Output")
# plt.xlim(1e3, 1e5)
# plt.ylim(0, 1)
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("Amplitude (V)")
# plt.grid()
# plt.legend()
# plt.show()