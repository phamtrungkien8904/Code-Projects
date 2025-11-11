reset
set encoding utf8

# set terminal epslatex color
# set output 'signal-diode-1k.tex'

# set title 'Signals over time (R = 100)'
set title 'Signals over time (R = 1k)'
set xlabel 'Time (ms)'
set ylabel 'Voltage (V)'
set xrange [-2.5:2.5]
set yrange [-2:2]
set grid
set datafile separator ','

set fit quiet
set fit errorvariables

g(x) = c*x + d
fit[-1:0] g(x) 'data1k-raw.csv' using 1:2 via c,d
c = 2.0
d = 0.0


# Keep consistent styling for input vs. output traces
set style line 1 lw 2 lc rgb 'blue'
set style line 4 lw 2 lc rgb 'red'
set style line 5 lw 2 dt 2 lc rgb 'black' 

# Plot column 2 (input) and column 3 (output)
plot \
    'data1k-raw.csv' using 1:2 every 200 with lines ls 1 title 'Input',\
    '' using 1:3 every 200 with lines ls 4 title 'Output',\
    g(x) with lines ls 5 title "Ideal Sawtooth"


# set output