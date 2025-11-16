from scipy.fft import fft, fftfreq, ifft
import numpy as np
import csv
import matplotlib.pyplot as plt

"""
RC Low-Pass Filter (1st order) Data Generator
"""

# Set the parameters for the filter
# sample points
N = 100000
dt = 1 / N   # Time step (dt << tau)
t = np.arange(0, 1, dt)  # Time array
f =1

# Generate the input signal (square wave)

# Sine wave
# u_in = np.sin(2 * np.pi *f* t)

# Square wave
u_in = np.sign(np.sin(2 * np.pi *f* t))

# Fourier series approximation of square wave
# u_in = np.sum([ (4/(np.pi*(2*n+1))) * np.sin(2 * np.pi * (2*n+1) * f * t) for n in range(50)], axis=0)

# Sawtooth wave
# u_in = (2*(t*f - np.floor(0.5 + t*f)))

# Sawtooth wave Fourier series
# u_in = 1/3*np.sum([ ((-1)**n)/(n+1) * np.sin(2 * np.pi * (n+1) * f * t) for n in range(50)], axis=0)


# Fourier series (random noising waves)
# u_in = 1*np.sin(2 * np.pi * f * t) + (1/5)*np.sin(2 * np.pi * 10 * f * t) + (1/5)*np.sin(2 * np.pi * 20 * f * t) + (1/5)*np.sin(2 * np.pi * 15 * f * t)

# AC sweep
# f_start = 10
# f_end = 2000
# df = 5
# u_in = np.sin(2 * np.pi * (f_start + df*t*1000 ) * t) 


R = 144
C = 220e-6
L = 10e-1
# Transfer function (complex, not just amplitude)
def transfer_function(f):
    s = 1j * 2 * np.pi * f
    Z_R = R
    Z_C = 1 / (s * C)
    H = Z_C / (Z_R + Z_C)
    return H  # Return complex transfer function, not just magnitude




yf = fft(u_in)
xf = fftfreq(N, dt)



# Apply transfer function, but ignore f = 0.0 (DC component)
mask = xf != 0
H = np.ones_like(xf, dtype=complex)
H[mask] = transfer_function(xf[mask])

yf_out = yf * H


# Save the input and output signals to a CSV file
# with open("data.csv", "w", newline="") as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(["# Time", "Input"])
#     for i in range(len(t)):
#         csvwriter.writerow([t[i], u_in[i]])  
yinv = ifft(yf_out)

    

plt.plot(xf, 2.0/N * np.abs(yf))
plt.plot(xf, 2.0/N * np.abs(yf_out))
plt.xlim(0, 100)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (V)")
plt.title("FFT of Input Signal")
plt.grid()
plt.show()


plt.plot(t, u_in, label="Input Signal")
plt.plot(t, np.abs(yinv), label="Output Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.title("Time-Domain Signal through RC Low-Pass Filter")
plt.grid()
plt.legend()
plt.show()