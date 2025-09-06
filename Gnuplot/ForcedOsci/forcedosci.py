import numpy as np
import csv

"""
Forced Oscillation Data Generator
---------------------------------
Creates a time-series dataset for a damped, driven harmonic oscillator:

	m x'' + b x' + k x = F0 * cos(omega_d * t)

Saved columns in data.csv:
	t,s        time (s)
	x          displacement (arb)
	v          velocity (arb/s)
	a          acceleration (arb/s^2)
	driving    driving force (arb)
	energy     instantaneous mechanical energy (arb)

Adjust parameters below as desired.
"""

# Physical / model parameters (you can tweak these)
m = 1.0          # mass
k = 2.0          # spring constant
b = 0.5          # damping coefficient
F0 = 2.0         # driving force amplitude
omega_d = 1.0    # driving angular frequency

# Simulation parameters
dt = 0.01       # time step (s)
t_max = 100.0     # total simulation time (s)

# Initial conditions
x0 = 4.0         # initial displacement
v0 = 0.0         # initial velocity

# Theoretical Amplitude   
A = F0 / np.sqrt((k - m * omega_d**2)**2 + (b * omega_d)**2)

def step(x, v, t):
	"""Single time step using velocity-Verlet for damped driven system."""
	# Acceleration at current state
	a = (F0 * np.cos(omega_d * t) - b * v - k * x) / m
	# Velocity half step
	v_half = v + 0.5 * a * dt
	# Position full step
	x_new = x + v_half * dt
	# Acceleration at new position (predictor uses same v_half approx)
	a_new = (F0 * np.cos(omega_d * (t + dt)) - b * v_half - k * x_new) / m
	# Complete velocity step
	v_new = v_half + 0.5 * a_new * dt
	return x_new, v_new, a_new


def simulate():
	n_steps = int(t_max / dt) + 1
	t_values = np.linspace(0.0, t_max, n_steps)
	x = x0
	v = v0
	a = (F0 * np.cos(omega_d * 0.0) - b * v - k * x) / m
	v = v + a * dt  #
	x = x + v * dt  #

	rows = []
	for t in t_values:
		rows.append((t, x, v, a))
		# Advance
		x, v, a = step(x, v, t)
	return rows


def write_csv(rows, filename="data.csv"):
	header = ["t", "x", "v", "a", "A_theory"]
	with open(filename, "w", newline="", encoding="utf-8") as f:
		writer = csv.writer(f)
		writer.writerow(header)
		for row in rows:
			writer.writerow(row + (A,))

if __name__ == "__main__":
	data = simulate()
	write_csv(data)
	print(f"Wrote {len(data)} rows to data.csv")

