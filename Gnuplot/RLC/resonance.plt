reset
set encoding utf8

# set terminal epslatex color
# set output 'resonance.tex'


set datafile separator ","
set title "Resonance curve"
set xlabel "$x = f/f_0$"
set ylabel "$y = \bar{I}/(\bar{U}/R)$"
set xrange [0:3]
set yrange [0:1.2]
set samples 10000

Q1 = 1
Q2 = 0.5
Q3= 5

f(x, Q) = 1/sqrt(1 + Q**2 * (x - 1/x)**2)

#line style
set style line 1 lc rgb 'red' lw 2 pt 8 ps 1
set style line 2 lc rgb 'blue' lw 2 pt 8 ps 1
set style line 3 lc rgb 'green' lw 2 pt 8 ps 1

plot f(x, Q1) title '$Q=1$' with lines linestyle 1, \
     f(x, Q2) title '$Q=0.5$' with lines linestyle 2, \
     f(x, Q3) title '$Q=5$' with lines linestyle 3


# set output