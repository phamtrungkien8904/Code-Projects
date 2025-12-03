reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Bode diagram (Phase)'
set xlabel 'X=log(w/w0)'
set ylabel 'Phase (degrees)'
set xrange [10e-5:10e5]
set logscale x 10
set format x '10^{%L}'
set yrange [-90:90]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 1 lc rgb 'black' dt 2




H1(x) = 1/sqrt(1 + x**2)
phi1(x) = -atan(x)*180/pi
fc = 1


H2(x) = 1/sqrt((1 - x**2)**2 + (3*x)**2)
phi2(x) = -atan(abs((3*x)/(1 - x**2)))*180/pi
fc = 0.374239*fc

# set arrow from 1, graph 0 to 1, graph 1 nohead dt 2 lc rgb 'black'
# set arrow from fc, graph 0 to fc, graph 1 nohead dt 2 lc rgb 'black'

plot phi1(x) title 'n = 1' with lines linestyle 1,\
     phi2(x) title 'n = 2' with lines linestyle 2