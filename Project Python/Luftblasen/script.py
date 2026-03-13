import numpy as np
import csv

##### Air bubble in water #####
# Parameters
N = 1000  # Number of samples
dt = 0.01  # Time step
t = np.zeros()

# Apply the low-pass filter
def script():
    u_C = np.zeros_like(u_in)
    for i in range(1, len(u_in)):
        u_C[i] = (dt/tau)*u_in[i] + (1 - (dt/tau))*u_C[i - 1]
    return u_C

u_out = script()


# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["# Time", "Input", "Output"])
    for i in range(len(t)):
        csvwriter.writerow([t[i], u_in[i], u_out[i]])  