import csv
import numpy as np

frequency_hz = 5.0
sample_rate_hz = 1000
duration_s = 1.0

num_samples = int(sample_rate_hz * duration_s)
time_step = 1.0 / sample_rate_hz

with open("signal.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["# sample", "time_s", "value"])
    for n in range(num_samples):
        t = n * time_step
        value = np.sin(2 * np.pi * frequency_hz * t)
        writer.writerow([n, f"{t:.6f}", f"{value:.6f}"])