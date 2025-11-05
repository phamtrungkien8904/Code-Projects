reset
set encoding utf8

# set terminal pngcairo size 1200,600
# set output 'signal.png'

set title 'Characteristic Diode Response'
set xlabel 'Voltage (V)'
set ylabel 'Current (A)'
set xrange [-1:2]
set yrange [-0.01:0.01]
set grid
set datafile separator ','


# Keep consistent styling for input vs. output traces
set style line 1 lw 2 lc rgb 'black'
set style line 4 lw 2 lc rgb 'red'

# Plot column 2 (input) and column 3 (output)
plot \
    'data.csv' using ($2 - $3):($3/100) with lines ls 1 notitle

# set output