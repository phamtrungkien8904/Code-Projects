import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# Physical parameters
# -------------------------------------------------
wavelength = 0.154e-9         # X-ray wavelength: 0.154 nm
k = 2 * np.pi / wavelength    # Wave number
screen_distance = 0.25        # Distance from DNA segment to screen [m]

# -------------------------------------------------
# DNA segment geometry
# -------------------------------------------------
number_base_pairs = 20
base_pairs_per_turn = 10
base_pair_rise = 0.34e-9      # Rise between base pairs [m]
helix_radius = 1.0e-9         # Approximate DNA helix radius [m]

base_pair_index = np.arange(number_base_pairs)
z_positions = base_pair_index * base_pair_rise
turn_angle = 2 * np.pi * base_pair_index / base_pairs_per_turn

strand_one_x = helix_radius * np.cos(turn_angle)
strand_one_y = z_positions

strand_two_x = helix_radius * np.cos(turn_angle + np.pi)
strand_two_y = z_positions

# -------------------------------------------------
# DNA source points
# -------------------------------------------------
active_x = np.concatenate([strand_one_x, strand_two_x])
active_y = np.concatenate([strand_one_y, strand_two_y])

source_grid_points = 201
source_x_min = -5.0e-9
source_x_max = 5.0e-9
source_y_min = -1.0e-9
source_y_max = z_positions[-1] + 1.0e-9
strand_width = 0.1e-9        # Visual width of each DNA strand [m]
pair_width = 0.1e-9          # Visual width of each base-pair rung [m]

x_source = np.linspace(source_x_min, source_x_max, source_grid_points)
y_source = np.linspace(source_y_min, source_y_max, source_grid_points)
Xs, Ys = np.meshgrid(x_source, y_source)

def segment_distance(px, py, x1, y1, x2, y2):
    segment_x = x2 - x1
    segment_y = y2 - y1
    segment_length_squared = segment_x**2 + segment_y**2
    if segment_length_squared == 0:
        return np.sqrt((px - x1)**2 + (py - y1)**2)

    projection = ((px - x1) * segment_x + (py - y1) * segment_y) / segment_length_squared
    projection = np.clip(projection, 0.0, 1.0)
    closest_x = x1 + projection * segment_x
    closest_y = y1 + projection * segment_y
    return np.sqrt((px - closest_x)**2 + (py - closest_y)**2)


source_mask = np.zeros_like(Xs, dtype=bool)

for strand_x, strand_y in ((strand_one_x, strand_one_y), (strand_two_x, strand_two_y)):
    for start_index in range(number_base_pairs - 1):
        source_mask |= (
            segment_distance(
                Xs,
                Ys,
                strand_x[start_index],
                strand_y[start_index],
                strand_x[start_index + 1],
                strand_y[start_index + 1],
            ) <= strand_width / 2
        )

for start_index in range(number_base_pairs):
    source_mask |= (
        segment_distance(
            Xs,
            Ys,
            strand_one_x[start_index],
            strand_one_y[start_index],
            strand_two_x[start_index],
            strand_two_y[start_index],
        ) <= pair_width / 2
    )

source_mode = (
    f"DNA double helix: {base_pairs_per_turn} bp/turn, "
    f"{base_pair_rise * 1e9:.2f} nm rise"
)

print("Total base pairs:", number_base_pairs)
print("Total source grid points:", source_grid_points**2)
print("Source mode:", source_mode)
print("Active source points:", len(active_x))

# -------------------------------------------------
# Two-dimensional screen
# -------------------------------------------------
number_screen_points = 401
screen_size = 300e-3          # Screen width and height [m]

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
        x_source[0] * 1e9,
        x_source[-1] * 1e9,
        y_source[0] * 1e9,
        y_source[-1] * 1e9,
    ],
    origin="lower",
    cmap="gray"
)
ax1.set_xlabel("x [nm]")
ax1.set_ylabel("DNA axis [nm]")
ax1.set_title(f"DNA source grid: {source_mode}")
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
ax2.set_title("X-ray field from a DNA segment")
fig.colorbar(im2, ax=ax2, label="Normalized intensity")

plt.tight_layout()

plt.show()