import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from astroquery.jplhorizons import Horizons
from astropy.time import Time

START = "1979-01-01"
STOP = "1980-01-01"
AU_KM = 149_597_870.7

# Horizons ID and plot color
objects = {
    "Voyager 2": ("-32", "orangered"),
    "Earth":    ("399", "blue"),
    "Mars":     ("499", "red"),
    "Jupiter":   ("599", "lime"),
    "Saturn":    ("699", "cyan"),
    "Uranus":    ("799", "gold"),
    "Neptune":   ("899", "magenta"),
}


def get_vectors(object_id):
    v = Horizons(
        id=object_id,
        location="@10",  # Sun
        epochs={"start": START, "stop": STOP, "step": "10h"}
    ).vectors(refplane="ecliptic")

    return {
        key: np.asarray(v[key], dtype=float)
        for key in ["x", "y", "z", "vx", "vy", "vz", "datetime_jd"]
    }


print("Downloading data from JPL Horizons...")
data = {name: get_vectors(obj_id) for name, (obj_id, _) in objects.items()}

# Use the shortest returned dataset
frames = min(len(d["x"]) for d in data.values())

dates = Time(
    data["Voyager 2"]["datetime_jd"][:frames],
    format="jd",
    scale="tdb"
).to_datetime()

# Precompute Voyager 2 speeds (km/s) for plotting
voy = data["Voyager 2"]
speeds = np.sqrt(voy["vx"][:frames] ** 2 + voy["vy"][:frames] ** 2 + voy["vz"][:frames] ** 2) * AU_KM / 86400

# ------------------------------------------------------------
# Figure
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 8), facecolor="black")
ax.set_facecolor("black")
ax.set_aspect("equal")
ax.axis("off")

# Automatically choose plot limits
limit = max(
    np.max(np.abs(d[coordinate][:frames]))
    for d in data.values()
    for coordinate in ["x", "y"]
) * 1.1

# ax.set_xlim(-limit, limit)
# ax.set_ylim(-limit, limit)

ax.set_xlim(-4.5, -3.5)
ax.set_ylim(3, 4)

# Sun
ax.scatter(0, 0, s=20, color="yellow", zorder=5)

dots = {}

# Full trajectories and moving objects
for name, (_, color) in objects.items():
    d = data[name]

    ax.plot(
        d["x"][:frames],
        d["y"][:frames],
        color=color,
        linewidth=1.3
    )

    dots[name], = ax.plot(
        [],
        [],
        "o",
        color=color,
        markersize=6
    )

date_text = ax.text(
    0.01, 0.97, "",
    transform=ax.transAxes,
    color="white",
    fontsize=16,
    va="top"
)

ax.text(
    0.99, 0.97, "Voyager 2",
    transform=ax.transAxes,
    color="white",
    fontsize=18,
    ha="right",
    va="top"
)

info_text = ax.text(
    0.5, 0.03, "",
    transform=ax.transAxes,
    color="white",
    fontsize=14,
    ha="center"
)


def update(i):
    for name, dot in dots.items():
        d = data[name]
        dot.set_data([d["x"][i]], [d["y"][i]])

    voyager = data["Voyager 2"]

    distance = np.sqrt(
        voyager["x"][i] ** 2
        + voyager["y"][i] ** 2
        + voyager["z"][i] ** 2
    ) * AU_KM

    speed = np.sqrt(
        voyager["vx"][i] ** 2
        + voyager["vy"][i] ** 2
        + voyager["vz"][i] ** 2
    ) * AU_KM / 86400

    date_text.set_text(dates[i].strftime("%Y-%m-%d"))
    info_text.set_text(f"{speed:.1f} km/s     {distance:,.0f} km")

    return [*dots.values(), date_text, info_text]


animation = FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=15,
    blit=True,
    repeat=True,
    cache_frame_data=False
)

plt.show()

# Additional static plot: Voyager 2 speed vs time
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(dates, speeds, color="orangered")
ax2.set_xlabel("Date")
ax2.set_ylabel("Speed (km/s)")
ax2.set_title("Voyager 2 speed vs time")
ax2.grid(True)
fig2.autofmt_xdate()
plt.show()

