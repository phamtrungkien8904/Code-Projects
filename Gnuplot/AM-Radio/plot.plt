reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Waveform of AM Radio Signal'
set xlabel 't/s'
set ylabel 'U/V'
# set xrange [0:5]
# set yrange [-2:2]
set sample 10000
# set grid
set datafile separator ','

set style line 1 lt 1 lw 2 lc rgb 'red'
set style line 2 lt 1 lw 2 lc rgb 'blue'
set style line 3 lt 1 lw 2 lc rgb 'black' dt 2


# # Message signal
# f_m = 1
# m(x) = 1*sin(2*pi*f_m*x) + 0.3*sin(2*pi*2*f_m*x) + 0.2*sin(2*pi*5*f_m*x)
# # Carrier signal
# f_c = 10
# c(x) = 1*sin(2*pi*f_c*x)
# # AM signal
# mu = 0.8
# e(x) = 1 + mu*m(x)
# s(x) = e(x)*c(x)

plot 'data.csv' using 1:(3*$7) with lines ls 1 title 'Tuned Signal',\
    'data.csv' using 1:4 with lines ls 2 title 'AM Signal'

