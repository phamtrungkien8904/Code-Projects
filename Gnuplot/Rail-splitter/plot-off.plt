reset
set encoding utf8 

# set terminal epslatex color
# set out 'plot-on.tex' #################

# ============================ Plot Settings ============================



set title "Temperature of circuit (Power off)\n(Ambient temperature: 24 °C)"
set ylabel 'Temperature $T$ (°C)'
set xlabel 'Time $t$ (s)'
# set grid
set xrange [0:900]
set yrange [0:180]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000




# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 2 pt 4 ps 1.0 dt 3 lc rgb 'red' 



# Plot
plot \
    'data-off.csv' using 1:2 with linespoints ls 4 notitle, \
    24 with lines ls 1 notitle


# set out