import numpy as np
import csv

# Parameters
T_min = 0
T_max = 5
samples = 10000
dt = (T_max - T_min)/samples   # Time step
t = np.arange(T_min, T_max, dt)  # Time array
fs = 1.0 / dt                   # Sample rate (Hz)


"""
Simple AM receiver simulation:
- Generate message m(t), carrier c(t), and AM RF signal s_in(t) = (1+mu m) * c(t)
- Series RLC band-pass tuned near the carrier
- RF amplifier with adjustable gain and optional clip
- Diode + RC envelope detector (envelope ~ 1 + mu m)
- Recover baseband message by removing DC and normalizing
Outputs a CSV for plotting/inspection.
"""

# Input Signal

# Message signal
f_m = 1
m_true = 1*np.sin(2*np.pi*f_m*t)  # baseband message (true)
# Carrier signal
f_c = 10
c = 1*np.sin(2*np.pi*f_c*t)
# AM signal
mu = 0.8
e = 1 + mu*m_true            # AM envelope factor
s_in = e*c                    # RF signal

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

# RF amplifier (adjustable)
G_RF = 5.0                    # RF gain
VCLIP_RF = None               # set e.g. to 5.0 to enable hard clipping
s_rf = G_RF * s_tuned
if VCLIP_RF is not None:
    s_rf = np.clip(s_rf, -VCLIP_RF, VCLIP_RF)

# Diode detector (half-wave) and RC envelope
Vd = 0.02                # diode drop (V), small for germanium/schottky
tau_env = 0.2            # envelope RC time constant (s), ~ 1/(2π f_m)
alpha = dt / tau_env
# Avoid all-zero output if tuned amplitude < Vd: adapt effective drop to 10% of peak
peak = float(np.max(np.abs(s_tuned)))
Vd_eff = min(Vd, 0.1 * peak)
rect = np.maximum(s_rf - Vd_eff, 0.0)
env = np.zeros_like(rect)
for n in range(1, len(rect)):
    env[n] = env[n-1] + alpha * (rect[n] - env[n-1])

"""Recover baseband message from envelope.
The envelope approximates k*(1 + mu*m). Remove DC and normalize to get m_hat.
If mu is known, one could also estimate scale k and compute (env/k - 1)/mu.
Here we subtract mean and normalize to unit peak for a robust shape recovery.
"""
env_dc = float(np.mean(env))
m_hat = env - env_dc
# Simple output gain for audio stage
G_AF = 1.0
m_hat *= G_AF
# Normalize to [-1,1] for comparison/viewing (avoid divide-by-zero)
peak_m = float(np.max(np.abs(m_hat)))
if peak_m > 0:
    m_hat_norm = m_hat / peak_m
else:
    m_hat_norm = m_hat.copy()

# Save the input and output signals to a CSV file
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['# Time', 'm_true', 'EnvelopeFactor(1+mu*m)', 'Carrier', 'RF_in', 'RLC_out', 'RF_amp', 'Rectified', 'Envelope', 'm_hat', 'm_hat_norm'])
    for i in range(len(t)):
        writer.writerow([t[i], m_true[i], e[i], c[i], s_in[i], s_tuned[i], s_rf[i], rect[i], env[i], m_hat[i], m_hat_norm[i]])

