reset
set encoding utf8 

set terminal epslatex color
set out 'tv0.tex'

set title 'Magnetfeld gegen Schleifenradius'
set xlabel 'Radius $r/cm$'
set ylabel '$\Delta B_z/\mathrm{\mu T}$'

set samples 10000



set style line 1 lt 1 lw 2 lc rgb '#d62728'
set style line 2 pt 7 ps 1 lc rgb '#111111'


# Linear Regression Fit
f(x) = a*(1/x) + b

set fit quiet
fit f(x) 'data.csv' using 1:2 via a,b 

plot \
	'data.csv' using 1:2:(0.1):(2.0) with xyerrorbars ls 2 title 'Messdaten', \
	f(x) with lines ls 1 title 'Fitkurve $f(x) = a/x + b$'

set out