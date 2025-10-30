import csv
import numpy as np

frequency_hz = 50.0
sample_rate_hz = 10000
duration_s = 1.0

num_samples = int(sample_rate_hz * duration_s)
time_step = 1.0 / sample_rate_hz


with open("signal.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["#time_s", "value"])
    for n in range(num_samples):
        t = n * time_step
        value = 0.5 * np.sin(2.0 * np.pi * frequency_hz * t) + 1.0 * np.sin(2.0 * np.pi * 2.0 * frequency_hz * t)
        writer.writerow([f"{t:.6f}", f"{value:.6f}"])