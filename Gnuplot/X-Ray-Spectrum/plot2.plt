# Duane–Hunt Verschiebungsgesetz
reset
set encoding utf8 

set title 'Röntgenspektren für verschiedene Beschleunigungsspannungen'
set xlabel 'Wellenlänge λ (pm)'
set ylabel 'Intensität (norm.)'
set xrange [0:300]
set yrange [0:2]

set samples 10000

## Parameterized minimum wavelength via Duane–Hunt (simplified proportional) λ_min ∝ 1/U
# Provide a base set of accelerating voltages (kV) and compute λ_min scaling.
U1 = 20000
U2 = 30000
U3 = 40000

# Reference λ for highest voltage (arbitrary scaling): for U3 -> λ_min_ref
h = 6.626e-34
c = 3e8
e = 1.602e-19



# Intensity scaling ~ U (simplified); adjust exponent if needed

N = 1000
# Bremsstrahlung for given U
f_raw(x,U) = N*(x/lambda_min(U) - 1)/x**2
f(x,U) = (x>=lambda_min(U)) ? ( (f_raw(x,U)>0)? f_raw(x,U) : 0 ) : 0

# Characteristic radiation spectrum (Gauss distribution)

x1 = 100
sigma1 = 0.5

x2 = 130
sigma2 = 1


g(x) = 0.5*(1/sqrt(2*pi*sigma1**2)*exp(-0.5*((x-x1)/sigma1)**2) + 1/sqrt(2*pi*sigma2**2)*exp(-0.5*((x-x2)/sigma2)**2))

total(x,U) = f(x,U) + g(x)


# Vertical lines at Gaussian peak centers x1 and x2
set style line 1 lc rgb '#d62728' lw 1.5 dt 2
set style line 2 lc rgb '#2ca02c' lw 1.5 dt 2
set label 1 sprintf('λ_1 = %.2f pm', x1) at x1, 0.95 left tc rgb '#d62728'
set label 2 sprintf('λ_2 = %.2f pm', x2) at x2, 0.90 left tc rgb '#2ca02c'

set arrow 1 from x1,0 to x1,2 nohead ls 1
set arrow 2 from x2,0 to x2,2 nohead ls 2



plot \
	normalize(x,U1)+offset(U1) with lines lw 2 lc rgb '#1f77b4' title sprintf('U=%.0f kV (λ_min=%.1f pm)', U1, lambda_min(U1)), \
	normalize(x,U2)+offset(U2) with lines lw 2 lc rgb '#ff7f0e' title sprintf('U=%.0f kV (λ_min=%.1f pm)', U2, lambda_min(U2)), \
	normalize(x,U3)+offset(U3) with lines lw 2 lc rgb '#2ca02c' title sprintf('U=%.0f kV (λ_min=%.1f pm)', U3, lambda_min(U3))

