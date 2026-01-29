reset
set encoding utf8 

# set terminal epslatex color
# set out 'FM-theory.tex' 

# ============================ Plot Settings ============================

set title 'AM (Theory)'
set xlabel '$t$/ms'
set ylabel '$U$/V'
set xrange [0.5:2]
set yrange [-2:2]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'green'
set style line 4 lt 1 lw 2 lc rgb 'orange'
set style line 5 lt 1 lw 2 lc rgb 'black' dt 2


# plot 'data.csv' using ($1*1000):2 with lines linestyle 1 title 'Message Signal', \
#      'data.csv' using ($1*1000):3 with lines linestyle 2 title 'AM Signal',\


plot 'data.csv' using ($1*1000):2 with lines linestyle 1 title 'Message Signal',\
     'data.csv' using ($1*1000):3 with lines linestyle 2 title 'FM Signal',\


# plot 'data.csv' using ($1*1000):4 with lines linestyle 3 title 'AM Signal',\
#      'data.csv' using ($1*1000):5 with lines linestyle 4 title 'Capacitor Voltage',\
#      0.45 with lines linestyle 5 notitle,\
#      -0.45 with lines linestyle 5 notitle


# set out