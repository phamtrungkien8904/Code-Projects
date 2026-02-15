reset
set encoding utf8 

# set terminal epslatex color
# set out 'plot-on.tex' #################

# ============================ Plot Settings ============================



set title "Temperature of circuit (Power on)\n(Ambient temperature: -1°C)"
set ylabel 'Temperature $T$ (°C)'
set xlabel 'Time $t$ (s)'
# set grid
set xrange [0:300]
set yrange [0:250]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000




# Fit

b = 0.01
a = 175
T0 = 7
g(x) = T0 + a*(1- exp(-b*x))


h(x) =T0 + 175*(1- exp(-0.01*x))

set fit quiet
fit g(x) 'data-on.csv' using 1:2:3:4 xyerrors via a,b,T0


T_max = T0 + a

# In-plot labels (centered on lines)
set label 2 sprintf('T_{max} = %.0f°C', T_max) at 150, T_max + 10 center

# Overheat zone (150 C to T_max)
set object 1 rect from graph 0, first 150 to graph 1, first T_max fc rgb 'red' fs solid 0.3 noborder
set label 3 'Overheat' at 150, (150 + T_max) / 2 center
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
    T_max with lines ls 1 notitle

print sprintf("Fitted parameters:\na = %.2f\nb = %.4f\nT0 = %.2f°C\nT_max = %.2f°C\n", a, b, T0, T_max)

# set out