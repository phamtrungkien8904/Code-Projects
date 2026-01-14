import numpy as np
import csv
import argparse

"""
RC Low-Pass Filter (1st order) Data Generator
"""


def add_measurement_error(
    rng: np.random.Generator,
    x: np.ndarray,
    t: np.ndarray,
    *,
    noise_abs: float,
    noise_rel: float,
    offset: float,
    drift_per_s: float,
    outlier_prob: float,
    outlier_sigma_mult: float,
    quant_step: float,
    clip_abs: float | None,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (x_meas, sigma) where sigma is the assumed 1-sigma per-sample error."""
    sigma = noise_abs + noise_rel * np.abs(x)
    sigma = np.maximum(sigma, 0.0)

    x_meas = x + offset + drift_per_s * (t - t[0])
    if np.any(sigma > 0):
        x_meas = x_meas + rng.normal(0.0, sigma, size=x.shape)

    if outlier_prob > 0:
        mask = rng.random(size=x.shape) < outlier_prob
        if np.any(mask):
            outlier_sigma = outlier_sigma_mult * (sigma[mask] if sigma.ndim else sigma)
            x_meas[mask] = x_meas[mask] + rng.normal(0.0, outlier_sigma)

    if quant_step and quant_step > 0:
        x_meas = np.round(x_meas / quant_step) * quant_step

    if clip_abs is not None:
        x_meas = np.clip(x_meas, -abs(clip_abs), abs(clip_abs))

    return x_meas, sigma

# Set the parameters for the filter
R = 270
C = 2.2e-6
tau = R*C  # Time constant
dt = 0.000001   # Time step (dt << tau)
t = np.arange(0, 0.01, dt)  # Time array
f0 = 1/(2*np.pi*tau)  # Limit frequency

# Fake measurement error parameters (edit here or use CLI args)
DEFAULT_SEED = 1

INPUT_NOISE_ABS = 0.005     # Volts (absolute)
INPUT_NOISE_REL = 0.005      # relative to |signal|
INPUT_OFFSET = 0.00         # Volts
INPUT_DRIFT_PER_S = 0.00    # Volts/second

OUTPUT_NOISE_ABS = 0.005     # Volts
OUTPUT_NOISE_REL = 0.005
OUTPUT_OFFSET = 0.00
OUTPUT_DRIFT_PER_S = 0.00

OUTLIER_PROB = 0.001        # probability per sample
OUTLIER_SIGMA_MULT = 1.0    # outliers are N(0, mult*sigma)

QUANT_STEP = 0.00           # Volts; set >0 to quantize (e.g., ADC step)
CLIP_ABS = None             # Volts; set e.g. 1.2 to clip


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate RC low-pass data (with optional fake measurement errors).")
    p.add_argument("--seed", type=int, default=DEFAULT_SEED)
    p.add_argument("--no-noise", action="store_true", help="Disable measurement error columns (writes meas=true).")

    p.add_argument("--in-noise-abs", type=float, default=INPUT_NOISE_ABS)
    p.add_argument("--in-noise-rel", type=float, default=INPUT_NOISE_REL)
    p.add_argument("--in-offset", type=float, default=INPUT_OFFSET)
    p.add_argument("--in-drift", type=float, default=INPUT_DRIFT_PER_S)

    p.add_argument("--out-noise-abs", type=float, default=OUTPUT_NOISE_ABS)
    p.add_argument("--out-noise-rel", type=float, default=OUTPUT_NOISE_REL)
    p.add_argument("--out-offset", type=float, default=OUTPUT_OFFSET)
    p.add_argument("--out-drift", type=float, default=OUTPUT_DRIFT_PER_S)

    p.add_argument("--outlier-prob", type=float, default=OUTLIER_PROB)
    p.add_argument("--outlier-mult", type=float, default=OUTLIER_SIGMA_MULT)
    p.add_argument("--quant-step", type=float, default=QUANT_STEP)
    p.add_argument("--clip-abs", type=float, default=CLIP_ABS)
    return p.parse_args()

# Generate the input signal (square wave)
f = f0 # Frequency of wave  

# Sine wave
# u_in = np.sin(2 * np.pi *f* t)

# Square wave
u_in =np.sign(np.sin(2 * np.pi *3.6*f* t))

# Fourier series approximation of square wave
# u_in = np.sum([ (4/(np.pi*(2*n+1))) * np.sin(2 * np.pi * (2*n+1) * f * t) for n in range(3)], axis=0)

# # Sawtooth wave
# u_in = (2*(t*f - np.floor(0.5 + t*f)))

# Sawtooth wave Fourier series
# u_in = 1/3*np.sum([ ((-1)**n)/(n+1) * np.sin(2 * np.pi * (n+1) * f * t) for n in range(20)], axis=0)


# Fourier series (random noising waves)
# u_in = 1*np.sin(2 * np.pi * f * t) + (1/5)*np.sin(2 * np.pi * 10 * f * t) + (1/5)*np.sin(2 * np.pi * 20 * f * t) + (1/5)*np.sin(2 * np.pi * 15 * f * t)

# # AC sweep
# f_start = 10
# f_end = 1000
# df = (f_end - f_start)/len(t)
# u_in = np.sin(2 * np.pi * (f_start + df*t*100000) * t) 

# Apply the low-pass filter
def low_pass_filter(u_in, tau, dt):
    u_C = np.zeros_like(u_in)
    for i in range(1, len(u_in)):
        u_C[i] = (dt/tau)*u_in[i] + (1 - (dt/tau))*u_C[i - 1]
    return u_C

u_out = low_pass_filter(u_in, tau, dt)
args = parse_args()
rng = np.random.default_rng(args.seed)

if args.no_noise:
    u_in_meas = u_in.copy()
    u_out_meas = u_out.copy()
    u_in_sigma = np.zeros_like(u_in)
    u_out_sigma = np.zeros_like(u_out)
else:
    u_in_meas, u_in_sigma = add_measurement_error(
        rng,
        u_in,
        t,
        noise_abs=args.in_noise_abs,
        noise_rel=args.in_noise_rel,
        offset=args.in_offset,
        drift_per_s=args.in_drift,
        outlier_prob=args.outlier_prob,
        outlier_sigma_mult=args.outlier_mult,
        quant_step=args.quant_step,
        clip_abs=args.clip_abs,
    )
    u_out_meas, u_out_sigma = add_measurement_error(
        rng,
        u_out,
        t,
        noise_abs=args.out_noise_abs,
        noise_rel=args.out_noise_rel,
        offset=args.out_offset,
        drift_per_s=args.out_drift,
        outlier_prob=args.outlier_prob,
        outlier_sigma_mult=args.outlier_mult,
        quant_step=args.quant_step,
        clip_abs=args.clip_abs,
    )

print(f"f0 = {f0:.3f} Hz")

# # Transfer function (Amplitude)
# def transfer_function(f, tau):
#     s = 1j * 2 * np.pi * f
#     H = 1 / (1 + s * tau)
#     return abs(H) 

# H_amp = transfer_function(f, tau)

# Save the input and output signals to a CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    # Keep original 3 columns (Time/Input/Output) as the *true* signals for compatibility.
    # Additional columns contain fake measurement data + 1-sigma uncertainties.
    csvwriter.writerow(
        [
            "# Time",
            "Input_meas",
            "Output_meas",
            "Input_sigma",
            "Output_sigma",
        ]
    )
    for i in range(len(t)):
        csvwriter.writerow(
            [
                t[i],
                u_in_meas[i],
                u_out_meas[i],
                u_in_sigma[i],
                u_out_sigma[i],
            ]
        )