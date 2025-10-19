reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Trajectory of the Brick'
set xlabel 'x (m)'
set ylabel 'y (m)'
set xrange [0:1]
set yrange [0:1]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'black' dt 2




plot 'data.csv' using 2:3 with lines linestyle 1 title 'Coordinates'

