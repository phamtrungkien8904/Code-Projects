import csv
from pathlib import Path
import numpy as np

def load_time_series(csv_name="signal.csv"):
    path = Path(__file__).with_name(csv_name)
    times, samples = [], []
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        for row in reader:
            # skip empty rows
            if not row:
                continue
            # find first non-empty token to detect comment/header lines
            first_token = next((t for t in row if t.strip()), None)
            if first_token is None:
                continue
            # skip comment/header lines starting with '#'
            if first_token.lstrip().startswith('#'):
                continue

            # Attempt to parse numeric tokens; skip row if any token is non-numeric
            values = []
            for token in row:
                if not token.strip():
                    continue
                try:
                    values.append(float(token))
                except ValueError:
                    # non-numeric token (e.g. header), skip this row entirely
                    values = []
                    break

            if not values:
                continue

            if len(values) == 1:
                samples.append(values[0])
            else:
                times.append(values[0])
                samples.append(values[1])
    return (np.asarray(times) if times else None,
            np.asarray(samples, dtype=float))

def discrete_fourier_transform(samples):
    samples = np.asarray(samples, dtype=complex)
    n = samples.size
    indices = np.arange(n)
    exponent = -2j * np.pi * indices[:, None] * indices / n
    return np.exp(exponent) @ samples

def main():
    times, samples = load_time_series()
    if samples.size == 0:
        raise ValueError("signal.csv has no samples")
    dt = float(np.mean(np.diff(times))) if times is not None and len(times) > 1 else 1.0
    spectrum = discrete_fourier_transform(samples)
    freqs = np.fft.fftfreq(samples.size, d=dt)
    for freq, value in zip(freqs[: samples.size // 2], spectrum[: samples.size // 2]):
        print(f"{freq:.6f},{np.abs(value):.6f}")

if __name__ == "__main__":
    main()