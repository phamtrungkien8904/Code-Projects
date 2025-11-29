import numpy as np
import csv

"""
RLC Bandpass Filter (2nd order) Data Generator
"""

# Set the parameters for the filter
R = 1    # Resistance in ohms
L = 1.0      # Inductance in henrys
C = 0.1     # Capacitance in farads
w0 = 1/np.sqrt(L*C)  # Resonant angular frequency
Q = w0*L/R        # Quality factor
dt = 0.05   # Time step
t = np.arange(0, 10, dt)  # Time array

# Generate the input signal (square wave)
f0 = w0/(2*np.pi)  # Limit frequency
f = f0  # Frequency of the square wave

# Sine wave
u_in = np.sin(2 * np.pi *0.5*f* t)

# Square wave
# u_in = np.sign(np.sin(2 * np.pi *f* t))

# Fourier series approximation of square wave
# u_in = np.sum([ (4/(np.pi*(2*n+1))) * np.sin(2 * np.pi * (2*n+1) * f * t) for n in range(3)], axis=0)

# Sawtooth wave
# u_in = (2*(t*f - np.floor(0.5 + t*f)))

# Sawtooth wave Fourier series
# u_in = 1*np.sum([ ((-1)**n)/(n+1) * np.sin(2 * np.pi * (n+1) * f * t) for n in range(20)], axis=0)

# Fourier series (random noising waves)
# amplitudes = [1,0.2,0.2]
# frequencies = [1,10,20]
# u_in = sum(a * np.sin(2 * np.pi * x* f * t) for a, x in zip(amplitudes, frequencies))

# Apply the band-pass filter
def band_pass_filter():
    D2q_dt2 = np.zeros_like(u_in)
    Dq_dt = np.zeros_like(u_in)
    q = np.zeros_like(u_in)
    u_out = np.zeros_like(u_in)
    for i in range(2, len(t)):
        D2q_dt2[i] = (u_in[i] - R * Dq_dt[i-1] - q[i-1]/C - L * D2q_dt2[i-1]) / L
        Dq_dt[i] = Dq_dt[i-1] + D2q_dt2[i] * dt
        q[i] = q[i-1] + Dq_dt[i] * dt
        u_out[i] = R* Dq_dt[i] 
    return u_out

u_out = band_pass_filter()


# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input", "Output"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_in[i], u_out[i]])  