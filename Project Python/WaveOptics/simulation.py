import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# Physical parameters
# -------------------------------------------------
wavelength = 633e-9           # Wavelength: 633 nm (red light)
k = 2 * np.pi / wavelength    # Wave number
screen_distance = 1.0         # Distance from slits to screen [m]

# -------------------------------------------------
# 101 x 101 source grid
# -------------------------------------------------
number_source_points = 101
source_size = 1.0e-3          # Total source-plane width and height [m]

x_source = np.linspace(
    -source_size / 2,
    source_size / 2,
    number_source_points
)

y_source = np.linspace(
    -source_size / 2,
    source_size / 2,
    number_source_points
)

Xs, Ys = np.meshgrid(x_source, y_source)

# -------------------------------------------------
# Double-slit geometry
# -------------------------------------------------
double_slit_dark = True        # False: slits are dark, everything else is bright
slit_width = 0.1e-3          # Width of each slit [m]
slit_height = 0.2e-3         # Height of each slit [m]
slit_separation = 0.2e-3     # Distance between slit centers [m]

left_slit = (
    (np.abs(Xs + slit_separation / 2) <= slit_width / 2)
    & (np.abs(Ys) <= slit_height / 2)
)

right_slit = (
    (np.abs(Xs - slit_separation / 2) <= slit_width / 2)
    & (np.abs(Ys) <= slit_height / 2)
)

# Points that emit light
source_mask = ~(left_slit | right_slit) if not double_slit_dark else (left_slit | right_slit)

active_x = Xs[source_mask]
active_y = Ys[source_mask]

source_mode = "slits dark, outside bright" if not double_slit_dark else "double slit bright"

print("Total source grid points:", number_source_points**2)
print("Source mode:", source_mode)
print("Active source points:", len(active_x))

# -------------------------------------------------
# Two-dimensional screen
# -------------------------------------------------
number_screen_points = 251
screen_size = 20e-3           # Screen width and height [m]

x_screen = np.linspace(
    -screen_size / 2,
    screen_size / 2,
    number_screen_points
)

y_screen = np.linspace(
    -screen_size / 2,
    screen_size / 2,
    number_screen_points
)

X, Y = np.meshgrid(x_screen, y_screen)

# Complex electric field on the screen
electric_field = np.zeros(X.shape, dtype=complex)

# -------------------------------------------------
# Add the wave from every active source point
# -------------------------------------------------
for x0, y0 in zip(active_x, active_y):

    # Distance from source point (x0, y0, 0)
    # to every screen point (X, Y, screen_distance)
    distance = np.sqrt(
        (X - x0)**2
        + (Y - y0)**2
        + screen_distance**2
    )

    # Spherical wave
    electric_field += np.exp(1j * k * distance) / distance

# Intensity is proportional to |E|²
intensity = np.abs(electric_field)**2

# Normalize intensity between 0 and 1
intensity = intensity / np.max(intensity)

# -------------------------------------------------
# Plot source and interference pattern
# -------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

im1 = ax1.imshow(
    source_mask,
    extent=[
        x_source[0] * 1e3,
        x_source[-1] * 1e3,
        y_source[0] * 1e3,
        y_source[-1] * 1e3
    ],
    origin="lower",
    cmap="gray"
)
ax1.set_xlabel("x [mm]")
ax1.set_ylabel("y [mm]")
ax1.set_title(f"51 × 51 source grid: {source_mode}")
fig.colorbar(im1, ax=ax1, label="Source amplitude")

im2 = ax2.imshow(
    intensity,
    extent=[
        x_screen[0] * 1e3,
        x_screen[-1] * 1e3,
        y_screen[0] * 1e3,
        y_screen[-1] * 1e3
    ],
    origin="lower",
    cmap="hot",
    aspect="equal",
    interpolation="bicubic"
)
ax2.set_xlabel("Screen x [mm]")
ax2.set_ylabel("Screen y [mm]")
ax2.set_title("Two-dimensional double-slit interference")
fig.colorbar(im2, ax=ax2, label="Normalized intensity")

plt.tight_layout()

plt.show()