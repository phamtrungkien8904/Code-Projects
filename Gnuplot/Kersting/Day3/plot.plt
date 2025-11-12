reset
set encoding utf8

set terminal epslatex color
set output 'inout.tex'


set datafile separator ","
set title "Input vs Output"
set xlabel "Input Voltage (V)"
set ylabel "Output Voltage (V)"
set xrange [0:15]
set yrange [0:6]

#line style
set style line 1 lc rgb 'red' lw 2 pt 8 ps 1



plot "data.csv" using 1:2 with points ls 1 title "Data"

set output