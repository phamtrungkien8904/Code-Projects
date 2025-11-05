reset
set encoding utf8

# set terminal pngcairo size 1200,600
# set output 'signal.png'

set title 'Input vs Output'
set xlabel 'Output Voltage (V)'
set ylabel 'Input Voltage (V)'
set xrange [-3:3]
set yrange [-2:2]
set grid
set datafile separator ','

# Diode current-voltage relationship
VT = 0.05
IS = 1e-10
I(x) = IS*(exp(x/VT)-1)

set fit quiet
f(x) = a*x + b
fit[1:2] f(x) 'data.csv' using 2:3 via a,b


print sprintf("Diode 1N4148")
print sprintf("Forward Voltage: %.4f (V)", -b/a)

# Keep consistent styling for input vs. output traces
set style line 1 lw 2 lc rgb 'black'
set style line 4 lw 2 lc rgb 'red'



plot\
    'data.csv' using ($2>=-2 && $2<=2 ? $2 : 1/0):3 with lines ls 4 title 'Data',\
    f(x) with lines lc rgb 'blue' lw 2 title sprintf('Fit: V_F = %.2f', -b/a)
# set output