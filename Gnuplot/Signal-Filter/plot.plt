reset
set encoding utf8 

# set terminal epslatex color
# set out 'bandpass-sweep.tex' 

# ============================ Plot Settings ============================

set title 'Signal Filter (RLC Bandpass)'
set xlabel '$t$/ms'
set ylabel '$U$/V'
set xrange [0:40]
set yrange [-2:2]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'black' dt 2


plot 'data.csv' using ($1*1000):3 with lines linestyle 1 title 'Output Signal', \
     'data.csv' using ($1*1000):2 with lines linestyle 2 title 'Input Signal'

# set out