reset
set encoding utf8

# set terminal epslatex color
# set output '1kHz.tex'


set datafile separator ","
set title "Op-Amp Single Supply (1 kHz)"
set xlabel "Time (ms)"
set ylabel "Voltage (V)"
set xrange [-2:2]
set yrange [-1.5:1.5]
set samples 10000

#line style
set style line 1 lc rgb 'red' lw 2 pt 8 ps 1
set style line 2 lc rgb 'blue' lw 2 pt 8 ps 1
set style line 3 lc rgb 'green' lw 2 pt 8 ps 1

# plot 'sin.csv' using 1:2 every 100 with lines linestyle 1 title 'Input',\
#     'sin.csv' using 1:3 every 100 with lines linestyle 2 title 'Output'

# plot 'square.csv' using 1:2 every 100 with lines linestyle 1 title 'Input',\
#     'square.csv' using 1:3 every 100 with lines linestyle 2 title 'Output'

plot 'sawtooth.csv' using 1:2 every 100 with lines linestyle 1 title 'Input',\
    'sawtooth.csv' using 1:3 every 100 with lines linestyle 2 title 'Output'
# set output