import numpy as np
import csv

"""
RC Low-Pass Filter (1st order) Data Generator
"""

# Set the parameters for the filter
dt = 0.00001   # Time step (dt << tau)
t = np.arange(0, 1, dt)  # Time array
f = 1

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
# u_in = 1/3*np.sum([ ((-1)**n)/(n+1) * np.sin(2 * np.pi * (n+1) * f * t) for n in range(20)], axis=0)


# Fourier series (random noising waves)
# u_in = 1*np.sin(2 * np.pi * f * t) + (1/5)*np.sin(2 * np.pi * 10 * f * t) + (1/5)*np.sin(2 * np.pi * 20 * f * t) + (1/5)*np.sin(2 * np.pi * 15 * f * t)

# AC sweep
# f_start = 10
# f_end = 2000
# df = 5
# u_in = np.sin(2 * np.pi * (f_start + df*t*1000 ) * t) 




# # Transfer function (Amplitude)
# def transfer_function(f, tau):
#     s = 1j * 2 * np.pi * f
#     H = 1 / (1 + s * tau)
#     return abs(H) 

# H_amp = transfer_function(f, tau)

# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_in[i]])  
