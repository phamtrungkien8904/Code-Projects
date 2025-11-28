reset
set encoding utf8`

# set terminal epslatex color
# set output 'rlc_circuit.tex'


set datafile separator ","
set title "RLC Circuit"
set xlabel "Time"
set ylabel "Voltage"
set xrange [0:2]
set yrange [-1:2]
set samples 10000

#line style
set style line 1 lc rgb 'red' lw 2 pt 8 ps 1
set style line 2 lc rgb 'blue' lw 2 pt 8 ps 1
set style line 3 lc rgb 'green' lw 2 pt 8 ps 1

w0 = 10
Q = 2
w = w0*sqrt(1 - 1/(4*Q**2))
r0 = w0/(2*Q)
U_0 = 1

U_C(x) = U_0 *(1 - exp(-r0*x)*(cos(w*x)+ (r0/w)*sin(w*x))) 
U_R(x) = U_0 *1/sqrt(Q**2 - 1/4) * exp(-r0*x)*sin(w*x)
U_L(x) = U_0 *exp(-r0*x)*(cos(w*x) - 1/sqrt(4*Q**2 -1)*sin(w*x))
`
plot U_C(x) title 'U_C(t)' with lines linestyle 1, \
     U_R(x) title 'U_R(t)' with lines linestyle 2,\
     U_L(x) title 'U_L(t)' with lines linestyle 3

# set output