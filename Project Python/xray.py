import numpy as np
import matplotlib.pyplot as plt

# Energy range (keV)
E = np.linspace(0.1, 20, 1000)

# Bremsstrahlung background (simplified model)
def bremsstrahlung(E, E_max):
    spectrum = np.where(E < E_max, (E_max - E) / E, 0)
    return spectrum

# Parameters
E_max = 20  # Maximum energy of incoming electrons (tube voltage in keV)
brem = bremsstrahlung(E, E_max)

# Add characteristic lines for Cu
k_alpha = 8.04
k_beta = 8.91

# Add sharp peaks
char_lines = (
    50 * np.exp(-((E - k_alpha)**2) / (2 * 0.05**2)) +  # Kα line
    30 * np.exp(-((E - k_beta)**2) / (2 * 0.05**2))     # Kβ line
)

# Total spectrum
spectrum = brem + char_lines

# Plot
plt.figure(figsize=(10, 6))
plt.plot(E, spectrum, label="Cu X-ray Spectrum")
plt.axvline(k_alpha, color='red', linestyle='--', label='Kα (8.04 keV)')
plt.axvline(k_beta, color='green', linestyle='--', label='Kβ (8.91 keV)')
plt.title("X-ray Emission Spectrum of Cu Anode")
plt.xlabel("Photon Energy (keV)")
plt.ylabel("Intensity (a.u.)")
plt.legend()
plt.grid(True)
plt.show()
