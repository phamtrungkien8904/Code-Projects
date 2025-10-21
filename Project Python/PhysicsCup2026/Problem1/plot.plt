reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Trajectory of the Brick'
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
    'data1.csv' using 2:3 with lines linestyle 1 title '$a_0 = 1 m/s^2$',\
    'data2.csv' using 2:3 with lines linestyle 2 title '$a_0 = 2 m/s^2$',\
    'data3.csv' using 2:3 with lines linestyle 3 title '$a_0 = 3 m/s^2$',\
    'data4.csv' using 2:3 with lines linestyle 4 title '$a_0 = 4 m/s^2$'

