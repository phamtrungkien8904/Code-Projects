reset
set encoding utf8 

# set terminal epslatex color
# set out 'AM.tex' 

# ============================ Plot Settings ============================

set title 'AM (Experiment)'
set xlabel '$t$/ms'
set ylabel '$U$/V'
set xrange [0:3]
set yrange [-5:5]
set samples 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'green'
set style line 4 lt 1 lw 2 lc rgb 'orange'
set style line 5 lt 1 lw 2 lc rgb 'black' dt 2


# plot '1kHz-500-900DC-45V.csv' using 1:3 every 80 with lines linestyle 1 title 'Input Voltage', \
#      '1kHz-500-900DC-45V.csv' using 1:2 every 80 with lines linestyle 2 title 'Output Voltage', \

plot 'AM.csv' using 1:2 every 50 with lines linestyle 1 title 'Message Signal', \
     'AM.csv' using 1:3 every 50 with lines linestyle 2 title 'AM Signal', \

# plot 'FM.csv' using 1:2 every 50 with lines linestyle 1 title 'Message Signal', \
#      'FM.csv' using 1:4 every 50 with lines linestyle 2 title 'FM Signal', \
#      'FM.csv' using 1:3 every 50 with lines linestyle 3 title 'Intermodulated Signal', \
#      'FM.csv' using 1:5 every 50 with lines linestyle 4 title 'Capacitor Voltage'

# set out