reset
set encoding utf8

# set terminal pngcairo size 1200,600
# set output 'signal.png'

set title 'Characteristic Diode Fit'
set xlabel 'V'
set ylabel 'ln(I)'
# set xrange [0:2]
# set yrange [0:0.01]
set grid
set datafile separator ','

set fit quiet
f(x) = a*x + b # ln(I) = q/kT*V + ln(IS) for V large enough 
fit[0.6:] f(x) 'data.csv' using ($2 - $3):(log($3/1000)) via a,b

# Keep consistent styling for input vs. output traces
set style line 1 lw 2 lc rgb 'black'
set style line 4 lw 2 lc rgb 'red'

# Plot column 2 (input) and column 3 (output)
plot \
    [0:]'data.csv' using ($2 - $3):(log($3/1000)) with lines ls 4 title 'Data Points',\
    f(x) with lines lc rgb 'blue' lw 2 title sprintf('Fit: I_S = %.2e (A)', exp(b))
# set output