reset
set encoding utf8

# set terminal epslatex color
# set output 'inout.tex'


set datafile separator ","
set title "RLC Circuit"
set xlabel "Time $t$"
set ylabel "Capacitor Voltage $V_C(t)$"
set xrange [0:10]
set yrange [0:2]
set samples 10000



#line style
set style line 1 lc rgb 'red' lw 2 pt 8 ps 1

w0 = 10
Q = 0.7
r0 = w0/(2*Q)
w = w0*sqrt(1 - 1/(4*Q**2))

f(x) = 1 - exp(-r0*x)*cos(w*x)

plot f(x) with lines ls 1 notitle





# set output