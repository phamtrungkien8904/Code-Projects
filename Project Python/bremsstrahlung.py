import numpy as np
import matplotlib.pyplot as plt

# Define parameters
sampling_rate = 1000  # Samples per second
duration = 2  # Seconds
time = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Define three frequencies for the harmonic function
freq1 = 5  # Hz
freq2 = 50  # Hz
freq3 = 100  # Hz

# Define the harmonic function
signal = (np.sin(2 * np.pi * freq1 * time) +
          np.sin(2 * np.pi * freq2 * time) +
          np.sin(2 * np.pi * freq3 * time))

# Perform Fourier Transform
frequencies = np.fft.rfftfreq(len(time), 1 / sampling_rate)
fft_values = np.fft.rfft(signal)

# Plot the original signal
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(time, signal)
plt.title("Original Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()

# Plot the Fourier Transform (magnitude spectrum)
plt.subplot(2, 1, 2)
plt.plot(frequencies, np.abs(fft_values))
plt.title("Fourier Transform (Magnitude Spectrum)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()

plt.tight_layout()
plt.show()