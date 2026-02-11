reset
set encoding utf8 

# set terminal epslatex color
# set out 'plot-on.tex' #################

# ============================ Plot Settings ============================



set title "Temperature of circuit (Power on)\n(Ambient temperature: 26°C)"
set ylabel 'Temperature $T$ (°C)'
set xlabel 'Time $t$ (s)'
# set grid
set xrange [0:120]
set yrange [0:250]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000




# Fit
T0 = 26
b = 0.01
a = 175
g(x) = T0 + a*(1- exp(-b*x))


h(x) =T0 + 175*(1- exp(-0.01*x))

set fit quiet
fit g(x) 'data-on.csv' using 1:2:3:4 xyerrors via a,b


T_max = T0 + a

# In-plot labels (centered on lines)
set label 1 'T_{amb} = 26°C' at 60, T0 - 10 center
set label 2 sprintf('T_{max} = %.0f°C', T_max) at 60, T_max + 10 center

# Overheat zone (150 C to T_max)
set object 1 rect from graph 0, first 150 to graph 1, first T_max fc rgb 'red' fs solid 0.3 noborder
set label 3 'Overheat' at 60, (150 + T_max) / 2 center
# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 pt 7 lc rgb 'red' 



# Plot
plot \
    'data-on.csv' using 1:2:3:4 with xyerrorbars ls 4 title 'Data', \
    g(x) with lines ls 2 title 'Fit',\
    T0 with lines ls 1 notitle, \
    T_max with lines ls 1 notitle

# set out