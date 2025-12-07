import numpy as np
from scipy.linalg import eigh, solve_banded
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ================================================================
# PARAMETERS
# ================================================================
m = 1.0
omega = 1.0
hbar = 1.0
N = 1000                   # number of intervals (→ N+1 grid points)
x_min, x_max = -10.0, 10.0
x = np.linspace(x_min, x_max, N+1)
dx = x[1] - x[0]

# ================================================================
# HAMILTONIAN (TRIDIAGONAL)
# ================================================================
diag = 1.0/dx**2 + 0.5 * m * omega**2 * x**2
off = -0.5/dx**2 * np.ones(N)

# H acting on a vector (fast, avoids dense matrix multiply)
def H_dot(psi):
    res = diag * psi
    res[:-1] += off * psi[1:]
    res[1:]  += off * psi[:-1]
    return res

# Build dense matrix only once for eigen-decomposition
H_dense = np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)

# ================================================================
# EIGENSTATES
# ================================================================
E, psi = eigh(H_dense)

def normalize(v):
    return v / np.sqrt(np.trapezoid(np.abs(v)**2, x))

psi0 = normalize(psi[:, 0])
psi1 = normalize(psi[:, 1])

# initial wavefunction ψ(0) = (ψ0 + ψ1)/√2
psi_t = (psi0 + psi1) / np.sqrt(2)

# ================================================================
# TIME EVOLUTION (CAYLEY METHOD)
# ================================================================
T = 4 * np.pi / omega
Nt = 150
dt = T / Nt

coef = 0.5j * dt / hbar     # Cayley coefficient

# A = I + coef * H  (banded form for fast solving)
ab_A = np.zeros((3, N+1), dtype=complex)
ab_A[1, :] = 1.0 + coef * diag         # main diagonal
ab_A[0, 1:] = coef * off               # upper diagonal
ab_A[2, :-1] = coef * off              # lower diagonal

frames = []
psi_current = psi_t.copy()

for _ in range(Nt):
    # B ψ = ψ - coef * H ψ
    rhs = psi_current - coef * H_dot(psi_current)
    # Solve A ψ_{t+dt} = B ψ_t
    psi_next = solve_banded((1, 1), ab_A, rhs)
    psi_current = psi_next
    frames.append(psi_current.copy())

# ================================================================
# ANIMATION
# ================================================================
fig, ax = plt.subplots(figsize=(8, 4))
line_re, = ax.plot(x, np.real(frames[0]), label="Re ψ")
line_im, = ax.plot(x, np.imag(frames[0]), label="Im ψ")
line_abs, = ax.plot(x, np.abs(frames[0]), label="|ψ|")

ax.legend(loc="upper right")
ax.set_xlabel("x")
ax.set_title("Time evolution (Cayley) of ψ — Re, Im, |ψ|")

# Set vertical limits based on first frame
ymax = np.max(np.abs(frames[0]))
ax.set_ylim(-1.2 * ymax, 1.2 * ymax)

def update(frame_index):
    psi = frames[frame_index]
    line_re.set_ydata(np.real(psi))
    line_im.set_ydata(np.imag(psi))
    line_abs.set_ydata(np.abs(psi))
    return line_re, line_im, line_abs

anim = FuncAnimation(fig, update, frames=Nt, interval=50)
plt.show()

# # Save animation
# anim.save("schrodinger_animation.gif", writer=PillowWriter(fps=20))
# print("Saved as schrodinger_animation.gif")
