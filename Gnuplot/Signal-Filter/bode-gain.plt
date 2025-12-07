reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Bode Diagram'
set xlabel 'X=log(w/w0)'
set ylabel 'G (dB)'
set xrange [10e-5:10e5]
set logscale x 10
set format x '{%L}'
set yrange [-80:20]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'green'
set style line 4 lt 1 lw 1 lc rgb 'black' dt 2
set style line 5 lt 1 lw 2 lc rgb 'orange'




H1(x) = 1/sqrt(1 + x**2)
G1(x) = 20*log10(H1(x))
fc = 1



H2(x) = 1/sqrt((1 - x**2)**2 + (3*x)**2)
G2(x) = 20*log10(H2(x))
fc = 0.374239*fc

i = sqrt(-1)
lamb(x) = acosh(1 + i*x/2)
H(x,N) = cosh(lamb(x)*0.5)/cosh(lamb(x)*(N + 0.5)) 
G(x,N) = 20*log10(abs(H(x,N)))
phi(x,N) = arg(H(x,N)) * 180 / pi



# set arrow from 1, graph 0 to 1, graph 1 nohead dt 2 lc rgb 'black'
# set arrow from fc, graph 0 to fc, graph 1 nohead dt 2 lc rgb 'black'

plot G(x,1) title sprintf('n = %d', 1) with lines linestyle 1,\
     G(x,2) title sprintf('n = %d', 2) with lines linestyle 2,\
     G(x,6) title sprintf('n = %d', 6) with lines linestyle 3,\
     G(x,10) title sprintf('n = %d', 10) with lines linestyle 5,\
     -3 with lines linestyle 4 notitle

