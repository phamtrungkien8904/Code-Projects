reset
set encoding utf8 

# set terminal epslatex color
# set out 'bandpass-sweep.tex' 

# ============================ Plot Settings ============================

set title 'Signal Filter (RLC Bandpass)'
set xlabel '$t$/ms'
set ylabel '$U$/V'
set xrange [2:3]
set yrange [-10:10]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'green' 
set style line 4 lt 1 lw 2 lc rgb 'black' dt 2

plot 'data.csv' using ($1*1000):3 with lines linestyle 1 title 'Reference Signal', \
     'data.csv' using ($1*1000):2 with lines linestyle 2 title 'Input Signal',\
    'data.csv' using ($1*1000):4 with lines linestyle 3 title 'Mix Signal',\
    'data.csv' using ($1*1000):5 with lines linestyle 4 title 'Output Signal'

# set out