reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Signal Filter'
set xlabel 't/s'
set ylabel 'U/V'
set xrange [0:0.2]
set yrange [-2:2]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'black' dt 2

tau_C = 2.0  # Capacitor time constant
tau_L = 0.5  # Inductance time constant
f0 = 1/(2*pi*sqrt(tau_L * tau_C))  # Resonant frequency
f = f0

f(x) = 1*sin(2*pi*f*x)


plot 'data.csv' using 1:3 with lines linestyle 1 title 'Output Signal', \
     'data.csv' using 1:2 with lines linestyle 2 title 'Input Signal', \
     'data.csv' using 1:4 with lines linestyle 3 title 'Transfer Function (Amplitude)', \
     'data.csv' using 1:(-$4) with lines linestyle 3 notitle

