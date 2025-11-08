import numpy as np

# test.py
# Plot Bode diagram for series R with parallel L||C (R - (L||C))
import matplotlib.pyplot as plt

# Component values
R = 51.0               # ohm
L = 10e-6              # henry (10 uH)
C = 1e-6               # farad (1 uF)

# Frequency axis (Hz)
f = np.logspace(3, 5, 2000)   # 1 kHz .. 100 kHz
w = 2 * np.pi * f

# Impedances
R_S = 50.0  # Source resistance (50 ohm)
R_L = 0.23   # Loss in inductor (0.1 ohm at 1 MHz)
Z_L = 1j * w * L 
Z_C = 1 / (1j * w * C)
Z_p = 1 / (1 / Z_L + 1 / Z_C)      # parallel of L and C
Z_p2 = 1 / (1 / (Z_L + R_L) + 1 / Z_C)  # parallel of (L+R_L) and C

# Transfer function: voltage across parallel branch (voltage divider)
H_theo = Z_p / (R + Z_p)

H_error = Z_p2 / (R + Z_p2)

H1 = (R + Z_p2)/(R_S + R + Z_p2)
H2 = Z_p2/(R_S + R + Z_p2)
# Magnitude and phase
mag_db_theo = 20 * np.log10(np.abs(H_theo))
phase_deg_theo = np.unwrap(np.angle(H_theo)) * 180 / np.pi

mag_db_error = 20 * np.log10(np.abs(H_error))
phase_deg_error = np.unwrap(np.angle(H_error)) * 180 / np.pi

# Function



# Resonant frequency (parallel resonance)
f0 = 1 / (2 * np.pi * np.sqrt(L * C))

# Plot
plt.plot(f, mag_db_theo, label="Theoretical")
plt.plot(f, mag_db_error, label="Including R_L")
plt.plot(f, H1, label="Including R_S")
plt.xlim(1e3, 1e5)
plt.xscale("log")
plt.ylim(-40, 0)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (V)")
plt.grid()
plt.legend()
plt.show()


# plt.plot(f, H1, label="Including R_S")
# plt.plot(f, H2, label="Including R_S")
# plt.xlim(1e3, 1e5)
# plt.ylim(0, 1)
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("Amplitude (V)")
# plt.grid()
# plt.legend()
# plt.show()