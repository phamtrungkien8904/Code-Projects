reset
set encoding utf8 

# set terminal epslatex color
# set out 'plot-off.tex' #################

# ============================ Plot Settings ============================



set title "Temperature of circuit (Power off)\n(Ambient temperature: 26°C)"
set ylabel 'Temperature $T$ (°C)'
set xlabel 'Time $t$ (s)'
# set grid
set xrange [0:900]
set yrange [0:180]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000

# Fit
T0 = 26
f(x) = T0 + (a - T0)*exp(-b*x)
a = 140
b = 0.01

set fit quiet
fit f(x) 'data-off.csv' using 1:2:3:4 xyerrors via a,b


set label 1 'T_{amb} = 26°C' at 450, T0 - 5 center
g(x) = 27 + (140 - 27)*exp(-0.0085*x)
# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 pt 7 lc rgb 'red' 



# Plot
plot \
    'data-off.csv' using 1:2:3:4 with xyerrorbars ls 4 title 'Data', \
    f(x) with lines ls 2 title 'Fit',\
    T0 with lines ls 1 notitle



# set out