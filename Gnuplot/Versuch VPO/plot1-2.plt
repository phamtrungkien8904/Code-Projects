## RL alternating current frequency response (R in Ohm, L in H)
reset

set terminal epslatex color
set out 'tv1-2.tex'

set title 'RL-Glied: Frequenzgang'
set xlabel 'Frequenz $f$ (kHz)'
set ylabel 'Spannung $U$ (V)'
set xrange [0:40]
set yrange [0:1.1]



R = 10**3
L = 0.12
U0 = 1.00
pi = 3.141592653589793

g(x) = U0/(sqrt(1+R**2/(2*pi*L*x*1000)**2))
f(x) = U0/(sqrt(1+(2*pi*L*x*1000)**2/R**2))


plot \
	f(x) title '$\hat{U}_R$' with lines lw 3 lc rgb '#1f77b4', \
	g(x) title '$\hat{U}_L$' with lines lw 3 lc rgb '#d62728'

set out
