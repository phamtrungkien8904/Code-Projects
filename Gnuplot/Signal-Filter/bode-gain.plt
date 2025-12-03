reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Bode Diagram'
set xlabel 'X=log(w/w0)'
set ylabel 'G (dB)'
set xrange [10e-5:10e5]
set logscale x 10
set format x '10^{%L}'
set yrange [-80:20]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'green'
set style line 4 lt 1 lw 1 lc rgb 'black' dt 2




H1(x) = 1/sqrt(1 + x**2)
G1(x) = 20*log10(H1(x))
fc = 1



H2(x) = 1/sqrt((1 - x**2)**2 + (3*x)**2)
G2(x) = 20*log10(H2(x))
fc = 0.374239*fc

N = 10
i = sqrt(-1)
r1(x) = 1 + 0.5*i*x + sqrt(i*x - 0.25*x**2)
r2(x) = 1 + 0.5*i*x - sqrt(i*x - 0.25*x**2)
D(x) = (((1+i*x) - r2(x))*r1(x)**N - ((1+i*x) - r1(x))*r2(x)**N)/(r1(x) - r2(x))
H(x) = 1/abs(D(x))
G(x) = 20*log10(H(x))



set arrow from 1, graph 0 to 1, graph 1 nohead dt 2 lc rgb 'black'
set arrow from fc, graph 0 to fc, graph 1 nohead dt 2 lc rgb 'black'

plot G1(x) title 'n = 1' with lines linestyle 1,\
     G2(x) title 'n = 2' with lines linestyle 2,\
     G(x) title sprintf('n = %d', N) with lines linestyle 3,\
     -3 with lines linestyle 4 notitle

