reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Force Oscillator Simulation'
set xlabel 't'
set ylabel 'x'
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'blue'


plot 'data.csv' using 1:2 with lines linestyle 1 title 'Data', \
     'data.csv' using 1:5 with lines linestyle 2 title 'Theoretical Amplitude',\
        'data.csv' using 1:(-$5) with lines linestyle 3 notitle
