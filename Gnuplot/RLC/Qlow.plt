reset
set encoding utf8

set terminal epslatex color
set output 'Qlow.tex'


set datafile separator ","
set title "RLC Circuit"
set xlabel "Time"
set ylabel "Voltage/$U_0$"
set xrange [0:2]
set yrange [-0.5:1.5]
set samples 10000

#line style
set style line 1 lc rgb 'red' lw 2 pt 8 ps 1
set style line 2 lc rgb 'blue' lw 2 pt 8 ps 1
set style line 3 lc rgb 'green' lw 2 pt 8 ps 1

w0 = 10
Q = 0.2
r = w0*sqrt(1/(4*Q**2) - 1)
r0 = w0/(2*Q)


U_C(x) = 1 *(1 - exp(-r0*x)*(cosh(r*x)+ 1/sqrt(1-4*Q**2)*sinh(r*x))) 
U_R(x) = 1 *2/sqrt(1-4*Q**2) * exp(-r0*x)*sinh(r*x)
U_L(x) = 1 *exp(-r0*x)*(cosh(r*x) - 1/sqrt(1-4*Q**2)*sinh(r*x))
`
plot U_C(x) title '$U_C(t)$' with lines linestyle 1, \
     U_R(x) title '$U_R(t)$' with lines linestyle 2,\
     U_L(x) title '$U_L(t)$' with lines linestyle 3

set output