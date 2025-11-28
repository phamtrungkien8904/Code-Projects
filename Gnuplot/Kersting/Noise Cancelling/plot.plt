reset
set encoding utf8

# set terminal epslatex color
# set output 'inout.tex'


set datafile separator ","
set title "Noise Cancelling Characterization"
set ylabel "Voltage (V)"
set xlabel "Time (ms)"
set xrange [-2.5:2.5]
set yrange [-0.7:0.7]
set key inside bottom right

#line style
set style line 1 lc rgb 'red' lw 2 pt 8 ps 1
set style line 2 lc rgb 'blue' lw 2 pt 6 ps 1
set style line 3 lc rgb 'green' lw 2 pt 4 ps 1
set style line 4 lc rgb 'orange' lw 2 pt 2 ps 1



plot "data-offset.csv" using 1:2 every 100 with lines ls 1 title "Noise", \
     "data-offset.csv" using 1:3 every 100 with lines ls 2 title "Music", \
     "data-offset.csv" using 1:5 every 100 with lines ls 4 title "Output"

# set output