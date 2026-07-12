from cmath import phase

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# Physical parameters
# -------------------------------------------------
wavelength = 633e-9           # Wavelength: 633 nm (red light)
k = 2 * np.pi / wavelength    # Wave number
screen_distance = 1.0         # Distance from slits to screen [m]

# # -------------------------------------------------
# # 51 x 51 source grid
# # -------------------------------------------------
number_source_points = 51
# source_size = 1.0e-3          # Total source-plane width and height [m]

# x_source = np.linspace(
#     -source_size / 2,
#     source_size / 2,
#     number_source_points
# )

# y_source = np.linspace(
#     -source_size / 2,
#     source_size / 2,
#     number_source_points
# )

# Xs, Ys = np.meshgrid(x_source, y_source)

# # -------------------------------------------------
# # Double-slit geometry
# # -------------------------------------------------
# slit_width = 0.08e-3          # Width of each slit [m]
# slit_height = 0.60e-3         # Height of each slit [m]
# slit_separation = 0.30e-3     # Distance between slit centers [m]

# left_slit = (
#     (np.abs(Xs + slit_separation / 2) <= slit_width / 2)
#     & (np.abs(Ys) <= slit_height / 2)
# )

# right_slit = (
#     (np.abs(Xs - slit_separation / 2) <= slit_width / 2)
#     & (np.abs(Ys) <= slit_height / 2)
# )

# # Points that emit light
# source_mask = left_slit | right_slit

# # -------------------------------------------------
# # Diffraction grating parameters
# # -------------------------------------------------
# number_of_slits = 7
# slit_width = 0.08e-3         # Width of each slit [m]
# slit_height = 0.8e-3         # Height of each slit [m]
# grating_period = 0.25e-3     # Distance between slit centers [m]

# source_mask = np.zeros_like(Xs, dtype=bool)

# # Create equally spaced vertical slits
# for n in range(number_of_slits):

#     # Center the complete grating around x = 0
#     x_center = (
#         n - (number_of_slits - 1) / 2
#     ) * grating_period

#     slit = (
#         (np.abs(Xs - x_center) <= slit_width / 2)
#         & (np.abs(Ys) <= slit_height / 2)
#     )

#     source_mask = source_mask | slit

# # -------------------------------------------------
# # Circular source: 51 x 51 grid
# # -------------------------------------------------
# N_source = 101
# source_size = 1.0e-3          # Size of source plane [m]

# x_source = np.linspace(
#     -source_size / 2,
#     source_size / 2,
#     N_source
# )

# y_source = np.linspace(
#     -source_size / 2,
#     source_size / 2,
#     N_source
# )

# Xs, Ys = np.meshgrid(x_source, y_source)

# # Circular aperture
# circle_radius = 0.25e-3       # Radius [m]

# source_mask = Xs**2 + Ys**2 <= circle_radius**2

# # -------------------------------------------------
# # DNA double-helix geometry
# # -------------------------------------------------
# N_source = 51
# source_width = 1.5e-3
# source_height = 3.0e-3

# x_source = np.linspace(
#     -source_width / 2,
#     source_width / 2,
#     N_source
# )

# y_source = np.linspace(
#     -source_height / 2,
#     source_height / 2,
#     N_source
# )

# Xs, Ys = np.meshgrid(x_source, y_source)

# -------------------------------------------------
# 101 x 101 source grid
# -------------------------------------------------
N_source = 201

source_width = 1.5e-3
source_height = 3.0e-3

x_source = np.linspace(
    -source_width / 2,
    source_width / 2,
    N_source
)

y_source = np.linspace(
    -source_height / 2,
    source_height / 2,
    N_source
)

Xs, Ys = np.meshgrid(x_source, y_source)

# -------------------------------------------------
# DNA helix parameters
# -------------------------------------------------
helix_radius = 0.35e-3
helix_pitch = 2.0e-3          # Vertical length of one turn
strand_thickness = 0.06e-3

base_pairs_per_turn = 10
base_pair_spacing = helix_pitch / base_pairs_per_turn
base_pair_thickness = 0.035e-3

# Adjustable relative phase between the two strands
strand_phase_offset = 1.0 * np.pi

# Number of full turns in the source plane
number_of_turns = source_height / helix_pitch

# -------------------------------------------------
# Two strands
# -------------------------------------------------
phase_1 = 2 * np.pi * Ys / helix_pitch
phase_2 = phase_1 + strand_phase_offset

strand_1_x = helix_radius * np.cos(phase_1)
strand_2_x = helix_radius * np.cos(phase_2)

strand_1 = (
    np.abs(Xs - strand_1_x)
    <= strand_thickness / 2
)

strand_2 = (
    np.abs(Xs - strand_2_x)
    <= strand_thickness / 2
)

dna_mask = strand_1 | strand_2

# -------------------------------------------------
# Base pairs: exactly 10 per complete turn
# -------------------------------------------------
first_base_pair_y = -source_height / 2 + base_pair_spacing / 2

base_pair_y_positions = np.arange(
    first_base_pair_y,
    source_height / 2,
    base_pair_spacing
)

for y0 in base_pair_y_positions:

    phase1_y = 2 * np.pi * y0 / helix_pitch
    phase2_y = phase1_y + strand_phase_offset

    x1 = helix_radius * np.cos(phase1_y)
    x2 = helix_radius * np.cos(phase2_y)

    base_pair = (
        (np.abs(Ys - y0) <= base_pair_thickness / 2)
        & (Xs >= min(x1, x2))
        & (Xs <= max(x1, x2))
    )

    dna_mask |= base_pair

# Opaque DNA obstacle: invert the mask to get the transmitting region
source_mask = ~dna_mask
# Coordinates of active source points
active_x = Xs[source_mask]
active_y = Ys[source_mask]

print("Total source grid points:", N_source**2)
print("Transmitting grid points:", len(active_x))

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
plt.figure(figsize=(6, 5))

plt.imshow(
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

plt.xlabel("x [mm]")
plt.ylabel("y [mm]")
plt.title("Source grid")
plt.colorbar(label="Source amplitude")
plt.tight_layout()


plt.figure(figsize=(7, 6))

plt.imshow(
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

plt.xlabel("Screen x [mm]")
plt.ylabel("Screen y [mm]")
plt.title("Screen intensity pattern")
plt.colorbar(label="Normalized intensity")

plt.show()