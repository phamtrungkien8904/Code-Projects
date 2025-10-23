set title 'RLC Bandpass Filter'
set xlabel 'f (Hz)'
set ylabel 'H(f)'
set xrange [0:100]
set logscale x 10
set yrange [0:1]
# set logscale y 10
set samples 10000

R= 1
L=1
C=1/L/(2*pi*10)**2
H(x) = 1/sqrt(1+ R**2/((2*pi*x*L - 1/(2*pi*x*C))**2))




plot \
	H(x) notitle with lines lw 2 lc rgb 'red'