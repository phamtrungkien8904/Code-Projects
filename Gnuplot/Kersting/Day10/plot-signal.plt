reset
set encoding utf8 

# set terminal epslatex color
# set out 'signal.tex'

# ============================ Plot Settings ============================

set title 'Sweep Signal'
set ylabel 'Signal (V)'
set xlabel 'Time (ms)'
# set grid
set xrange [0:0.05]
set yrange [-2:2]
set datafile separator ','
set samples 10000



# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 pt 7 ps 0.3 lc rgb 'black'
set style line 2 pt 7 ps 0.3 lc rgb 'blue' 
set style line 3 pt 7 ps 0.3 lc rgb 'purple'
set style line 4 pt 7 ps 0.3 lc rgb 'red'




# Plot
plot \
    'data.csv' using 1:2 every 3 with line ls 2 title 'Input Signal',\
    'data.csv' using 1:3 every 3 with line ls 4 title 'Output Signal'



# set out