reset
set encoding utf8

# set terminal epslatex color
# set output 'signal-diode.png'

set title 'Signals over time'
set xlabel 'Time (ms)'
set ylabel 'Voltage (V)'
set xrange [-3:3]
set yrange [-2:2]
set grid
set datafile separator ','




# Keep consistent styling for input vs. output traces
set style line 1 lw 2 lc rgb 'black'
set style line 4 lw 2 lc rgb 'red'

# Plot column 2 (input) and column 3 (output)
plot \
    'data.csv' using 1:2 with lines ls 1 title 'Input',\
    '' using 1:3 with lines ls 4 title 'Output'

# set output