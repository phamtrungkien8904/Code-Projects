# Inverse FFT to reconstruct time-domain signal from frequency-domain data
import numpy as np
import matplotlib.pyplot as plt
data = np.loadtxt("fft.csv", delimiter=",", comments="#")
frequencies = data[:, 0]
input_amplitudes = data[:, 1]
output_amplitudes = data[:, 2]


# Set the parameters for the filter
dt = 0.00001   # Time step (dt << tau)
t = np.arange(0, 1, dt)  # Time array
u_in = np.zeros_like(t)
u_out = np.zeros_like(t)

for i in range(len(frequencies)):
    f = frequencies[i]
    A_in = input_amplitudes[i]
    A_out = output_amplitudes[i]

    u_in += A_in * np.sin(2 * np.pi * f * t)
    u_out += A_out * np.sin(2 * np.pi * f * t)




# Plot the reconstructed time-domain signal
plt.plot(t, u_in, label="Reconstructed Input Signal")
plt.plot(t, u_out, label="Reconstructed Output Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Inverse FFT Reconstructed Signal")
plt.grid()
plt.legend()
plt.show()
# Save the reconstructed signal to a CSV file
np.savetxt(
    "ifft.csv",
    np.column_stack((t, u_in)),
    delimiter=",",
    header="# Time(s) , Reconstructed_Amplitude",
    comments="",
)

