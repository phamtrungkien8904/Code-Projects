import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import signal

"""
Diode
"""
# Set the parameters for the diode
V_T = 0.05  # Thermal voltage (V)
I_S = 1e-10  # Saturation current (A)
R = 100  # Load resistance (Ohm)

dt = 0.001
t = np.arange(0, 2, dt)
# Input signal (sawtooth wave)
u_in = 2*signal.sawtooth(2 * np.pi * 1 * t)


def diode(u_in):
    """Return load voltage for each input sample using Shockley equation."""
    u_out = np.zeros_like(u_in)
    for idx, v_in in enumerate(u_in):
        v_diode = float(np.clip(v_in, -0.5, 0.9))
        for _ in range(50):
            exp_term = np.exp(v_diode / V_T)
            i_diode = I_S * (exp_term - 1.0)
            residual = v_diode + i_diode * R - v_in
            if abs(residual) < 1e-12:
                break
            derivative = 1.0 + (I_S * exp_term * R / V_T)
            v_diode -= residual / derivative
        i_diode = I_S * (np.exp(v_diode / V_T) - 1.0)
        u_out[idx] = i_diode * R
    return u_out

u_out = diode(u_in)


# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input", "Output"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_in[i], u_out[i]])  


plt.plot(t, u_in, label="Input")
plt.plot(t, u_out, label="Output")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.xlim(0, 2)
plt.ylim(-3, 3)
plt.title("Diode Response")
plt.legend()
plt.grid()
plt.show()

plt.scatter(u_in, u_out)
plt.xlabel("Input Voltage (V)")
plt.ylabel("Output Voltage (V)")
plt.show()