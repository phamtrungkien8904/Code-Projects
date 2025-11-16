import numpy as np
import matplotlib.pyplot as plt


# Constant
hbar = 1.0  # Reduced Planck's constant in J·s
me = 1.0   # Electron mass in kg


# Parameters

nx = 100
nt = 100

x_min = -5
x_max = 5
dx = (x_max - x_min) / (nx - 1)

t_min = 0
t_max = 1
dt = (t_max - t_min) / (nt - 1)

# Infinite square well potential


# Time-independent schrödinger equation solver
def schroedinger(x)