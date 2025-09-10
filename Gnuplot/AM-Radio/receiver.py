import numpy as np
import csv

# Parameters
T_min = 0
T_max = 5
samples = 10000
dt = (T_max - T_min)/samples   # Time step
t = np.arange(T_min, T_max, dt)  # Time array
fs = 1.0 / dt                   # Sample rate (Hz)


# Input Signal

# Message signal
f_m = 1
m = 1*np.sin(2*np.pi*f_m*t) # + 0.3*np.sin(2*np.pi*2*f_m*t) + 0.2*np.sin(2*np.pi*5*f_m*t)
# Carrier signal
f_c = 10
c = 1*np.sin(2*np.pi*f_c*t)
# AM signal
mu = 0.8
e = 1 + mu*m
s_in = e*c

# Tuned circuit: simple analog series RLC and diode envelope detector
# Choose LC from target f_t; choose Q to set R
f_t = 1.2 * f_c           # tuning frequency (Hz)
Q   = 20.0                # quality factor for series RLC
C   = 1e-6                # Farads (choose convenient value)
omega0 = 2.0 * np.pi * f_t
L   = 1.0 / (omega0**2 * C)
# Series RLC: Q = (omega0 * L) / R  =>  R = (omega0 * L) / Q
R   = (omega0 * L) / Q

def series_rlc_bandpass(v_in: np.ndarray, R: float, L: float, C: float, dt: float) -> np.ndarray:
    """Simulate a series RLC excited by Vin. Output is voltage across R (band-pass).
    State: current i, capacitor voltage vC. KVL: L di/dt + R i + vC = Vin; dvC/dt = i/C
    Integrate via semi-implicit Euler.
    """
    y = np.zeros_like(v_in)
    i = 0.0
    vC = 0.0
    for n in range(len(v_in)):
        Vin = v_in[n]
        # Update current using previous vC
        di_dt = (Vin - R * i - vC) / L
        i    = i + di_dt * dt
        # Update capacitor voltage from new current
        vC   = vC + (i / C) * dt
        # Output across R is band-pass component
        y[n] = R * i
    return y

s_tuned = series_rlc_bandpass(s_in, R, L, C, dt)

# Diode detector (half-wave) and RC envelope
Vd = 0.02                # diode drop (V), small for germanium/schottky
tau_env = 0.2            # envelope RC time constant (s), ~ 1/(2π f_m)
alpha = dt / tau_env
# Avoid all-zero output if tuned amplitude < Vd: adapt effective drop to 10% of peak
peak = float(np.max(np.abs(s_tuned)))
Vd_eff = min(Vd, 0.1 * peak)
rect = np.maximum(s_tuned - Vd_eff, 0.0)
env = np.zeros_like(rect)
for n in range(1, len(rect)):
    env[n] = env[n-1] + alpha * (rect[n] - env[n-1])


# Save the input and output signals to a CSV file
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['# Time', 'Message Signal', 'Carrier Signal', 'AM Signal', 'Tuned Signal', 'Rectified', 'Envelope'])
    for i in range(len(t)):
        writer.writerow([t[i], e[i], c[i], s_in[i], s_tuned[i], rect[i], env[i]])

