set title 'RC-Glied: Frequenzgang'
set xlabel 'Frequenz f (kHz)'
set ylabel 'Spannung U (V)'
set xrange [0:100]
set yrange [0:1.1]



R = 10**3
C = 10**(-8)
U0 = 1.00
p = 3.141592653589793

f(x) = U0/(sqrt(1+1/(2*p*R*C*x*1000)**2))
g(x) = U0/(sqrt(1+(2*p*R*C*x*1000)**2))

plot \
	f(x) title 'U_R' with lines lw 2 lc rgb '#1f77b4', \
	g(x) title 'U_C' with lines lw 2 lc rgb '#d62728'