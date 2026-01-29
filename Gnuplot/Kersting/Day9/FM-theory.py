import numpy as np
import csv

"""
RC Low-Pass Filter (1st order) Data Generator
"""

# Set the parameters for the filter
R = 3000
C = 10e-9
tau = R*C  # Time constant
dt = 0.001*tau   # Time step (dt << tau)
t = np.arange(0, 0.01, dt)  # Time array

fe = 1000
u_e =0.8 + 0.3*np.sin(2 * np.pi *fe* t)
U0 = 4.5 # Saturation Voltage
u_f = np.zeros_like(t)


def simulate_rc_schmitt(u_e, tau, dt, U0, rel_threshold=0.1):
    """Simulate RC + inverting Schmitt trigger with hysteresis.

    Thresholds are symmetric around 0: ±rel_threshold * U0.
    Output levels are ±U0 and *inverted* w.r.t. the internal state.
    """

    u_s = np.zeros_like(u_e)
    u_rc = np.zeros_like(u_e)
    u_f = np.zeros_like(u_e)

    u_high = rel_threshold * U0
    u_low = -rel_threshold * U0

    # state: 0 -> output +U0, 1 -> output -U0 (inverting characteristic)
    state = 0
    u_f[0] = U0

    for i in range(1, len(u_e)):
        u_s[i] = u_e[i] * np.sign(u_f[i - 1])
        u_rc[i] = (dt / tau) * u_s[i] + (1 - (dt / tau)) * u_rc[i - 1]

        if state == 0 and u_rc[i] > u_high:
            state = 1
        elif state == 1 and u_rc[i] < u_low:
            state = 0

        u_f[i] = -U0 if state == 1 else U0

    return u_s, u_rc, u_f


u_s, u_s_prime, u_f = simulate_rc_schmitt(u_e, tau, dt, U0, rel_threshold=0.1)


# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input", "Output", "Intermodulated", "Capacitor"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_e[i], u_f[i], u_s[i], u_s_prime[i]])  