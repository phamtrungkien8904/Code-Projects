reset
set encoding utf8

# set terminal epslatex color
# set output 'RLC1.tex'


set datafile separator ","
set title "RLC Circuit ($Q=10,\ \omega = 0.1 \omega_0$)"
set xlabel "Time"
set ylabel "Voltage"
set xrange [0:40]
set yrange [-2:2]
set samples 10000

#line style
set style line 1 lc rgb 'red' lw 2 pt 8 ps 1
set style line 2 lc rgb 'blue' lw 2 pt 8 ps 1
set style line 3 lc rgb 'green' lw 2 pt 8 ps 1

plot 'data.csv' using 1:2 title '$e(t)$' with lines linestyle 1, \
     '' using 1:3 title '$U_R \times 10$' with lines linestyle 2, 

# set output