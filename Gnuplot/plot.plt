set xrange [0:6]
set yrange [-2:2]
set grid
set title "Damped Oscillation"
set xlabel "x"
set ylabel "y"


f(x) = 2*sin(4*x)*exp(-x)
plot f(x) with lines ls 6