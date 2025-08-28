reset
set encoding utf8 

set title 'Röntgenspektrum'
set xlabel 'Wellenlänge λ (pm)'
set ylabel 'Intensität (norm.)'
set xrange [0:300]
set yrange [0:2]

set samples 10000

lambda_0 = 20

# Bremsstrahlung spectrum

N0 = 10**3

# Bremsstrahlung only for x >= lambda_0 ; else 0. Also force non-negative.
f_raw(x) = N0*(x/lambda_0 - 1)/x**2
f(x) = (x>=lambda_0) ? ( (f_raw(x)>0)? f_raw(x) : 0 ) : 0

# Characteristic radiation spectrum (Gauss distribution)

x1 = 100
sigma1 = 0.5

x2 = 130
sigma2 = 1


g(x) = 1/sqrt(2*pi*sigma1**2)*exp(-0.5*((x-x1)/sigma1)**2) + 1/sqrt(2*pi*sigma2**2)*exp(-0.5*((x-x2)/sigma2)**2)

total(x) = f(x) + g(x)


# Vertical lines at Gaussian peak centers x1 and x2
set style line 1 lc rgb '#d62728' lw 1.5 dt 2
set style line 2 lc rgb '#2ca02c' lw 1.5 dt 2
set label 1 sprintf('λ_1 = %.2f pm', x1) at x1, 0.95 left tc rgb '#d62728'
set label 2 sprintf('λ_2 = %.2f pm', x2) at x2, 0.90 left tc rgb '#2ca02c'

set arrow 1 from x1,0 to x1,2 nohead ls 1
set arrow 2 from x2,0 to x2,2 nohead ls 2

plot \
	total(x) with lines lw 2 lc rgb '#1f77b4' title 'Röntgenspektrum'

