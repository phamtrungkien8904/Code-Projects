reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'RC-Tiefpass'
set xlabel 't'
set ylabel 'U'
set xrange [0:20]
set yrange [-1.1:1.1]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'



plot 'data.csv' using 1:3 with lines linestyle 1 title 'Output Signal', \
     'data.csv' using 1:2 with lines linestyle 2 title 'Input Signal'

