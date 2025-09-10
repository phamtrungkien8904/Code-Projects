import numpy as np
import csv

# Parameters
T_min = 0
T_max = 5
samples = 10000
dt = (T_max - T_min)/samples   # Time step
t = np.arange(T_min, T_max, dt)  # Time array


# Input Signal

# Message signal
f_m = 1
m = 1*np.sin(2*np.pi*f_m*t) # + 0.3*np.sin(2*np.pi*2*f_m*t) + 0.2*np.sin(2*np.pi*5*f_m*t)
# Carrier signal
f_c = 10
c = 1*np.sin(2*np.pi*f_c*t)
c2 = 1*np.sin(2*np.pi*2*f_c*t)
# AM signal
mu = 0.8
e = 1 + mu*m
s_in = e*c

# Tuned Circuit
f_t = 1*f_c
tau_L = 1/(2*np.pi*f_t)  # Inductance time constant
tau_C = tau_L/10  # Capacitor time constant

def Tuned(s_in, dt):
    u_C = np.zeros_like(s_in)
    Du_C = np.zeros_like(s_in)  # First derivative of u_C
    u_R = np.zeros_like(s_in)  # Output across LC (bandpass output)
    for i in range(1, len(s_in)):
        Du_C[i] = Du_C[i-1]*(1 - dt/tau_L) + (s_in[i-1] - u_C[i-1])*(dt/(tau_L*tau_C))
        u_C[i] = u_C[i-1] + Du_C[i]*dt
        u_R[i] = Du_C[i]*tau_C
        # Crossing detector (diode)
        if u_R[i] < 0:
            u_R[i] = 0
    return u_R

s_tuned = Tuned(s_in, dt)


# Save the input and output signals to a CSV file
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['# Time', 'Message Signal', 'Carrier Signal', 'AM Signal', 'Tuned Signal'])
    for i in range(len(t)):
        writer.writerow([t[i], e[i], c[i], s_in[i], s_tuned[i]])

