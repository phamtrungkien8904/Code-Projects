reset
set encoding utf8

# set terminal pngcairo size 1200,600
# set output 'signal.png'

set title 'Diode Response'
set xlabel 'Time (s)'
set ylabel 'Voltage (V)'
set grid
set datafile separator ','

# Keep consistent styling for input vs. output traces
set style line 1 lw 2 lc rgb 'black'
set style line 4 lw 2 lc rgb 'red'

# Plot column 2 (input) and column 3 (output)
plot \
    'diode_response.csv' using 1:2 with lines ls 1 title 'Input', \
    '' using 1:3 with lines ls 4 title 'Output'

# set output