reset
set encoding utf8 

set terminal epslatex color
set out 'plot2.tex'

# ============================ Plot Settings ============================

set title 'Trajectory of the Brick with different initial accelerations'
set xlabel '$x$ (m)'
set ylabel '$y$ (m)'
set xrange [0:1]
set yrange [0:1]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'orange'
set style line 4 lt 1 lw 2 lc rgb 'green'

set style line 5 lt 1 lw 2 lc rgb 'black' dt 2




plot \
    'data1.csv' using 2:3 with lines linestyle 1 title '$v = 1\ \mathrm{m/s}$',\
    'data5.csv' using 2:3 with lines linestyle 2 title '$v = 2\ \mathrm{m/s}$',\
    'data6.csv' using 2:3 with lines linestyle 3 title '$v = 3\ \mathrm{m/s}$',\
    'data7.csv' using 2:3 with lines linestyle 4 title '$v = 4\ \mathrm{m/s}$'

set out