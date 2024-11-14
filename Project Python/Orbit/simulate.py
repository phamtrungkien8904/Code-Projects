from orbit import simulate_orbit

# Initial conditions
AU = 1.496e11  # Astronomical unit in meters
R = AU  # Scale the plot to 1 AU
initial_position = [AU, 0]  # 1 AU from the Sun
initial_velocity = [0, 29780]  # Approximate orbital speed of Earth in m/s
dt = 24* 60 * 60  # Time step in seconds (1 hour)
tmax = 365 * 24 * 60 * 60  # One year in seconds
GM = 1.32712440018e20  # Gravitational constant * mass of the Sun (m^3/s^2)

simulate_orbit(initial_position, initial_velocity, dt, tmax, GM, R)