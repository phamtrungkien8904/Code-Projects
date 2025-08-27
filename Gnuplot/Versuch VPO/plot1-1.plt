## RC alternating current frequency response (R in Ohm, C in F)

set terminal epslatex color
set out 'tv1-1.tex'

set title 'RC-Glied: Frequenzgang'
set xlabel 'Frequenz $f$ (kHz)'
set ylabel 'Spannung $U$ (V)'
set xrange [0:100]
set yrange [0:1.1]



R = 10**3
C = 10**(-8)
U0 = 1.00
pi = 3.141592653589793

f(x) = U0/(sqrt(1+1/(2*pi*R*C*x*1000)**2))
g(x) = U0/(sqrt(1+(2*pi*R*C*x*1000)**2))


plot \
	f(x) title '$\hat{U}_R$' with lines lw 3 lc rgb '#1f77b4', \
	g(x) title '$\hat{U}_C$' with lines lw 3 lc rgb '#d62728'

set out
