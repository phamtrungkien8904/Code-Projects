reset
set encoding utf8 

set terminal epslatex color
set out 'exp.tex' 

# ============================ Plot Settings ============================

set title 'Comparator-based relaxation oscillator)'
set xlabel '$t$/ms'
set ylabel '$U$/V'
set xrange [2:6]
set yrange [-2:2]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'black' dt 2


plot 'data.csv' using ($1*1000):3 with lines linestyle 1 title 'Output Voltage', \
     'data.csv' using ($1*1000):2 with lines linestyle 2 title 'Capacitor Voltage', \

set out