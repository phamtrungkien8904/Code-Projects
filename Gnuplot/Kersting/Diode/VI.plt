reset
set encoding utf8

# set terminal pngcairo size 1200,600
# set output 'signal.png'

set title 'Characteristic Diode Response'
set xlabel 'Voltage (V)'
set ylabel 'Current (A)'
set xrange [-1:2]
set yrange [-0.0005:0.001]
set grid
set datafile separator ','

# set fit quiet
# I(x) = a*(exp(b*x)-1)
# fit I(x) 'data.csv' using ($2 - $3):($3/1000) every 100 via a,b


# Keep consistent styling for input vs. output traces
set style line 1 lw 2 lc rgb 'black'
set style line 4 lw 2 lc rgb 'red'

# Plot column 2 (input) and column 3 (output)
plot \
    'data.csv' using ($2 - $3):($3/1000) with lines ls 1 notitle
    # I(x) with lines ls 4 title sprintf('Fit: I_S = %.2e (A)', a)

# set output