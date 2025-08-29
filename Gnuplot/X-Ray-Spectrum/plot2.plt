# Duane–Hunt Verschiebungsgesetz
reset
set encoding utf8 

set title 'Röntgenspektren der Molybdän-Anode für verschiedene Beschleunigungsspannungen'
set xlabel 'Wellenlänge λ (pm)'
set ylabel 'Intensität (norm.)'
set yrange [0:10]
set xrange [0:150]

set samples 10000

## Parameterized minimum wavelength via Duane–Hunt (simplified proportional) λ_min ∝ 1/U
# Provide a base set of accelerating voltages (kV) and compute λ_min scaling.
U1 = 17.7 # kV
U2 = 23.5 # kV
U3 = 29.3 # kV
U4 = 35.0 # kV

# Reference λ for highest voltage (arbitrary scaling): for U3 -> λ_min_ref
HC_e_pm_factor = 1.239841984e3   # (hc/e) (pm*kV) expressed so that λ_min(pm) = 1.23984e3 / U(kV)
lambda_min(U) = HC_e_pm_factor / U  # pm



# Bremsstrahlung continuum:
# Use approximate shape I(λ) ∝ U**1.5 * (1 - λ_min/λ) / λ^2 for λ ≥ λ_min, else 0.
scaleB = 3e2      # tuning factor; increase if still too low (≈0.00005–0.0001 range)
Ibrems_raw(x,U) = scaleB * U**1.5 * (1 - lambda_min(U)/x) / x**2
f(x,U) = (x>=lambda_min(U)) ? ( (Ibrems_raw(x,U) > 0) ? Ibrems_raw(x,U) : 0 ) : 0

lambda_Imax(U) = 3/2 * lambda_min(U)

# Characteristic radiation spectrum (Gauss distributions)
lambda_alpha = 71.08 # pm (Kα)
lambda_beta  = 63.09 # pm (Kβ)
sigma = 0.1  # standard deviation of both Gaussians

# Lines only appear if accelerating voltage is high enough: lambda_min(U) < lambda_line.
N1(U) = (lambda_min(U) < lambda_alpha ? 4e-3 * U**1.5 : 0)  # Kα intensity scaling
N2(U) = (lambda_min(U) < lambda_beta  ? 1e-3 * U**1.5 : 0)  # Kβ intensity scaling (weaker)

g(x,U) = N1(U)/sqrt(2*pi*sigma**2)*exp(-0.5*((x-lambda_alpha)/sigma)**2) \
	+ N2(U)/sqrt(2*pi*sigma**2)*exp(-0.5*((x-lambda_beta )/sigma)**2)

total(x,U) = f(x,U) + g(x,U)



# Vertical lines at Gaussian peak centers (only if any spectrum actually contains the line)
set style line 1 lc rgb '#d62728' lw 1.5 dt 2
set style line 2 lc rgb '#2ca02c' lw 1.5 dt 2

show_Ka = (lambda_min(U1) < lambda_alpha || lambda_min(U2) < lambda_alpha || lambda_min(U3) < lambda_alpha || lambda_min(U4) < lambda_alpha)
show_Kb = (lambda_min(U1) < lambda_beta  || lambda_min(U2) < lambda_beta  || lambda_min(U3) < lambda_beta  || lambda_min(U4) < lambda_beta )

if (show_Ka) set label 1 sprintf('λ_{Kα} = %.2f pm', lambda_alpha) at (lambda_alpha+1), 8.0 right rotate by 90 tc rgb '#d62728'
if (show_Kb) set label 2 sprintf('λ_{Kβ} = %.2f pm', lambda_beta ) at (lambda_beta +1), 8.0 right rotate by 90 tc rgb '#2ca02c'

if (show_Ka) set arrow 1 from lambda_alpha,0 to lambda_alpha,10 nohead ls 1
if (show_Kb) set arrow 2 from lambda_beta ,0 to lambda_beta ,10 nohead ls 2



plot \
	total(x,U1) with lines lw 2 lc rgb '#1f77b4' title sprintf('U=%.0f kV (λ_{min}=%.2f pm)', U1, lambda_min(U1)), \
	total(x,U2) with lines lw 2 lc rgb '#ff7f0e' title sprintf('U=%.0f kV (λ_{min}=%.2f pm)', U2, lambda_min(U2)), \
	total(x,U3) with lines lw 2 lc rgb '#2ca02c' title sprintf('U=%.0f kV (λ_{min}=%.2f pm)', U3, lambda_min(U3)), \
	total(x,U4) with lines lw 2 lc rgb '#9467bd' title sprintf('U=%.0f kV (λ_{min}=%.2f pm)', U4, lambda_min(U4))