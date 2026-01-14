reset
set encoding utf8 

# set terminal epslatex color
# set out 'exp.tex' 

# ============================ Plot Settings ============================

set title 'Wien-Robinson oscillator'
set xlabel '$t$/ms'
set ylabel '$U$/V'
set xrange [2:6]
set yrange [-15:15]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'black' dt 2


plot 'data12V.csv' using 1:3 every 80 with lines linestyle 1 title 'Input Voltage', \
     'data12V.csv' using 1:2 every 80 with lines linestyle 2 title 'Output Voltage', \

# set out