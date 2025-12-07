import numpy as np
from scipy.linalg import eigh, solve_banded
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ================================================================
# FERMI'S GOLDEN RULE SIMULATION
# Transition rate: Γ = (2π/ℏ)|⟨f|V|i⟩|² ρ(E_f)
# We apply a sinusoidal perturbation V(x,t) = V₀ x cos(ω_p t)
# and track transition probabilities from initial state to final states
# ================================================================

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

# Perturbation parameters
V0 = 0.05                   # perturbation strength (weak perturbation)
omega_p = 1.0               # perturbation frequency

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

# Normalize all eigenstates
for i in range(len(E)):
    psi[:, i] = normalize(psi[:, i])

# Calculate matrix elements ⟨n|x|m⟩ for perturbation V = V₀ x cos(ω_p t)
n_states = min(20, len(E))  # Use first 20 states
V_matrix = np.zeros((n_states, n_states))
for i in range(n_states):
    for j in range(n_states):
        V_matrix[i, j] = V0 * np.trapezoid(psi[:, i].conj() * x * psi[:, j], x)

# Start in ground state
initial_state = 0
psi_t = psi[:, initial_state].copy()
coefficients = np.zeros(n_states, dtype=complex)
coefficients[initial_state] = 1.0

# ================================================================
# TIME EVOLUTION WITH TIME-DEPENDENT PERTURBATION
# ================================================================
T = 50.0  # longer time to see transitions
Nt = 500
dt = T / Nt
time_array = np.linspace(0, T, Nt)

# Store evolution
frames = []
prob_history = np.zeros((Nt, n_states))  # Probability in each state
psi_current = psi_t.copy()

# Time evolution using first-order perturbation theory in eigenstate basis
for idx, t in enumerate(time_array):
    # Update coefficients using time-dependent perturbation theory
    # dc_n/dt = -(i/ℏ) Σ_m c_m(t) V_nm exp(i ω_nm t) cos(ω_p t)
    dc_dt = np.zeros(n_states, dtype=complex)
    
    for n in range(n_states):
        for m in range(n_states):
            omega_nm = (E[n] - E[m]) / hbar
            # cos(ω_p t) = (exp(i ω_p t) + exp(-i ω_p t))/2
            phase1 = np.exp(1j * (omega_nm + omega_p) * t)
            phase2 = np.exp(1j * (omega_nm - omega_p) * t)
            dc_dt[n] += -1j/hbar * coefficients[m] * V_matrix[n, m] * 0.5 * (phase1 + phase2)
    
    # Simple Euler integration
    coefficients += dc_dt * dt
    
    # Reconstruct wavefunction
    psi_current = np.zeros_like(x, dtype=complex)
    for n in range(n_states):
        psi_current += coefficients[n] * psi[:, n] * np.exp(-1j * E[n] * t / hbar)
    
    frames.append(psi_current.copy())
    prob_history[idx, :] = np.abs(coefficients)**2

# ================================================================
# FERMI'S GOLDEN RULE CALCULATION
# ================================================================
# Calculate transition rate from initial state to final state at resonance
# Γ_if = (2π/ℏ)|⟨f|V|i⟩|² δ(E_f - E_i ± ℏω_p)
print("\n" + "="*60)
print("FERMI'S GOLDEN RULE - TRANSITION RATES")
print("="*60)
print(f"Perturbation: V(x,t) = {V0} x cos({omega_p} t)")
print(f"Initial state: n={initial_state}, E={E[initial_state]:.4f}")
print("\nResonant transitions (|E_f - E_i ± ℏω_p| < 0.1):")
print("-"*60)

for f in range(1, n_states):
    delta_E = abs(E[f] - E[initial_state])
    # Check if near resonance with perturbation frequency
    if abs(delta_E - hbar * omega_p) < 0.1 or abs(delta_E + hbar * omega_p) < 0.1:
        matrix_element = abs(V_matrix[f, initial_state])**2
        transition_rate = (2 * np.pi / hbar) * matrix_element
        print(f"State {initial_state}→{f}: ΔE={delta_E:.4f}, |⟨f|V|i⟩|²={matrix_element:.6f}, Γ={transition_rate:.6f}")

# ================================================================
# PLOTTING
# ================================================================
fig = plt.figure(figsize=(14, 10))

# Plot 1: Wavefunction evolution
ax1 = plt.subplot(2, 2, 1)
line_abs, = ax1.plot(x, np.abs(frames[0])**2, label="|ψ|²")
ax1.set_xlabel("Position x")
ax1.set_ylabel("Probability Density")
ax1.set_title("Wavefunction Evolution")
ax1.set_xlim(x_min, x_max)
ax1.legend()
time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, verticalalignment='top')

# Plot 2: State populations over time
ax2 = plt.subplot(2, 2, 2)
for i in range(min(5, n_states)):
    ax2.plot(time_array, prob_history[:, i], label=f"n={i}")
ax2.set_xlabel("Time")
ax2.set_ylabel("Population |c_n|²")
ax2.set_title("State Populations (Fermi's Golden Rule)")
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Energy level diagram with transitions
ax3 = plt.subplot(2, 2, 3)
for i in range(min(10, n_states)):
    ax3.hlines(E[i], 0, 1, colors='blue', linewidth=2)
    ax3.text(1.1, E[i], f"n={i}", va='center')

# Draw arrows for significant transitions
for f in range(1, min(10, n_states)):
    if abs(prob_history[-1, f]) > 0.01:  # Show if final population > 1%
        ax3.annotate('', xy=(0.5, E[f]), xytext=(0.5, E[initial_state]),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2, alpha=0.5))

ax3.set_xlim(-0.2, 1.5)
ax3.set_ylabel("Energy")
ax3.set_title("Energy Levels & Transitions")
ax3.set_xticks([])

# Plot 4: Final state distribution
ax4 = plt.subplot(2, 2, 4)
final_probs = prob_history[-1, :min(10, n_states)]
ax4.bar(range(len(final_probs)), final_probs, color='green', alpha=0.7)
ax4.set_xlabel("State n")
ax4.set_ylabel("Final Population |c_n(T)|²")
ax4.set_title(f"Final State Distribution (t={T:.1f})")
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()

# Animation function
def update(frame_index):
    psi = frames[frame_index]
    line_abs.set_ydata(np.abs(psi)**2)
    time_text.set_text(f't = {time_array[frame_index]:.2f}')
    return line_abs, time_text

anim = FuncAnimation(fig, update, frames=Nt, interval=50)
plt.show()

# # Save animation
# anim.save("fermi_golden_rule.gif", writer=PillowWriter(fps=20))
# print("\nSaved as fermi_golden_rule.gif")
